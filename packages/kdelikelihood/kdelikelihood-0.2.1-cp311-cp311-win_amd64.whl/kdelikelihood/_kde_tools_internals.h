#include <unordered_map>
#include <vector>
#include <math.h>
#include <iostream>

inline float log_df(float arg)
{
   return logf(arg);
}

inline double log_df(double arg)
{
   return log(arg);
}

inline float log1p_df(float arg)
{
   return log1pf(arg);
}

inline double log1p_df(double arg)
{
   return log1p(arg);
}

inline float exp_df(float arg)
{
   return expf(arg);
}

inline double exp_df(double arg)
{
   return exp(arg);
}

struct NoHasher
{
   std::size_t operator()(const std::size_t &value) const
   {
      return value;
   }
};

typedef uint_fast32_t index_t;
typedef std::vector<index_t> grid_vertex_type;
typedef std::unordered_map<std::size_t, std::vector<index_t>, NoHasher> map_t;

template <typename T>
T square(T input)
{
   return input * input;
}

template <typename T>
short sign(T input)
{
   if (input > 0)
      return 1;
   else if (input < 0)
      return -1;
   else
      return 0;
}

template <typename T>
class ElementaryLikelihoodComputerBackend
{

public:
   ElementaryLikelihoodComputerBackend(){}; // Default constructor for placeholders only. Do not use!
   ElementaryLikelihoodComputerBackend(T **observations_, int *consideredColumns_, int dim_, 
                                       long lenObservations_, T guaranteedLookupDistance_,
                                       int *domains_, T *inverseBandwidth_,
                                       T logNormalization_) : dim(dim_),
                                                              observations(observations_),
                                                              consideredColumns(consideredColumns_),
                                                              lenObservations(lenObservations_),
                                                              guaranteedLookupDistance(guaranteedLookupDistance_),
                                                              cellWidth(guaranteedLookupDistance_ * 2),
                                                              halfGuaranteedLookupDistance(guaranteedLookupDistance_ / 2),
                                                              squareDistanceBound(square(guaranteedLookupDistance_)),
                                                              domains(domains_),
                                                              inverseBandwidth(inverseBandwidth_),
                                                              logNormalization(logNormalization_)
   {
      init_log1pexp_cache();
      reflect.resize(dim);

      for (int i = 0; i < dim; i++)
      {
         reflect[i] = (bool)domains[consideredColumns[i]];
      }

      fill_hashmap();
   }

   void compute_log_likelihood(T **sample, long lenSample, T *out)
   {

      std::vector<index_t> *observationIndices;
      auto logPMax = std::vector<T>(lenObservations, -INFINITY);
      T newLogPValue;

      // Search for the respective closest sample point to
      // each observation. We do not need to do a perfect search,
      // hitting the right order of magnitude is just fine.
      // Hence, we consider only the first portion of the sampling
      // points and correct this later if this was insufficient.
      index_t searchSize = lenSample / 10;
      if (searchSize < 50)
      {
         searchSize = 50;
         if (searchSize > lenSample)
         {
            searchSize = lenSample;
         }
      }

      for (index_t i = 0; i < searchSize; i++)
      {
         auto &thisSample = sample[i];
         auto indexSearch = hashMap.find(get_grid_vertex_hash(thisSample));

         if (indexSearch != hashMap.end())
         {
            for (auto &j : indexSearch->second)
            {
               newLogPValue = compute_log_likelihood_element(observations[j], thisSample);
               if (logPMax[j] < newLogPValue)
                  logPMax[j] = newLogPValue;
            }
         }
      }

      auto newLogPMax = logPMax;
      auto resultTmp = std::vector<T>(lenObservations, 0);

      for (int repetition = 0; repetition < 2; repetition++)
      {
         T maxLogPMaxError = 0;
         bool repeat = false;
         for (index_t i = 0; i < lenSample; i++)
         {
            auto &thisSample = sample[i];
            auto indexSearch = hashMap.find(get_grid_vertex_hash(thisSample));

            if (indexSearch != hashMap.end())
            {
               for (auto &j : indexSearch->second)
               {
                  newLogPValue = compute_log_likelihood_element(observations[j], thisSample);

                  if (!repeat)
                  {
                     resultTmp[j] += exp_df(newLogPValue - logPMax[j]);
                  }

                  if (newLogPMax[j] < newLogPValue)
                  {
                     newLogPMax[j] = newLogPValue;
                     auto error = newLogPValue - logPMax[j];
                     if (error > maxLogPMaxError)
                     {
                        maxLogPMaxError = error;
                        repeat = maxLogPMaxError > 100;
                     }
                  }
               }
            }
         }

         if (repeat)
         {
            logPMax = newLogPMax;
            std::fill(resultTmp.begin(), resultTmp.end(), 0.);
         }
         else
         {
            break;
         }
      }

      T logLenSample = log_df(T(lenSample));
      for (index_t i = 0; i < lenObservations; i++)
      {
         out[i] = (logPMax[i] + log_df(resultTmp[i]) - logLenSample);
      }
   }

protected:
   int dim;              // Dimension of the considered data space.
   long lenObservations; // Number of considered observatons
   map_t hashMap;        // Set of grid cells and corresponding observations. 

   std::vector<T> log1pexp_cache; // cache fr faster computation of the log1pexp function
   T **observations;          // Observations for which the likelihood should be computed
   int *consideredColumns;    // Indices of the columns of the observations that should be considered
   int *domains;              // Domains of the Observations by column (0: R, 1: R+, 2: N)
   std::vector<bool> reflect; // Whether the kernel for the columns should use reflecting boundary conditions

   T *inverseBandwidth;             // Inverse of the bandwidth by column
   T guaranteedLookupDistance;      // Minimal radius within which all neighbours are considered to compute the likelihood
   T logNormalization;              // Log of the normalization constants by column
   T cellWidth;                     // Width of a cell for internal data storage. Is 2*guaranteedLookupDistance
   T halfGuaranteedLookupDistance;  // 0.5 * guaranteedLookupDistance

   // Square of the maximal considered distance between two data points. I.e.,
   // square cell width.
   T squareDistanceBound;

   static const inline T MIN_log1pexp = -10;
   static const inline T RESOLUTION_log1pexp = -1e-3; // -1e-5;

   /*
    * References: https://jimmy-shen.medium.com/stl-map-unordered-map-with-a-vector-for-the-key-f30e5f670bae
    *	            https://stackoverflow.com/questions/20511347/a-good-hash-function-for-a-vector
    * Should use the same method as boost to generate a hash
    */
   std::size_t get_grid_vertex_hash(const grid_vertex_type &vec)
   {
      std::size_t hash = vec.size();
      for (auto &i : vec)
      {
         hash ^= i + 0x9e3779b9 + (hash << 6) + (hash >> 2);
      }
      return hash;
   }

   std::size_t get_grid_vertex_hash(T *observations)
   {
      std::size_t hash = dim;

      for (int i = 0; i < dim; i++)
      {
         auto index = index_t(observations[consideredColumns[i]] / cellWidth);
         hash ^= index + 0x9e3779b9 + (hash << 6) + (hash >> 2);
      }

      return hash;
   };

   grid_vertex_type get_grid_vertex(T *observations)
   {
      auto result = grid_vertex_type(dim);
      for (int i = 0; i < dim; i++)
      {
         result[i] = index_t(observations[consideredColumns[i]] / cellWidth);
      }

      return result;
   }

   void fill_hashmap()
   {

      for (index_t i = 0; i < lenObservations; i++)
      {
         auto gridVertex = get_grid_vertex(observations[i]);

         // The sign of distancesToCenter indicates if the point is closer to the
         // lower or upper end of the cell in a dimension. The value is the
         // distance to the cell center.
         std::vector<T> distancesToCenter = std::vector<T>(dim);
         for (int j = 0; j < dim; j++)
         {
            distancesToCenter[j] = observations[i][consideredColumns[j]] - gridVertex[j] * cellWidth - guaranteedLookupDistance;
         }

         fill_in_neighbours(i, gridVertex, distancesToCenter, 0, 0.);
      }
   }

   /*
    * Adds an observation to all adjacent grid cells
    *
    * This funciton works recursively.
    *
    * Parameters
    * ----------
    * row:
    *    Index of the observation being considered.
    * gridVertex:
    *    Key of the vertex in the grid where the considered observation is located.
    * distancesToCenter:
    *    Distance between the cell's mid point and the observation.
    * index:
    *    Current index under consideration. Is incremented in every recursion level.
    * squareDistance:
    *    Lower bound for the squared distance of the considered point to the considered
    *    neighbouring cells computed based on the dimensions already processed.
    */
   void fill_in_neighbours(index_t row, grid_vertex_type &gridVertex, std::vector<T> &distancesToCenter,
                           int index, T squareDistance)
   {

      // recursion end
      if (index >= dim)
      {
         hashMap[get_grid_vertex_hash(gridVertex)].push_back(row);
         return;
      }

      // one option is not to change the current dimension
      fill_in_neighbours(row, gridVertex, distancesToCenter,
                         index + 1, squareDistance);

      auto distanceToThisCenter = distancesToCenter[index];
      if (distanceToThisCenter)
      {
         // check if we are still within the admissible radius
         auto direction = sign(distanceToThisCenter);

         // Note: halfCellWidth == guaranteedLookupDistance
         auto newSquareDistance = squareDistance + square(direction * guaranteedLookupDistance - distanceToThisCenter);

         if ((newSquareDistance <= squareDistanceBound) &&
             (direction > 0 || gridVertex[index] || !reflect[index]))
         {

            // change
            gridVertex[index] += direction;

            // the other option to consider the left or right neighbor
            fill_in_neighbours(row, gridVertex, distancesToCenter,
                               index + 1, newSquareDistance);

            // undo the change
            gridVertex[index] -= direction;
         }
      }
   }

   void init_log1pexp_cache()
   {
      std::size_t cache_size = std::size_t(std::ceil(MIN_log1pexp / RESOLUTION_log1pexp));
      cache_size += 1;
      log1pexp_cache.resize(cache_size);
      for (size_t i = 0; i < cache_size; i++)
      {
         log1pexp_cache[i] = log1p_df(exp_df(RESOLUTION_log1pexp * i));
      }
   }

   T log1pexp(T x)
   {
      if (x <= MIN_log1pexp)
      {
         return exp_df(x);
      }
      else
      {
         auto a = x / RESOLUTION_log1pexp;
         size_t i = size_t(a);
         a -= i;
         return (1 - a) * log1pexp_cache[i] + a * log1pexp_cache[i + 1];
      }
   }


   T compute_log_likelihood_element(T *observation, T *sample)
   {

      T result = -logNormalization;
      for (int i = 0; i < dim; i++)
      {
         auto j = consideredColumns[i];
         result -= square(observation[j] - sample[j]) * 0.5;
         if (domains[j] && observation[j] <= halfGuaranteedLookupDistance)
         {
            if (domains[j] == 1)
               result += log1pexp((-2) * observation[j] * sample[j]);
            else
               result += log1pexp((-2) * observation[j] * sample[j] - (observation[j] + sample[j] + 0.5 * inverseBandwidth[j]) * inverseBandwidth[j]);
         }
      }

      return result;
   }
};
