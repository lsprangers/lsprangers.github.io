---
layout: technical
title: 1.01 - Execution Policies
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---


# Execution Policies
Execution policies are `std::` variables that help to define whether CUDA runtime libraries run on CPU or GPU!

![Execution Policy](/img/nvcc_thrust_execution_policy.png)

The below example shows where each `std::thrust` function would run

<!-- Collapsible C++ snippet -->
<details>
  <summary>Show C++ Script</summary>

```cpp
int main() {
    // CPU
    dli::where_am_I("CPU");
    thrust::universal_vector<int> vec{1};

    // GPU - __host__ __device__ allows lambda to run on either
    thrust::for_each(thrust::device, vec.begin(), vec.end(),
                    [] __host__ __device__(int) { dli::where_am_I("GPU"); });

    // CPU
    thrust::for_each(thrust::host, vec.begin(), vec.end(),
                    [] __host__ __device__(int) { dli::where_am_I("CPU"); });
    dli::where_am_I("CPU");
    }
```

</details>

## Examples
Showcasing how `std::thrust` allows for a heterogeneous CPU and GPU compilation experience showcases difference

### Single Threaded CPU

<!-- Collapsible C++ snippet -->
<details>
  <summary>Show C++ Script</summary>

```cpp
using std;

int main() {
    float k = 0.5;
    float ambient_temp = 20;
    std::vector<float> temp{ 42, 24, 50 };

    std::printf("step  temp[0]  temp[1]  temp[2]\n");
    for (int step = 0; step < 3; step++) {
        for (int i = 0; i < temp.size(); i++) {
            float diff = ambient_temp - temp[i];
            temp[i] = temp[i] + k * diff;
        }

        std::printf("%d     %.2f    %.2f    %.2f\n", step, temp[0], temp[1], temp[2]);
    }
}
```

</details>

Using lambda functions will help the middle portion potentially run faster with some SIMD

<!-- Collapsible C++ snippet -->
<details>
  <summary>Show C++ Script</summary>

```cpp
using std;

int main() {
    float k = 0.5;
    float ambient_temp = 20;
    std::vector<float> temp{ 42, 24, 50 };

    auto op = [=] (float temp) {
        float diff = ambient_temp - temp;
        return temp + k * diff;

    }
    std::printf("step  temp[0]  temp[1]  temp[2]\n");
    for (int step = 0; step < 3; step++) {
        // start, end range
        // startIter, lambda function to run
        std::transform(temp.begin(), temp.end(), 
                        temp.begin(), op)

        std::printf("%d     %.2f    %.2f    %.2f\n", step, temp[0], temp[1], temp[2]);
    }
}
```

</details>

### GPU with Thrust

<!-- Collapsible C++ snippet -->
<details>
  <summary>Show C++ Script</summary>

```cpp
using std;

int main() {
    float k = 0.5;
    float ambient_temp = 20;
    thrust::universal_vector<float> temp{ 42, 24, 50 };

    // add host for CPU, device for GPU
    auto op = __host__ __device__ (float temp) {
        float diff = ambient_temp - temp;
        return temp + k * diff;

    }
    std::printf("step  temp[0]  temp[1]  temp[2]\n");
    for (int step = 0; step < 3; step++) {
        // thrust::host runs on CPU
        // thrust::device runs on GPU
        thrust::transform(thrust::device 
                        temp.begin(), temp.end(), 
                        temp.begin(), op)

        std::printf("%d     %.2f    %.2f    %.2f\n", step, temp[0], temp[1], temp[2]);
    }
}
```

</details>