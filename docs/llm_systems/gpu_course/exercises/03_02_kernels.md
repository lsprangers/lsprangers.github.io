---
layout: technical
title: 3.02 - Kernels
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Kernels
Sometimes standard libraries aren't enough to fulfill all the needs of an algorithm, and in that scenario we have to write our own **kernel**. Host CUDA code is compiled down to CPU instructions, and ran on the CPU; Device CUDA code is compiled down to GPU instructions, and ran on the GPU. However, `__global__` functions are compiled down to GPU instructions, ran on the GPU, but called from the CPU - these are **CUDA Kernels** and they can be called with the triple chevron `<<<kernel>>>` notation

These are asynchronous meaning the CPU doesn't wait for these to complete on the GPU

```cpp
__global__
void single_thread_kernel(dli::temperature_grid_f in, float *out)
{
    for (int id = 0; id < in.size(); id++)
    {
        out[id] = dli::compute(id, in);
    }
}
```

Out of the box the above code would still run sequentially. Meaning it will run one single thread that runs `dli::compute` over every single cell of the grid

CUDA Kernels are inherently able to be parallelized using **threads + thread indexes**. The below code shows how you can use threads and thread indexes to calculate things in parallel. Each thread needs to own a slice of the cells to calculate, and `threadIdx` is a built in variable available in any CUDA Kernel

The first thread works on `threadIdx = 0`, and then would jump to `id = 0 + 2`

![GPU Kernel Thread Idx](/img/gpu_thread_warp_branch.png)

```cpp
const int number_of_threads = 2

__global__
void block_kernel(dli::temperature_grid_fn in, float *out)
{
    int thread_index = threadIdx.x;
    for (int id = thread_index; id < in.size(); id += number_of_threads)
    {
        out[id] = dli::compute(id, in);
    }
}


void simulate(dli::temperature_grid_f in, float *out, cudaStream_t stream)
{
    block_kernel<<<1, number_of_threads, 0 stream>>>(in, out);
}
```

### Thread Blocks
We can keep bumping up the `number_of_threads` argument above, and as long as it's less than the total number of cells in our image it'll keep working and getting faster. However, there's a hard limit of $1,024$ threads that can be launches in a **thread block** at any time. Every thread we launch is apart of a thread block

`kernel<<<NUMBER-OF-BLOCKS, NUMBER-OF-THREADS, 0, stream>>>`

Threads are grouped into blocks, all blocks are the same size, and a collection of blocks is known as a **grid**
- `threadIdx.x` stores the index of the thread within the block
- `blockIdx.x` stores index of block within grid
- `blockDim.x` stores the number of threads in a thread block
- `gridDim.x` stores the number of blocks in the grid

![Thread Block and Grid](/img/cuda_thread_block_and_grid.png)

So in the above simulation, we need to split up the image across thread blocks, and process part of the image within different blocks (since our image is $\gt 1,024$)

`int thread_index = blockDim.x * blockIdx.x + threadIdx.x` would then give us a unique index to a thread across all blocks in a grid

There are some best practices with setting sizes, and they mostly deal with the SIMT levels that GPU's can use - i.e. using a multiple of 32 (warp size) for block sizes ensures that blocks can be scheduled simultaneously and never overlap across SIMT boundaries, but profiling is always needed to check throughput and synchronicity

Given a problem size $N$ and thread block size, we can compute the number of blocks we need in a grid as: 
- For a problem of size $N$, if block size is `threads_per_block` threads, you can compute the number of blocks as:
```
int threads_per_block = 256;
int num_blocks = cuda::ceil_div(N, threads_per_block)
```

This ensures you launch enough threads to cover all $N$ elements in the problem

## Exercises
```cpp
#include "dli.cuh"

// 1. convert the function below from a CPU function into a CUDA kernel - just mark with __global__
__global__
void symmetry_check_kernel(dli::temperature_grid_f temp, int row)
{
  int column = 0;

  // compare the row with the mirror row, extent gives nRows basically
  if (abs(temp(row, column) - temp(temp.extent(0) - 1 - row, column)) > 0.1)
  {
    printf("Error: asymmetry in %d / %d\n", column, temp.extent(1));
  }
}

void symmetry_check(dli::temperature_grid_f temp, cudaStream_t stream)
{
  int blocks_in_grid = 1;
  int threads_in_block = 1;
  int target_row = 0;
  // 2. use triple chevron to launch the kernel
  symmetry_check_kernel<<<blocks_in_grid, threads_in_block, 0, stream>>>(temp, target_row);
}
```


```cpp
__global__ void symmetry_check_kernel(dli::temperature_grid_f temp, int row)
{
  // if we're in 0th block of 1024 threads, this gives us the column to check
  //    and the last result would be 1023
  // and if we're in 1st block, the 0th index would give 1024
  int column = blockIdx.x * blockDim.x + threadIdx.x;

  // we always pass in 0 as row so I don't fully get how this is 
  //    comparing mirror images. If we're at row 0 col 0 (top left)
  //    we'd expect the mirror of this to be the last row but still 
  //    column 0. In this setup we'd have temp.extent = nRows - 1 - 0
  //    and column could be as high as 1024, and surely there's no column 
  //    of that index if we're at the last row...idk
  if (abs(temp(row, column) - temp(temp.extent(0) - 1 - row, column)) > 0.1)
  {
    printf("Error: asymmetry in %d / %d\n", column, temp.extent(1));
  }
}

void symmetry_check(dli::temperature_grid_f temp, cudaStream_t stream)
{
  // if there are 1,025 cells, we would launch 2 grids (ceil gives 2 instead of floor gives 1)
  int width      = temp.extent(1);
  int block_size = 1024;
  int grid_size  = cuda::ceil_div(width, block_size);

  int target_row = 0;
  // launch symmetry check with this
  symmetry_check_kernel<<<grid_size, block_size, 0, stream>>>(temp, target_row);
}
```