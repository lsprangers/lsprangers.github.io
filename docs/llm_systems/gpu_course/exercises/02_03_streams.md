---
layout: technical
title: 2.02 - Streams
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## CUDA Streams
Copying data between host and device can also be made asynchronous via `cudaMemcpyAsync`, which is just another optimization we can do to make the entire simulation more performant - `cudaMemcpyAsync` works on raw bytes and pointers, so we need to specify the entirety of memory we want to copy over, and it's not thread safe. If we start writing new bytes to the source before they're written, we can have an inconsistent write to destination

```cpp
cudaError_t cudaMemcpyAsync(
  void*           dst,  // destination pointer
  const void*     src,  // source pointer
  size_t        count,  // number of bytes to copy
  cudaMemcpyKind kind   // direction of copy
)
```

Just using `CudaMemcpyAsync` isn't enough to give a speedup either since all computations on GPU are also ordered, and this ordering of operations is known as a **Cuda Stream** which are basically in-order work queue of things (commands, functions, etc) to be executed on the GPU. If a stream isn't specified, the default stream is used
![GPU ordered functions](/img/gpu_ordered_functions.png)

CUDA streams allow for multiple computations to run in parallel on a GPU, and allows for stream synchronization (waiting for all or some to complete), a small amount of communication, and allocating work to different streams. All work in a stream is executed synchronously in order
![GPU CUDA Streams](/img/cuda_stream.png)

Currently, the code below is what's used to run async compute on GPU while I/O on CPU. There's a synchronous copy from GPU to CPU memory via `thrust:copy`, where it needs to wait for that copy to finish before proceeding with next computation

```cpp
void simulate(int width, int height, const thrust::device_vector<float> &in,
              thrust::device_vector<float> &out)
{
  cuda::std::mdspan temp_in(thrust::raw_pointer_cast(in.data()), height, width);
  cub::DeviceTransform::Transform(
    thrust::make_counting_iterator(0), out.begin(), width * height,
    [=] __host__ __device__(int id) { return dli::compute(id, temp_in); });
}

int main() 
{
  int height = 2048;
  int width = 8192;

  thrust::device_vector<float> d_prev = dli::init(height, width);
  thrust::device_vector<float> d_next(height * width);
  thrust::host_vector<float> h_prev(height * width);

  for (int write_step = 0; write_step < 3; write_step++) 
  {
    thrust::copy(d_prev.begin(), d_prev.end(), h_prev.begin());

    for (int compute_step = 0; compute_step < 750; compute_step++) 
    {
      simulate(width, height, d_prev, d_next);
      d_prev.swap(d_next);
    }

    dli::store(write_step, height, width, h_prev);

    cudaDeviceSynchronize(); 
  }
}
```

To speed this up on the GPU side, we now need to create multiple CUDA streams, one for copying data and one for running the actual simulation compute logic. Now if we run an async copy from the CPU, and call the copy command on the GPU, we want to ensure that write is complete before using it for the next compute stream - this is where we utilize `cudaStreamSynchronize` on different CUDA Streams to ensure the work is done. However, the below diagram **still introduces a data race** - as data is being copied from `dprev` to host, the GPU simulation will begin writing to it
![CUDA Stream Simulation](/img/cuda_stream_synchronization.png)

Solving these data race issues is usually done by utilizing another layer of indirection via buffers - you force the copy to be synchronous on the GPU side, and then you allow writing from the buffer to the host asynchronously:
- Allocate a device buffer
- Copy `dprev` into it in the compute stream
  - After, allow `dprev` to be written to 
- Start async copy frmo this buffer to `hprev` on the CPU

While this does seem redundant and esesntially leading us back to the same synchronous issue as before, this is still faster solely because GPU memory transfers are over 10x faster than CPU transfers, and 1000x faster than GPU to CPU transfers. Meaning transferring from `dprev` to a GPU buffer is faster than synchronously waiting for copying `dprev` to `hprev`. The real bottleneck is cross device transfers
![GPU Bandwidth](/img/gpu_cpu_inter_intra_bandwidth.png)


## Exercise - Streams
replace thrust::copy with cudaMemcpyAsync
put compute and copy operations in separate CUDA streams
synchronize the streams to follow the pattern from the diagram below

Input:
```cpp
%%writefile Sources/async-copy.cu
#include "dli.h"

void simulate(int width, int height, const thrust::device_vector<float> &in,
              thrust::device_vector<float> &out, 
              cudaStream_t stream = 0) 
{
  cuda::std::mdspan temp_in(thrust::raw_pointer_cast(in.data()), height, width);
  cub::DeviceTransform::Transform(
      thrust::make_counting_iterator(0), out.begin(), width * height,
      [=] __host__ __device__(int id) { return dli::compute(id, temp_in); },
      stream);
}

int main() 
{
  int height = 2048;
  int width = 8192;

  thrust::device_vector<float> d_prev = dli::init(height, width);
  thrust::device_vector<float> d_next(height * width);
  thrust::device_vector<float> d_buffer(height * width);
  thrust::host_vector<float> h_prev(height * width);

  const int compute_steps = 750;
  const int write_steps = 3;

  // 1. Create compute and copy streams

  for (int write_step = 0; write_step < write_steps; write_step++) 
  {
    thrust::copy(d_prev.begin(), d_prev.end(), d_buffer.begin());

    // 2. Replace `thrust::copy` with `cudaMemcpyAsync` on copy stream.
    //    Use `thrust::raw_pointer_cast(vec.data())` to get raw pointers from Thrust containers.
    thrust::copy(d_buffer.begin(), d_buffer.end(), h_prev.begin());

    for (int compute_step = 0; compute_step < compute_steps; compute_step++) 
    {
      // 3. Put `simulate` on compute stream
      simulate(width, height, d_prev, d_next);
      d_prev.swap(d_next);
    }

    // 4. Make sure to synchronize copy stream before reading `h_prev`
    dli::store(write_step, height, width, h_prev);

    // 5. Make sure to synchronize compute stream before next iteration
    cudaDeviceSynchronize(); 
  }
}
```



Output:
```cpp
cudaStream_t compute_stream;
cudaStreamCreate(&compute_stream);

cudaStream_t copy_stream;
cudaStreamCreate(&copy_stream);

for (int write_step = 0; write_step < write_steps; write_step++) 
{
  cudaMemcpy(thrust::raw_pointer_cast(d_buffer.data()),
             thrust::raw_pointer_cast(d_prev.data()),
             height * width * sizeof(float), cudaMemcpyDeviceToDevice); // copy d_prev to d_buffer -> sync
  cudaMemcpyAsync(thrust::raw_pointer_cast(h_temp.data()),
                  thrust::raw_pointer_cast(d_buffer.data()),
                  height * width * sizeof(float), cudaMemcpyDeviceToHost,
                  copy_stream); //copy d_buffer to h_temp on host

  for (int compute_step = 0; compute_step < compute_steps; compute_step++) {
    simulate(width, height, d_prev, d_next, compute_stream); //run simulation on d_prev, we know the data already sits in d_buffer from the sync copy command above
    d_prev.swap(d_next); //swap our data, results now sit in d_prev. d_prev is diff from d_buffer, and d_buffer is being written to h_temp
  }

  cudaStreamSynchronize(copy_stream); // ensure we've finished writing to h_temp
  dli::store(write_step, height, width, h_temp); //store h_temp

  cudaStreamSynchronize(compute_stream); //ensure we're done writing results
}

cudaStreamDestroy(compute_stream);
cudaStreamDestroy(copy_stream)
```