---
layout: technical
title: 3.04 - Synchronization
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Synchronization
Atomics let us regain functional correctness, but enforces serialization across threads accessing memory - each thread needs to wait its turn to access the variable, and each sit in a queue to eventually access it

Serialization should be avoided at all costs, if we have a block size of $256$ and a grid size of $16,384$ with everything mapping into one atomic variable to update, we'd have $4,194,304$ atomic serial operations sitting in a queue

To bypass this, we can implement **privatization** which is the idea of storing local versions of global data structures so that threads, blocks, or grids have access to their own subspace. At the end all of these subspaces can get merged together to create the global representation

To do this the problem needs to be divisible and aggregable, meaning counts, sums, etc can be done on a local portion and aggregated together to produce a correct global result

To ensure all local private threads are completed, we need to ensure all threads are synced - `_syncthreads()` helps to perform this, and all threads need to run this command in the same control path section to ensure they're synced back to the "main" path. Each thread must reach `_syncthreads()` function in their own control path before any thread is permitted to proceed to the next part of the code. Each thread is apart of a **thread scope** which define the set of threads that can synchronize using a given atomic - *thread scope can be system, device, or block*

```cpp
#include "dli.cuh"

constexpr float bin_width = 10;

// 1. Use `__syncthreads()` to synchronize threads within a block and avoid data race
__global__ void histogram_kernel(
  cuda::std::span<float> temperatures, 
  cuda::std::span<int> block_histograms, 
  cuda::std::span<int> histogram) 
{
  cuda::std::span<int> block_histogram = 
    block_histograms.subspan(blockIdx.x * histogram.size(), 
                             histogram.size());

  int cell = blockIdx.x * blockDim.x + threadIdx.x;
  int bin = static_cast<int>(temperatures[cell] / bin_width);

  cuda::std::atomic_ref<int> block_ref(block_histogram[bin]);
  block_ref.fetch_add(1);

  // entirety of exercise - add this in to ensure all threads reach 
  //  here before anything can continue and add themnselves to the global 
  //  histogram
  __syncthreads();

  if (threadIdx.x < histogram.size()) {
    // 2. Reduce scope of atomic operation using `cuda::atomic_ref`
    cuda::std::atomic_ref<int> ref(histogram[threadIdx.x]);
    ref.fetch_add(block_histogram[threadIdx.x]);
  }
}


void histogram(
  cuda::std::span<float> temperatures, 
  cuda::std::span<int> block_histograms, 
  cuda::std::span<int> histogram,
  cudaStream_t stream) 
{
  int block_size = 256;
  int grid_size = cuda::ceil_div(temperatures.size(), block_size);
  histogram_kernel<<<grid_size, block_size, 0, stream>>>(
    temperatures, block_histograms, histogram);
}
```