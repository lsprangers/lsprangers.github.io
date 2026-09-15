---
layout: technical
title: 3.06 - Cooperative Algorithm
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Cooperative Algorithm
- In a serial program, one thread invokes an algorithm and another thread executes it
- In a cooperative algorithm many threads invoke algorithms and many threads execute algorithms
- In parallel algorithms one thread invokes an algorithm and many threads execute it

![Cooperative Vs Serial Algorithm](/img/cooperative_vs_serial_algorithm.png)

These problems can (usually) be [divided and conquered](/docs/dsa/7.%20divide%20&%20conquer/index.md) which means each thread can simply choose a small part of the input to work on (cooperative), and on it's own little slice of the world it can run serial algorithms

CUDA provides a huge number of these algorithms out of the box, and most of them interface with each other quite well:
- `cuBLASDx`: provides cooperative linear algebra functions inside CUDA kernels
- `cuFFTDx`: provides fast cooperative Fourier Transform inside CUDA kernels
- `CUB`: provides cooperative general-purpose algorithms inside CUDA kernels
- ...

Taking `CUB` as an example, it provides both parallel and cooperative algorithms. It's block level reduction (meaning thread block level reducer) function interface can be summarized below. The nested `TempStorage` type provides a type of temporary storage needed by cooperative algorithms for thread communication, and an instance of this needs to be allocated in shared (L2) memory

```cpp
template <typename T, int BlockDimX>
struct cub::BlockReduce
{
  struct TempStorage { ... };

  __device__ BlockReduce(TempStorage& temp_storage) { ... }

  __device__ T Sum(T input) { return ...; }
}

__shared__ cub::BlockReduce<int, 4>::TempStorage storage;
int block_sum = cub::BlockReduce<int, 4>(storage).Sum(threadIdx.x)
```


## Exercise
```cpp
#include "dli.cuh"

constexpr int block_size = 256; //thread block size
constexpr int items_per_thread = 1; //number of items to compute per thread
constexpr int num_bins = 10; // histogram bins
constexpr float bin_width = 10;

__global__ void histogram_kernel(cuda::std::span<float> temperatures,
                                 cuda::std::span<int> histogram) {
  // shared L1 cache int array
  __shared__ int block_histogram[num_bins];

  // get specific cell to update
  int cell = blockIdx.x * blockDim.x + threadIdx.x;
  int bins[items_per_thread] = {
      static_cast<int>(temperatures[cell] / bin_width)};

  // 
  using histogram_t =
      cub::BlockHistogram<int, block_size, items_per_thread, num_bins,
                          cub::BlockHistogramAlgorithm::BLOCK_HISTO_ATOMIC>;
  __shared__ typename histogram_t::TempStorage temp_storage; //idk wtf this is
  histogram_t(temp_storage).Histogram(bins, block_histogram);

  // ensure all threads have reached here
  __syncthreads();
  if (threadIdx.x < num_bins) {
    cuda::atomic_ref<int, cuda::thread_scope_device> ref(
        histogram[threadIdx.x]);
    ref.fetch_add(block_histogram[threadIdx.x]);
  }
}

void histogram(cuda::std::span<float> temperatures,
               cuda::std::span<int> histogram, cudaStream_t stream) {
  int grid_size = cuda::ceil_div(temperatures.size(), block_size);
  histogram_kernel<<<grid_size, block_size, 0, stream>>>(temperatures,
                                                         histogram);
}
```