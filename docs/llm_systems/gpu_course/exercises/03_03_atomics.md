---
layout: technical
title: 3.03 - Atomics
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Atomics
Atomics are ways to ensure thread safe access to variables and memory locations. C++ has standards for atomics, and CUDA also provides it's own set of atomic utilities for use across kernels

![GPU Thread Race Condition](/img/gpu_thread_race_condition.png)

![GPU Thread Atomics](/img/gpu_thread_atomics.png)

Atomics are especially needed in GPU programs where a shared data structure like an array or memory address are utilized across threads in a kernel

## Exercise
```cpp
__global__ void kernel(int *count)
{
  // Wrap data in atomic_ref
  cuda::std::atomic_ref<int> ref(count[0]);

  // Atomically increment the underlying value
  ref.fetch_add(1);
}
```

```cpp
#include "dli.cuh"

constexpr float bin_width = 10;

__global__ void histogram_kernel(cuda::std::span<float> temperatures, 
                                 cuda::std::span<int> histogram)
{
  int cell = blockIdx.x * blockDim.x + threadIdx.x;
  if (cell < temperatures.size()) {
    int bin = static_cast<int>(temperatures[cell] / bin_width);

    // fix data race in incrementing histogram bins by using `cuda::std::atomic_ref`
    // int old_count = histogram[bin];
    // int new_count = old_count + 1;
    // histogram[bin] = new_count;
    cuda::std::atomic_ref<int> ref(histogram[bin]);
    ref.fetch_add(1);
  }
}

void histogram(cuda::std::span<float> temperatures, 
               cuda::std::span<int> histogram,
               cudaStream_t stream)
{
  int block_size = 256;
  int grid_size = cuda::ceil_div(temperatures.size(), block_size);
  histogram_kernel<<<grid_size, block_size, 0, stream>>>(
    temperatures, histogram);
}
```