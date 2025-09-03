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
   // get system time and use it to override seed for RNG
   struct timespec ts;
   clock_gettime(CLOCK_REALTIME, &ts);

   unsigned short seed[3];
   seed[0] = ts.tv_sec & 0xffff;
   seed[1] = (ts.tv_nsec << 16) & 0xffff;
   seed[2] = ts.tv_nsec & 0xffff;
   
   seed48(seed);

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
   float latest = A[0];

   // jump to index pointed to by the most recently accessed value in A
   // do this for all values in A
   for (int i = 1; i < N; i++) {
      sum += latest;
      latest = A[(int64_t) latest];
   }

   return sum;
}
