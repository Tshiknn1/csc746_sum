#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>

#include "sums.h"

void 
setup(int64_t N, float A[])
{
   printf(" inside sum_indirect problem_setup, N=%ld \n", N);

   // fill A with 0...N-1
   for (int64_t i = 0; i < N; i++) {
      A[i] = i;
   }

   // swap each item with a random index
   float tmp;
   int64_t randidx;
   for (int64_t i = 0; i < N; i++) {
      randidx = lrand48() % N;
      tmp = A[randidx];
      A[randidx] = A[i];
      A[i] = tmp;
   }
}

float
sum(int64_t N, float A[])
{
   printf(" inside sum_indirect perform_sum, N=%ld \n", N);

   float sum = 0.f;

   // jump to index pointed to by the most recently accessed value in A
   // do this for all values in A
   int64_t idx = 0;
   for (int i = 0; i < N; i++) {
      idx = std::round(A[idx]);  // anticipate rounding errors

      if (idx > N) {
         printf("[WARNING] sum_indirect went out of bounds");
         return 0.f;
      }

      sum += A[idx];
   }

   return sum;
}

