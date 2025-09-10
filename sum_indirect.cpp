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
   // fill A with 0...N-1
   for (int64_t i = 0; i < N; i++) {
      do {
         A[i] = lrand48() % N;
      } while ((int64_t) A[i] == i || (int64_t) A[i] == N);
   }
}

float
sum(int64_t N, float A[])
{
   // printf(" inside sum_indirect perform_sum, N=%ld \n", N);

   float sum = 0.f;
   float latest = 0.f;

   // jump to index pointed to by the most recently accessed value in A
   // do this for all values in A
   for (int i = 1; i < N; i++) {
      latest = A[(int64_t) latest];
      sum += latest;
   }

   return sum;
}
