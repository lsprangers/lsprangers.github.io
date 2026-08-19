---
layout: technical
title: GPU Notes + Courses
category: GPU Notes + Courses
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## GPU Courses
Did so much stuff in school I forgot, and then did a bunch of NVIDIA courses a while back that I just took the general notes and dumped them into here

GPU's are busses, and CPU's are cars! If we need to handle many small tasks with flexibility and not many passengers (data), a car works great. If we have a few specific tasks where we need to transport a large number of passengers (data), a bus works the best! GPU's typically have larger bandwidth, coupled with higher latency as compared to CPU's

The choice of single thread CPU, vs multi thread CPU, vs GPU usually comes to the data size $N$
![Single Thread CPU vs Multi Thread CPU vs GPU](/img/single_thread_cpu_vs_multi_thread_cpu_vs_gpu.png)

### Vocabulary
- **Bandwidth**: The maximum theoretical capacity of a network link
- **Throughput**: The actual data successfully delivered over time
- **Latency**: The delay or time from start to destination of data


### CUDA Compiler
CUDA itself is just another compiler to take C++ code and run it on a GPU, the same way `g++` and `aarch` are used to compile C++ onto x86 and ARM processors, `nvcc` is the CUDA compiler to transform C++ code into GPU instruction sets

`nvcc` doesn't inherently force it onto GPU usage, `nvcc` can just compile to C++ CPU code as well. Explicit GPU execution has to be programmed in application code and compilation itself - stuff like file system access, I/O to sockets, etc can only be done on the CPU, so every CUDA program starts on a CPU. The **execution space** refers to the actual place code is executed, whether it's the Host CPU, the Device GPU, etc

![NVCC CPU vs GPU](/img/nvcc_cpu_vs_gpu.png)
![Execution Policy](/img/nvcc_thrust_execution_policy.png)

The CUDA Runtime itself covers many areas, and inside of the CUDA Runtime there are a ton of different libraries that can be used to actually execute instructions on GPU's for data:
- Thrust builds pre-built components of common tasks for GPU for things like vectors, copying, sort, etc, except on a GPU
    - The [thrust example](/docs/llm_systems/gpu_course/code/thrust_execution_policy_cpu_vs_gpu.md#gpu-with-thrust) shows how `transform` lambda function can go from a for loop over a vector to a GPU based SIMD instruction
- CuDNN helps on DNN's
- CuBLAS helps on linear algebra
- etc

![CUDA Runtime](/img/cuda_runtime_libs.png)

That being said, if an algorithm doesn't fit into the standard CUDA Runtime / Libraries, 