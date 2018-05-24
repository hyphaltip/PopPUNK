#!/usr/bin/env python
# Copyright 2018 John Lees and Nick Croucher

# universal
import os
import sys
# additional
import numpy as np
import subprocess
from tempfile import mkstemp

# import poppunk package
from .__init__ import __version__

from .mash import checkMashVersion
from .mash import createDatabaseDir
from .mash import storePickle
from .mash import readPickle
from .mash import iterDistRows
from .mash import constructDatabase
from .mash import getKmersFromReferenceDatabase
from .mash import getSketchSize

#################
# run main code #
#################

# command line parsing
def get_options():

    import argparse

    parser = argparse.ArgumentParser(description='Remove sequences from a PopPUNK database',
                                     prog='prune_poppunk')

    # input options
    iGroup = parser.add_argument_group('Input files')
    iGroup.add_argument('--remove', required=True, help='File listing sequences to remove (required)')
    iGroup.add_argument('--distances', required=True, help='Prefix of input pickle of pre-calculated distances (required)')
    iGroup.add_argument('--ref-db', help='Location of reference db, if resketching')

    # output options
    oGroup = parser.add_argument_group('Output options')
    oGroup.add_argument('--output', required=True, help='Prefix for output files (required)')
    oGroup.add_argument('--resketch', default=False, action='store_true', help='Resketch the non-excluded sequences '
                                                                                '[default = False]')

    # processing
    other = parser.add_argument_group('Other options')
    other.add_argument('--mash', default='mash', help='Location of mash executable')
    other.add_argument('--threads', default=1, type=int, help='Number of threads to use [default = 1]')

    other.add_argument('--version', action='version',
                       version='%(prog)s '+__version__)

    return parser.parse_args()

def main():

    # Check input ok
    args = get_options()
    checkMashVersion(args.mash)
    if args.resketch and (args.ref_db is None or not os.path.isdir(args.ref_db)):
        sys.stderr.write("Must provide original --ref-db if using --resketch\n")
        sys.exit(1)

    # Read in old distances
    refList, queryList, self, distMat = readPickle(args.distances)
    if not self:
        raise RuntimeError("Distance DB should be self-self distances")

    # Read in seqs to remove
    remove_seqs_in = []
    with open(args.remove, 'r') as remove_file:
        for line in remove_file:
            remove_seqs_in.append(line.rstrip())

    # Find list items to remove
    remove_seqs = []
    removal_indices = []
    for to_remove in remove_seqs_in:
        found = False
        for idx, item in enumerate(refList):
            if item == to_remove:
                removal_indices.append(idx)
                remove_seqs.append(item)
                found = True
                break
        if not found:
            sys.stderr.write("Couldn't find " + to_remove + " in database\n")

    if len(remove_seqs) > 0:
        sys.stderr.write("Removing " + str(len(remove_seqs)) + " sequences\n")

        numNew = len(refList) - len(remove_seqs)
        newDistMat = np.zeros((int(0.5 * numNew * (numNew - 1)), 2))

        # Create new reference list iterator
        removal_indices.sort()
        removal_indices.reverse()
        next_remove = removal_indices.pop()
        newRefList = []
        for idx, seq in enumerate(refList):
            if idx == next_remove:
                if len(removal_indices) > 0:
                    next_remove = removal_indices.pop()
            else:
                newRefList.append(seq)

        newRowNames = iter(iterDistRows(newRefList, newRefList, self=True))

        # Copy over rows which don't have an excluded sequence
        newIdx = 0
        for distRow, (ref1, ref2) in zip(distMat, iterDistRows(refList, refList, self=True)):
            if ref1 not in remove_seqs and ref2 not in remove_seqs:
                (newRef1, newRef2) = next(newRowNames)
                if newRef1 == ref1 and newRef2 == ref2:
                    newDistMat[newIdx, :] = distRow
                    newIdx += 1
                else:
                    raise RuntimeError("Row name mismatch. Old: " + ref1 + "," + ref2 + "\n"
                                       "New: " + newRef1 + "," + newRef2 + "\n")

        storePickle(newRefList, newRefList, True, newDistMat, args.output)

        if args.resketch:
            sys.stderr.write("Resketching sequences\n")

            # Write names to file
            tmpHandle, tmpName = mkstemp(prefix=args.output, suffix=".tmp", dir=".")
            with open(tmpName, 'w') as tmpRefFile:
                for newRefSeq in newRefList:
                    tmpRefFile.write(newRefSeq + "\n")

            # Find db properties
            kmers = getKmersFromReferenceDatabase(args.ref_db)
            sketch_sizes = getSketchSize(args.ref_db, kmers, args.mash)

            # Resketch all
            createDatabaseDir(args.output, kmers)
            constructDatabase(tmpName, kmers, sketch_sizes, args.output, args.threads, args.mash, True)

            os.rename(args.output + ".pkl", args.output + "/" + args.output + ".pkl")
            os.rename(args.output + ".npy", args.output + "/" + args.output + ".npy")
            os.remove(tmpName)
    else:
        sys.stderr.write("No sequences to remove\n")

    sys.exit(0)
