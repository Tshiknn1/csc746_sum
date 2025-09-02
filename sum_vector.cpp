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
   printf(" inside sum_vector problem_setup, N=%ld \n", N);

   // fill A with 0...N-1
   for (int64_t i = 0; i < N; i++) {
      A[i] = i;
   }
}

float
sum(int64_t N, float A[])
{
   printf(" inside sum_vector perform_sum, N=%ld \n", N);

   float sum = 0.f;

   for (int64_t i = 0; i < N; i++) {
      sum += A[i];
   }

   return sum;
}

