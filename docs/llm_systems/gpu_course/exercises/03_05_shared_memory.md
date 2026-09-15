---
layout: technical
title: 3.05 - Shared Memory
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Shared Memory
Looking at [atomics](/docs/llm_systems/gpu_course/exercises/03_03_atomics.md), [thread synchronization](/docs/llm_systems/gpu_course/exercises/03_04_synchronization.md), and thread hierarchies, it makes sense why we need all of thees controls in place. One natural question is *"why do we need this hierarchy in the first place?"*

A natural answer to this is just easy human intuition, but realistically the hierarchy is tied to memory management. Understanding which threads have access to what memory, and [how threads work with process memory](/docs/dsa/concurrency/index.md) makes all of this a bit clearer. Threads share process memory space, and each thread spawned by a process has the same general heap and stack memory allocated to it on the CPU, but how does this work on GPU?

GPU's are composed of uniform memory blocks called **streaming multiprocessors (SM)**. Each SM has many cores, and local L1 cache. *Global GPU Memory* lives outside of these streaming multiprocessors (i.e. global)

![GPU Streaming Multiprocessor Caching](/img/gpu_streaming_multiprocessor_memory_cache.png)

Thread blocks are tied to these streaming multiprocessors, and so we can utilize **shared memory**, which is co-located to L1 cache on a streaming multiprocessor. *Shared memory is directly accessible and usable by threads within thread blocks*, and ensures we don't have queue of operations on L2 shared memory that we don't need

![Thread Block on SM](/img/thread_block_on_sm.png)

![L1 GPU Shared Memory](/img/l1_shared_memory_gpu.png)

To allocate shared memory, we just use `__shared__` with variable declaration!

```cpp
#include "dli.cuh"

constexpr int num_bins = 10;
constexpr float bin_width = 10;

__global__ void histogram_kernel(cuda::std::span<float> temperatures,
                                 cuda::std::span<int> histogram) {
  __shared__ int block_histogram[10];

  if (threadIdx.x < 10) {
    block_histogram[threadIdx.x] = 0;
  }

  // why here?
  __syncthreads();

  int cell = blockIdx.x * blockDim.x + threadIdx.x;
  int bin = static_cast<int>(temperatures[cell] / 10);

  // get an atomic reference to l1 shared memory in thread block
  cuda::atomic_ref<int, cuda::thread_scope_block> block_ref(
      block_histogram[bin]);
  
  // add 1 to it
  block_ref.fetch_add(1);

  // ensure all threads have reached here in thread block
  __syncthreads();

  // add the resulting local to global (device) data structure
  if (threadIdx.x < 10) {
    cuda::atomic_ref<int, cuda::thread_scope_device> ref(
        histogram[threadIdx.x]);
    ref.fetch_add(block_histogram[threadIdx.x]);
  }
}

void histogram(cuda::std::span<float> temperatures,
               cuda::std::span<int> block_histograms,
               cuda::std::span<int> histogram, cudaStream_t stream) {
  int block_size = 256;
  int grid_size = cuda::ceil_div(temperatures.size(), block_size);
  histogram_kernel<<<grid_size, block_size, 0, stream>>>(temperatures,
                                                         histogram);
}
```