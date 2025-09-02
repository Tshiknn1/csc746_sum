#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>
#include <time.h>

#include "sums.h"

void 
setup(int64_t N, float A[])
{
   printf(" inside sum_indirect problem_setup, N=%ld \n", N);

   // fill A with 0...N-1
   for (int64_t i = 0; i < N; i++) {
      A[i] = i;

      // at large problem sizes, we sometimes round up to N;
      // this will be a problem for perform_sum, so let's bring it down
      int64_t insert_val = i;
      while ((int64_t) A[i] == N) {
         insert_val--;
         A[i] = insert_val;
      }
   }

   // get system time and use it to override seed for RNG
   struct timespec ts;
   clock_gettime(CLOCK_REALTIME, &ts);

   unsigned short seed[3];
   seed[0] = ts.tv_sec & 0xffff;
   seed[1] = (ts.tv_nsec << 16) & 0xffff;
   seed[2] = ts.tv_nsec & 0xffff;
   
   seed48(seed);

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
      idx = (int64_t) A[idx];

      // if (idx > N) {
      //    printf("[WARNING] sum_indirect went out of bounds");
      //    return 0.f;
      // }

      sum += A[idx];
   }

   return sum;
}

