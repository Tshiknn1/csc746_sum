#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>

#include "sums.h"

// do nothing
void 
setup(int64_t N, float A[])
{
   printf(" inside direct_sum problem_setup, N=%ld \n", N);
}

float
sum(int64_t N, float A[])
{
   printf(" inside direct_sum perform_sum, N=%ld \n", N);

   float r = 0.f;

   for (int64_t i = 0; i < N; i++) {
      r += i;
   }

   return r;
}

