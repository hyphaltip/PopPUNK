Installation
============

The easiest way to install is through conda, which will also install the
dependencies::

    conda install poppunk

Then run with ``poppunk``.

.. important::
    PopPUNK requires python3 to run (which on many default Linux installations is
    run using ``python3`` rather than ``python``).

Installing with conda (recommended)
-----------------------------------
If you do not have ``conda`` you can install it through
`miniconda <https://conda.io/miniconda.html>`_ and then add the necessary
channels::

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

Then run::

    conda install poppunk

Installing with pip
-------------------
If you do not have conda, you can also install through pip::

    python3 -m pip install poppunk

You will also need `mash <http://mash.readthedocs.io/en/latest/>`__ (v2 or higher)
installed (see :ref:`dependencies`).

Clone the code
--------------
You can also clone the github to run the latest version, which is executed by::

    git clone https://github.com/johnlees/PopPUNK.git && cd PopPUNK
    python3 poppunk-runner.py

This will also give access to the :ref:`scripts`.

You will need to install the :ref:`dependencies` yourself (you can still use
conda or pip for this purpose).

.. _dependencies:

Dependencies
------------
We tested PopPUNK with the following packages:

* python3 (3.6.3)
* ``DendroPy`` (4.3.0)
* ``hdbscan`` (0.8.13)
* ``matplotlib`` (2.1.2)
* ``networkx`` (2.1)
* ``numpy`` (1.14.1)
* ``numba`` (0.36.2)
* ``pandas`` (0.22.0)
* ``scikit-learn`` (0.19.1)
* ``scipy`` (1.0.0)
* ``sharedmem`` (0.3.5)

``numba`` may need ``gcc >=v4.8`` to install correctly through pip (if you are
getting ``OSError`` or ``'GLIBCXX_3.4.17' not found``).

You will need a `mash <http://mash.readthedocs.io/en/latest/>`__ installation
which is v2.0 or higher

Optionally, you can use `rapidnj <http://birc.au.dk/software/rapidnj/>`__
if producing output with ``--microreact`` and ``--rapidnj`` options. We used
v2.3.2.

