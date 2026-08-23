---
layout: technical
title: 1.05 - Serial vs Parallel Execution
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Exercise - Serial vs Tabular Execution
It's quite easy to screw up a parallel GPU program and have it run serially even though you expect it to run in parallel. *For loops run sequentially*, even though it'd be nice if they were just magically parallelized

A good example is sum by row operation where we need to compute the total sum over each row in a matrix. If we wanted to use `thrust::tabulate`. `tabulate` receives a sequence and a function, and it applies the function to each element in the sequence, and stores the result into the provided sequence

Below, `vec` would end up storing `{0, 2, 4, 6}`
```cpp
thrust::universal_vector<int> vec(4);
thrust::tabulate(
   thrust::device, vec.begin(), vec.end(), 
   []__host__ __device__(int index) -> int { 
      return index * 2; 
   })
```

What I still don't fully grasp at the end of this is why `reduce_by_key` is inherently more parallel than a `for` loop inside of `tabulate`. The `for` loop itself would be sequential over all of the columns in the row, but each row itself would be ran in parallel. If we have 1,000 rows of 2,000 columns each, the `tabulate` call launches 1,000 parallel threads (one per row), and each thread is then trapped doing 2,000 sequential loop steps

The `reduce_by_key` approach would flatten the entire problem into 2,000,000 parallel threads, one per element, and instead of one thread adding up a row all of the hundreds / thousands of threads work together using a special tree based reduction to sum that same row in a fraction of the time

The `tabulate` call had a throughput of 1.7 GB/s and ran for 0.5 seconds, and the `reduce_by_key` had a throughput of ~300GB/s and ran in 0.007 seconds, which is a great showing of how this utilizes all GPU cores to run the computation in a fraction of the time


### The Segmented Sum Problem
The segmented sum problem, i.e. reduction as a whole, is a memory-bound algorithm. This means instead of analyzing it in terms fo elapsed time it's better to look at how many bytes it procesess in a second, which is known as **achieved throughput**

Contrasting this with the peak theoretical bandwidth of the GPU, we'll get a good understanding of the GPU saturation, which showcases how efficient the algorithm is

Ideally the GPU saturation is near 100% meaning we're processing as many rows as possible in parallel

The below algorithm will produce a low performance throughput of ~1.8GB / second which is considerably lower than the maximum bandwidth for GPU's. The biggest reason is because of the use of
```cpp
thrust::tabulate(thrust::device, sums.begin(), sums.end(), [=]__host__ __device__(int segment_id) {
    float sum = 0;
    for (int i = 0; i < segment_size; i++) {
        sum += d_values_ptr[segment_id * segment_size + i];
    }
    return sum; 
})
```
 
<!-- Collapsible C++ snippet -->
<details>
  <summary>Show C++ Script</summary>

```cpp
%%writefile Sources/naive-segmented-sum.cu
#include <cstdio>
#include <chrono>

#include <thrust/tabulate.h>
#include <thrust/execution_policy.h>
#include <thrust/universal_vector.h>

thrust::universal_vector<float> row_temperataures(
    int height, int width,
    const thrust::universal_vector<float>& temp) 
{
    // allocate vector to store sums
    thrust::universal_vector<float> sums(height);

    // take raw pointer to `temp`
    const float *d_temp_ptr = thrust::raw_pointer_cast(temp.data());

    // compute row sum
    thrust::tabulate(thrust::device, sums.begin(), sums.end(), [=]__host__ __device__(int row_id) {
        float sum = 0;
        for (int i = 0; i < width; i++) {
            sum += d_temp_ptr[row_id * width + i];
        }
        return sum; 
    });

    return sums;
}

thrust::universal_vector<float> init(int height, int width) {
  const float low = 15.0;
  const float high = 90.0;
  thrust::universal_vector<float> temp(height * width, low);
  thrust::fill(thrust::device, temp.begin(), temp.begin() + width, high);
  return temp;
}

int main() 
{
    int height = 16;
    int width = 16777216;
    thrust::universal_vector<float> temp = init(height, width);

    auto begin = std::chrono::high_resolution_clock::now();
    thrust::universal_vector<float> sums = row_temperataures(height, width, temp);
    auto end = std::chrono::high_resolution_clock::now();
    const double seconds = std::chrono::duration<double>(end - begin).count();
    const double gigabytes = static_cast<double>(temp.size() * sizeof(float)) / 1024 / 1024 / 1024;
    const double throughput = gigabytes / seconds;

    std::printf("computed in %g s\n", seconds);
    std::printf("achieved throughput: %g GB/s\n", throughput);
}
```

### Reduce By Key
The general answer to this is to use `thrust::reduce_by_key` which is a generalization of `thrust::reduce`. Instead of reducing the sequence to s single value it allows you to reduce segments of values and store the results in an output array / iterator. Distinguishing the elements is done by providing keys, where consecutive keys form a segment, and then `reduce_by_key` returns one value per segment

```cpp
int in_keys[] = {1, 1, 1, 3, 3};
int in_vals[] = {1, 2, 3, 4, 5};
int out_keys[2];
int out_vals[2];

thrust::reduce_by_key(in_keys, in_keys + 5, in_vals, out_keys, out_vals);
// out_keys = {1, 3}
// out_vals = {6, 9}

thrust::universal_vector<float> row_temperatures(
    int height, int width,
    thrust::universal_vector<int>& row_ids,
    thrust::universal_vector<float>& temp)
{
    thrust::universal_vector<float> sums(height);
    thrust::reduce_by_key(
        thrust::device, 
        row_ids.begin(), row_ids.end(),   // input keys 
        temp.begin(),                     // input values
        thrust::make_discard_iterator(),  // output keys
        sums.begin());                    // output values

    return sums;
}
```

The `discard_operator` is essentially `/dev/null` and is a black hole you can send iterators into when you no longer want to track them

## Exercise Input
Example of transform iterator API:
```cpp
int constant = 2;
auto transform_it = thrust::make_transform_iterator(
// iterator to the beginning of the input sequence
vector.begin(), 
// capture constant in the lambda by value with `[name]`
[constant]__host__ __device__(float value_from_input_sequence) { 
    // transformation of each element
    return value_from_input_sequence * constant; 
})
```

Along with counting iterator API:
```cpp
// start counting from 0
auto count_it = thrust::make_counting_iterator(0)
```

Rewrite the sum code below without materializing keys into memory:
```cpp
%%writefile Sources/segmented-sum-optimization.cu
#include "dli.h"

thrust::universal_vector<float> row_temperatures(
    int height, int width,
    thrust::universal_vector<int>& row_ids,
    thrust::universal_vector<float>& temp)
{
    thrust::universal_vector<float> sums(height);

    // Modify the line below to use counting and transform iterators to 
    // generates row indices `id / width` instead
    auto row_ids_begin = row_ids.begin(); 
    auto row_ids_end = row_ids_begin + temp.size();

    thrust::reduce_by_key(thrust::device, 
                          row_ids_begin, row_ids_end, 
                          temp.begin(), 
                          thrust::make_discard_iterator(), 
                          sums.begin());

    return sums;
}
```

## Exercise Solution
The part I needed help on below was the `transform_end` portion - I didn't really get what `reduce_by_key` needed from `transform_start , transform_end` and `transform_start` is an iterator, where `transform_end` just kinda seems like an end to a range. I don't get:
- How we can add an integer to an iterator and get an end iterator
- How storing the start of a counting iterator to return indexes at 0 somehow makes sense if the end is a counting iterator starting at `height * width`

Answers:
- These cpp iterators are **random access iterators** which means they behave exactly as raw pointers
- You can do `random_ptr + 5` and it will be valid pointer arithmetic to hop forward in memory
- Since they're fancy iterators (virtual iterators without actual memory objects), no memory is accessed when you add them. It's pure math
    - `count_start` holds the number 0
    - `count_start + 10` holds a new structure holding a number 10
    - `transform_start` holds onto `count_start` and the lambda function
    - `transform_start + total_elements` is a bit odd. Thrust will pass the addition down into the underlying counting iterator, and will create a new transform iterator whose internal counter starts at `total_elements`
- `reduce_by_key` will then loop from `transform_start` to `transform_end`, and increment a counter from `0` to whatever `transform_end` is, and pass each value through the divison lambda

We use these iterators because they point to raw memory, and it allows us to loop over memory segments until `transform_start == transform_end`, and work through data sitting in that virtual memory without actually storing it anywhere else

```cpp
%%writefile Sources/segmented-sum-optimization.cu
#include "dli.h"

thrust::universal_vector<float> row_temperatures(
    int height, int width,
    thrust::universal_vector<int>& row_ids,
    thrust::universal_vector<float>& temp)
{
    thrust::universal_vector<float> sums(height);

    // Modify the line below to use counting and transform iterators to 
    // generates row indices `id / width` instead

    // start counting from 0 to height * width
    auto count_start = thrust::make_counting_iterator(0);
    auto transform_start = thrust::make_transform_iterator(
        count_start,
        // width is constant
        [width] __host__ __device__ (int input_idx) {
            return input_idx / width;
        });
    auto total_elements = height * width;
    auto transform_end = transform_start + total_elements;
    
    thrust::reduce_by_key(thrust::device, 
                          transform_start, transform_end,
                          temp.begin(), 
                          thrust::make_discard_iterator(), 
                          sums.begin());

    return sums;
}
```

The expected solution is below:
```cpp
#include "dli.h"

thrust::universal_vector<float>
row_temperatures(int height, int width, thrust::universal_vector<int> &row_ids,
                 thrust::universal_vector<float> &temp) {
  thrust::universal_vector<float> sums(height);

  // use counting and transform iterators to generates row numbers instead
  auto row_ids_begin = thrust::make_transform_iterator(
      thrust::make_counting_iterator(0),
      [=] __host__ __device__(int i) { return i / width; });
  auto row_ids_end = row_ids_begin + temp.size();

  thrust::reduce_by_key(thrust::device, row_ids_begin, row_ids_end,
                        temp.begin(), thrust::make_discard_iterator(),
                        sums.begin());

  return sums;
}
```

## Next Exercise
We want to pass the final output into a mean average so we can see the segmented mean

### Input
```cpp
%%writefile Sources/segmented-mean.cu
#include "dli.h"

struct mean_functor {
    int width;
    __host__ __device__ float operator()(float x) const {
        return x / width;
    }
};

thrust::universal_vector<float> row_temperatures(
    int height, int width,
    thrust::universal_vector<int>& row_ids,
    thrust::universal_vector<float>& temp)
{
    thrust::universal_vector<float> means(height);

    // use `transform_output_iterator` instead of `means.begin()`
    auto means_output = means.begin(); 

    auto row_ids_begin = thrust::make_transform_iterator(
        thrust::make_counting_iterator(0), 
        [=]__host__ __device__(int i) {
            return i / width;
        });
    auto row_ids_end = row_ids_begin + temp.size();

    thrust::reduce_by_key(thrust::device, 
                          row_ids_begin, 
                          row_ids_end, 
                          temp.begin(), 
                          thrust::make_discard_iterator(), 
                          means_output);

    auto transform_op = mean_functor{width};

    // remove this `transform` call
    thrust::transform(thrust::device, 
                      means.begin(), 
                      means.end(), 
                      means.begin(), 
                      transform_op);

    return means;
}   
```

### Solution
This one I actually did by myself huh
- `reduce_by_key` passes the output into the iterator `means_output` since thrust accepts general output iterators for its results
-  `reduce_by_key` discards the keys, and for each key segment it outputs a singular `int` value to `means_output`, which itself is an iterator
- `means_output` would take in that output sum value and run it over the `mean_functor{width}` (which is just an initialized function itself)
    - The `operator()` is called on each output natively
    - When `reduce_by_key` finishes aggregating a segment, it attempts to write the resulting sum to the output iterator we give to it `*means_output = sum;`
    - In this scenario, the output iterator we gave to it is `thrust::transform_output_iterator`, and so it doesn't return a raw `float&`, instead the dereference operator `*` returns a temporary object that holds a reference to:
        - Another underlying iterator `means.begin()`
        - A copy of the functor program `mean_functor{width}`
        - The output iterator calls `mean_functor::operator()(sum)`, and the resulting float is written to the memory location pointed to by `means.begin()`

So at the end of everything, the output iterator just acts as a proxy iterator inbetween the real iterator and the reduce by key:
```cpp
// Simplified conceptual view of Thrust's internal proxy assignment
template <typename T>
proxy& operator=(const T& value) {
    // 1. Run the user's functor on the incoming value
    auto transformed_value = user_functor(value); 
    
    // 2. Write the transformed result to the real underlying iterator
    *real_iterator = transformed_value; 
    
    return *this;
}
```

```cpp
%%writefile Sources/segmented-mean.cu
#include "dli.h"

struct mean_functor {
    int width;
    __host__ __device__ float operator()(float x) const {
        return x / width;
    }
};

thrust::universal_vector<float> row_temperatures(
    int height, int width,
    thrust::universal_vector<int>& row_ids,
    thrust::universal_vector<float>& temp)
{
    thrust::universal_vector<float> means(height);

    // use `transform_output_iterator` instead of `means.begin()`
    auto means_output = thrust::transform_output_iterator(
        means.begin(),
        mean_functor{width}
    );

    auto row_ids_begin = thrust::make_transform_iterator(
        thrust::make_counting_iterator(0), 
        [=]__host__ __device__(int i) {
            return i / width;
        });
    auto row_ids_end = row_ids_begin + temp.size();

    thrust::reduce_by_key(thrust::device, 
                          row_ids_begin, 
                          row_ids_end, 
                          temp.begin(), 
                          thrust::make_discard_iterator(), 
                          means_output);

    return means;
}
```