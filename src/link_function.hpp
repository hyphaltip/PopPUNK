// dlib headers
#include <dlib/matrix.h>
typedef dlib::matrix<double,0,1> column_vector;

class LinearLink
{
   public:
      // Initialisation
      LinearLink(const column_vector& predictors, const column_vector& responses)
         : _predictors(predictors), _responses(responses)
      {
      }

      // Likelihood and first derivative
      double likelihood(const column_vector& b)
         const;
      column_vector gradient(const column_vector& b)
         const;

   protected:
      column_vector _predictors;
      column_vector _responses;
};

double (LinearLink::*likptr)(const column_vector&) const = &LinearLink::likelihood;