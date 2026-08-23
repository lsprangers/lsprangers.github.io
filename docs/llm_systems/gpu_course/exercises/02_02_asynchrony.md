---
layout: technical
title: 2.02 - Asynchrony
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Exercise - Asynchrony
The latest of the updated simulator:
```cpp
void simulate(int height, int width, 
              thrust::device_vector<float> &in, 
              thrust::device_vector<float> &out) 
{
  cuda::std::mdspan temp_in(thrust::raw_pointer_cast(in.data()), height, width);
  thrust::tabulate(
    thrust::device, out.begin(), out.end(), 
    [=] __host__ __device__(int id) { /* ... */ }
  );
}

for (int write_step = 0; write_step < 3; write_step++) 
{
  thrust::copy(d_prev.begin(), d_prev.end(), h_prev.begin());
  dli::store(write_step, height, width, h_prev);

  for (int compute_step = 0; compute_step < 3; compute_step++) {
    simulate(height, width, d_prev, d_next);
    d_prev.swap(d_next);
  }
}
```

The reason this is bad is that `tabulate` doesn't allow the CPU to actually run anything while GPU is doing computations. Ideally we can copy from GPU to CPU, and then as the GPU is running the next simulation the CPU can write the historic results to disk

`cub::DeviceTransform` is almost a stand in replacement for `thrust::tabulate()` - it basically just loops over an iterator performing some computation, but it ensures it's done on GPU

`cub::DeviceTransform::Transform(input_iterator, output_iterator, num_items, op)`

### Exercise Input
```cpp
%%writefile Sources/compute-io-overlap.cu
#include "dli.h"

void simulate(int width,
              int height,
              const thrust::device_vector<float> &in,
                    thrust::device_vector<float> &out)
{
  # create iloc indexer over in data
  cuda::std::mdspan temp_in(thrust::raw_pointer_cast(in.data()), height, width);
  # run tabulate with lambda 
  thrust::tabulate(out.begin(), out.end(), [=] __device__(int id) {
    return dli::compute(id, temp_in);
  });
}

int main()
{
  int height = 2048;
  int width  = 8192;

  thrust::device_vector<float> d_prev = dli::init(height, width);
  thrust::device_vector<float> d_next(height * width);
  thrust::host_vector<float> h_prev(height * width);

  const int compute_steps = 500;
  const int write_steps = 3;
  for (int write_step = 0; write_step < write_steps; write_step++)
  {
    auto step_begin = std::chrono::high_resolution_clock::now();
    # copy from GPU to CPU
    thrust::copy(d_prev.begin(), d_prev.end(), h_prev.begin());

    for (int compute_step = 0; compute_step < compute_steps; compute_step++)
    {
      # run next GPU computation
      simulate(width, height, d_prev, d_next);
      # move pervious to next
      d_prev.swap(d_next);
    }

    # after simulations, track timing
    auto write_begin = std::chrono::high_resolution_clock::now();
    dli::store(write_step, height, width, h_prev);
    auto write_end = std::chrono::high_resolution_clock::now();
    auto write_seconds = std::chrono::duration<double>(write_end - write_begin).count();

    auto step_end = std::chrono::high_resolution_clock::now();
    auto step_seconds = std::chrono::duration<double>(step_end - step_begin).count();
    std::printf("compute + write %d in %g s\n", write_step, step_seconds);
    std::printf("          write %d in %g s\n", write_step, write_seconds);
  }
}
```

### Exercise Solution
The main point is just a 1:1 replacement of `tabulate` with `Transform`, and then using `cudaDeviceSynchronize` to ensure the timings are equal. That being said, if the `compute_step` is running each GPU simulation, and `simulate()` runs `Transform`, is there a way to send the entirety of the `compute_step` for loop to the GPU to run? The `d_prev` and `d_next` vectors are GPU vectors, so they should be able to be copied to each other respectively, and it's a sequential operation as `d_next` needs to be copied to `d_prev` so it can't be done in parallel

Ideally, the entirety of the simulation is handed off to the GPU while the CPU can do whatever it wants to

```cpp
%%writefile Sources/compute-io-overlap.cu
#include "dli.h"

void simulate(int width,
              int height,
              const thrust::device_vector<float> &in,
                    thrust::device_vector<float> &out)
{
  # create iloc indexer over in data
  cuda::std::mdspan temp_in(thrust::raw_pointer_cast(in.data()), height, width);
  # run cub transform with lambda 
  cub::DeviceTransform::Transform(in.begin(), out.begin(), height * width, [=] __device__(int id) {
    return dli::compute(id, temp_in);
  });
}

int main()
{
  int height = 2048;
  int width  = 8192;

  thrust::device_vector<float> d_prev = dli::init(height, width);
  thrust::device_vector<float> d_next(height * width);
  thrust::host_vector<float> h_prev(height * width);

  const int compute_steps = 500;
  const int write_steps = 3;
  for (int write_step = 0; write_step < write_steps; write_step++)
  {
    auto step_begin = std::chrono::high_resolution_clock::now();
    # copy from GPU to CPU
    thrust::copy(d_prev.begin(), d_prev.end(), h_prev.begin());

    for (int compute_step = 0; compute_step < compute_steps; compute_step++)
    {
      # run next GPU computation
      simulate(width, height, d_prev, d_next);
      # at this point CPU is free to do whatever
      # move pervious to next
      d_prev.swap(d_next);
    }

    # after simulations, track timing
    auto write_begin = std::chrono::high_resolution_clock::now();
    dli::store(write_step, height, width, h_prev);
    cudaDeviceSynchronize();
    auto write_end = std::chrono::high_resolution_clock::now();
    auto write_seconds = std::chrono::duration<double>(write_end - write_begin).count();

    auto step_end = std::chrono::high_resolution_clock::now();
    auto step_seconds = std::chrono::duration<double>(step_end - step_begin).count();
    std::printf("compute + write %d in %g s\n", write_step, step_seconds);
    std::printf("          write %d in %g s\n", write_step, write_seconds);
  }
}
```


### Notes
Why not just do something to reach:
```
CPU
 |
 +-- submit entire computation
 |
 +------------------------------------+
                                      |
                                    GPU
                                      |
                              iteration 1
                                   ↓
                              iteration 2
                                   ↓
                              iteration 3
                                   ↓
                                  ...
                                   ↓
                              iteration 500
```

Launching each kernel function from the CPU seems like a bit of a waste

```cpp
__global__ void simulate_all(...) {

    for (int step = 0; step < 500; step++) {

        compute(...);

        swap(prev, next);
    }
}
```

It doesn't work as easily because of some synchronization stuff that'd need to happen. If `compute()` runs millions of parallel operations with tabulate / transform / whatever, it needs to ensure `swap()` happens. There's a decent amoount of device level `__syncthreads()` mechanisms, but they all deal with different levels of synchronization - threads, thread blocks, clusters, etc. In this scenario you need the entirety of all GPU threads to be finished with the calculation before you do a `swap()`, and because of that it's forced into multiple kernel launches from the CPU. There's no way to synchronize across all blocks in a normal kernel (easily)

`vector.swap(other_vector)` doesn't actually swap the memory, it just changes the iterators each points to!