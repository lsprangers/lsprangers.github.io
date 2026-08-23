---
layout: technical
title: 1.06 - Memory Spaces
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Exercise - Memory Spaces
A universal vector in `thrust` essentially keeps two copies of the same data, both on CPU and GPU. Managed memory abstracts away the fact that GPU and CPU have distinct memory spaces, and so imlpicit memory transfer between memory spaces happens upon accessing that memory in kernel code

![CUDA Exercise 1_06 Memory Spaces](/img/cuda_1_06_memory_spaces.png)

When the host calls `store` on CPU, and data is sitting on device memory, CUDA needs to move the data from device to host memory. Once `store` finishes, the GPU needs to run the next transformation, which means CUDA needs to copy the CPU data back onto the device

Essentially there's a continuous flip flop between CPU and GPU having the "valid" data, and it keeps having to copy the entire thing back and forth

Both vectors below are only accessible on the specific device it's constructed on:
- `thrust::host_vector` constructs and hosts the vector on CPU memory
- `thrust::device_vector` constructs the vector on CPU, but allocates the vector on GPU memory
- `thrust::copy` can transfer between device and host as needed

The flip flop can be seen in the computation metrics below for the following input code:
```
computed step 0 in 0.0265328 s
computed step 1 in 0.000513304 s
computed step 2 in 0.000507332 s
   write step 1
computed step 0 in 0.0265666 s
computed step 1 in 0.000512392 s
computed step 2 in 0.000514396 s
   write step 2
computed step 0 in 0.0277668 s
computed step 1 in 0.000512602 s
computed step 2 in 0.000507442 s
```

`dli::store` and `dli::simulate` keep copying data back and forth between CPU and GPU, which invalidates it on the other piece of hardware. That's why the first simulation on each step is so much longer than the rest

```cpp
%%writefile Sources/heat-2D.cu
#include "dli.h"

int main()
{
  int height = 4096;
  int width  = 4096;

  thrust::universal_vector<float> prev = dli::init(height, width);
  thrust::universal_vector<float> next(height * width);

  for (int write_step = 0; write_step < 3; write_step++) {
    std::printf("   write step %d\n", write_step);
    dli::store(write_step, height, width, prev);
    
    for (int compute_step = 0; compute_step < 3; compute_step++) {
      auto begin = std::chrono::high_resolution_clock::now();
      dli::simulate(height, width, prev, next);
      auto end = std::chrono::high_resolution_clock::now();
      auto seconds = std::chrono::duration<double>(end - begin).count();
      std::printf("computed step %d in %g s\n", compute_step, seconds);
      prev.swap(next);
    }
  }
}
```

All of this can be tweaked and managed inside of CUDA via:
```
thrust::host_vector<int> h_vec{ 11, 12 };
thrust::device_vector<int> d_vec{ 21, 22 };
thrust::copy_n(h_vec.begin(), 1, d_vec.begin())
```

![CUDA CPU and GPU Vector Copy](/img/cuda_cpu_gpu_copy.png)

### Exercise Input
```cpp
%%writefile Sources/heat-2D-explicit-memory-spaces.cu
#include "dli.h"

int main()
{
  int height = 4096;
  int width  = 4096;

  thrust::universal_vector<float> prev = dli::init(height, width);
  thrust::universal_vector<float> next(height * width);

  for (int write_step = 0; write_step < 3; write_step++) {
    std::printf("   write step %d\n", write_step);
    dli::store(write_step, height, width, prev);
    
    for (int compute_step = 0; compute_step < 3; compute_step++) {
      auto begin = std::chrono::high_resolution_clock::now();
      dli::simulate(height, width, prev, next);
      auto end = std::chrono::high_resolution_clock::now();
      auto seconds = std::chrono::duration<double>(end - begin).count();
      std::printf("computed step %d in %g s\n", compute_step, seconds);
      prev.swap(next);
    }
  }
}
```

### Solution
Just need to change `prev` and `next` to be device vectors, and write them to a `to_write` host vector that we copy data over to

```cpp
%%writefile Sources/heat-2D-explicit-memory-spaces.cu
#include "dli.h"

int main()
{
  int height = 4096;
  int width  = 4096;

  thrust::device_vector<float> prev = dli::init(height, width);
  thrust::device_vector<float> next(height * width);

  for (int write_step = 0; write_step < 3; write_step++) {
    std::printf("   write step %d\n", write_step);
    thrust::host_vector<float> to_write(height * width);
    thrust::copy(prev.begin(), prev.end(), to_write.begin());

    dli::store(write_step, height, width, to_write);
    
    
    for (int compute_step = 0; compute_step < 3; compute_step++) {
      auto begin = std::chrono::high_resolution_clock::now();
      dli::simulate(height, width, prev, next);
      auto end = std::chrono::high_resolution_clock::now();
      auto seconds = std::chrono::duration<double>(end - begin).count();
      std::printf("computed step %d in %g s\n", compute_step, seconds);
      prev.swap(next);
    }
  }
}
```