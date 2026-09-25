---
layout: technical
title: 4.01 - Final C++ Project
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Final C++ Project
The Maxwell's Equations simulator predicts how electromagnetic waves propagate. For this assessment, you'll begin with a simple, though working, 2D Maxwell's Equations simulator. In its current CPU-only form, this application takes about 15 seconds to run on $4096^2$ cells, and 4 minutes to run on $65536^2$ cells. Your task is to GPU-accelerate the program, retaining the correctness of the simulation.

## Step 1 and 2
Focus on re-doing the `for_each` and `std::vector` into using counting and fancy iterators so that everything can be done on GPU, and there's no writing to buffers. The more that are pushed into iterators, the more memory efficient and parallel it becomes

```cpp
%%writefile Sources/maxwell.cu
#include "dli.h"


void update_hx(int n, float dx, float dy, float dt,
               thrust::device_vector<float> &hx,
               thrust::device_vector<float> &ez) {
  
  // iterator to get output if e[i + n] - e[i]
  auto ez_diff_begin = thrust::make_transform_iterator(
      thrust::make_zip_iterator(
          // zip together e[i + n], e[i]
          thrust::make_tuple(ez.begin() + n, ez.begin())),
      // input here is a zip iterator output, which is a tuple
      [] __host__ __device__(thrust::tuple<float, float> t) {
        return thrust::get<0>(t) - thrust::get<1>(t);
      });

  // pass output of e[i + n] - e[i] here
  // 
  thrust::transform(
      hx.begin(), hx.end() - n,
      ez_diff_begin,
      hx.begin(),
      // input here is h begin and ez_diff begin, which are both floats
      // and we are writing those into h.begin(), i.e. writing into h
      [dt, dx, dy] __host__ __device__(float h, float cex) {
        return h - dli::C0 * dt / 1.3f * cex / dy;
      });
}

void update_hy(int n, float dx, float dy, float dt,
               thrust::device_vector<float> &hy,
               thrust::device_vector<float> &ez) {
  
  // iterator to get output if ez[i] - ez[i+1]
  auto ez_diff_begin = thrust::make_transform_iterator(
      thrust::make_zip_iterator(
          thrust::make_tuple(ez.begin(), ez.begin() + 1)),
      [] __host__ __device__(thrust::tuple<float, float> t) {
        return thrust::get<0>(t) - thrust::get<1>(t);
      });

  // pass output of ez[i] - ez[i+1]
  thrust::transform(
      hy.begin(), hy.end() - n,
      ez_diff_begin,
      hy.begin(),
      // input here is h begin and ez_diff begin, which are both floats
      // and we are writing those into h.begin(), i.e. writing into h
      [dt, dx, dy] __host__ __device__(float h, float cex) {
        return h - dli::C0 * dt / 1.3f * cex / dy;
      });
}

void update_dz(int n, float dx, float dy, float dt, thrust::device_vector<float> &hx_vec,
               thrust::device_vector<float> &hy_vec, thrust::device_vector<float> &dz_vec,
               thrust::counting_iterator<int> first, thrust::counting_iterator<int> last) {
  auto hx = hx_vec.begin();
  auto hy = hy_vec.begin();
  auto dz = dz_vec.begin();

  thrust::for_each(thrust::device, first, last,
                // leaving this lambda alone, seems complicated
                [n, dx, dy, dt, hx, hy, dz] __host__ __device__ (int cell_id) {
                  if (cell_id > n) {
                    float hx_diff = hx[cell_id - n] - hx[cell_id];
                    float hy_diff = hy[cell_id] - hy[cell_id - 1];
                    dz[cell_id] += dli::C0 * dt * (hx_diff / dx + hy_diff / dy);
                  }
                });
}


void update_ez(thrust::device_vector<float> &d_ez, thrust::device_vector<float> &d_dz) {                            
  thrust::transform(thrust::device, d_dz.begin(), d_dz.end(), d_ez.begin(),
                 [] __host__ __device__ (float d) { return d / 1.3f; });
}

// Do not change the signature of this function
void simulate(int cells_along_dimension, float dx, float dy, float dt,
              thrust::device_vector<float> &d_hx,
              thrust::device_vector<float> &d_hy,
              thrust::device_vector<float> &d_dz,
              thrust::device_vector<float> &d_ez) {

  int cells = cells_along_dimension * cells_along_dimension;
  thrust::counting_iterator<int> cell_ids(cells);
  auto first = thrust::counting_iterator<int>(0);
  auto last  = thrust::counting_iterator<int>(cells);

  for (int step = 0; step < dli::steps; step++) {
    update_hx(cells_along_dimension, dx, dy, dt, d_hx, d_ez);
    update_hy(cells_along_dimension, dx, dy, dt, d_hy, d_ez);
    update_dz(cells_along_dimension, dx, dy, dt, d_hx, d_hy, d_dz, first, last);
    update_ez(d_ez, d_dz);
  }

}
```

## Step 3
We want to do a pooling average over strides of blocks

If we have a $1,024$ initial Grid and our blocks are $2 \times 4$ then we would get to a coarse grid of $512$ rows and $256$ columns, and in total would run $256$ total `cub::BlockReduce`

`cub::BlockReduce` only writes the results to thread 0, so the entire idea is setting up the correct scaffolding and operations so that all of the averaging is done in thread blocks and returned to a new matrix

```cpp
%%writefile Sources/coarse.cu
#include "dli.h"

__global__ void kernel(dli::temperature_grid_f fine,
                       dli::temperature_grid_f coarse) {
  int coarse_row = blockIdx.x / coarse.extent(1);
  int coarse_col = blockIdx.x % coarse.extent(1);
  int row = threadIdx.x / dli::tile_size;
  int col = threadIdx.x % dli::tile_size;
  int fine_row = coarse_row * dli::tile_size + row;
  int fine_col = coarse_col * dli::tile_size + col;

  float thread_value = fine(fine_row, fine_col);

  const int total_cells = dli::tile_size * dli::tile_size;

  __shared__ cub::BlockReduce<float, total_cells>::TempStorage storage;
  float block_sum = cub::BlockReduce<float, total_cells>(storage).Sum(thread_value);

  float block_average = block_sum / total_cells;

  if (threadIdx.x == 0) {
    coarse(coarse_row, coarse_col) = block_average;
  }

  
}

// Don't change the signature of this function
void coarse(dli::temperature_grid_f fine, dli::temperature_grid_f coarse) {
  kernel<<<coarse.size(), dli::block_threads>>>(fine, coarse);
}
```

## Original Code - Step 1 and 2
```cpp
#include "dli.h"

// FIXME(Step 1):
// accept device containers instead of `std::vector<float>`
void update_hx(int n, float dx, float dy, float dt, std::vector<float> &hx,
               std::vector<float> &ez, std::vector<float> &buffer) {
  // FIXME(Step 2):
  // Use zip and transform iterators to avoid materializing `ez[i + n] - ez[i]`
  // FIXME(Step 1):
  // compute transformation on GPU
  std::transform(ez.begin() + n, ez.end(), ez.begin(), buffer.begin(),
                 [](float x, float y) { return x - y; });

  // FIXME(Step 1):
  // compute transformation on GPU
  std::transform(hx.begin(), hx.end() - n, buffer.begin(), hx.begin(),
                 [dt, dx, dy](float h, float cex) {
                   return h - dli::C0 * dt / 1.3f * cex / dy;
                 });
}

// FIXME(Step 1):
// accept device containers instead of `std::vector<float>`
void update_hy(int n, float dx, float dy, float dt, std::vector<float> &hy,
               std::vector<float> &ez, std::vector<float> &buffer) {
  // FIXME(Step 2):
  // Use zip and transform iterators to avoid materializing `ez[i] - ez[i + 1]`
  // FIXME(Step 1):
  // compute transformation on GPU
  std::transform(ez.begin(), ez.end() - 1, ez.begin() + 1, buffer.begin(),
                 [](float x, float y) { return x - y; });

  // FIXME(Step 1):
  // compute transformation on GPU
  std::transform(hy.begin(), hy.end() - 1, buffer.begin(), hy.begin(),
                 [dt, dx, dy](float h, float cey) {
                   return h - dli::C0 * dt / 1.3f * cey / dx;
                 });
}

// FIXME(Step 1):
// accept device containers instead of `std::vector<float>`
void update_dz(int n, float dx, float dy, float dt, std::vector<float> &hx_vec,
               std::vector<float> &hy_vec, std::vector<float> &dz_vec,
               std::vector<int> &cell_ids) {
  auto hx = hx_vec.begin();
  auto hy = hy_vec.begin();
  auto dz = dz_vec.begin();

  // FIXME(Step 1):
  // compute for each on GPU
  std::for_each(cell_ids.begin(), cell_ids.end(),
                [n, dx, dy, dt, hx, hy, dz](int cell_id) {
                  if (cell_id > n) {
                    float hx_diff = hx[cell_id - n] - hx[cell_id];
                    float hy_diff = hy[cell_id] - hy[cell_id - 1];
                    dz[cell_id] += dli::C0 * dt * (hx_diff / dx + hy_diff / dy);
                  }
                });
}

// FIXME(Step 1):
// accept device containers instead of `std::vector<float>`
void update_ez(std::vector<float> &ez, std::vector<float> &dz) {
  // FIXME(Step 1):
  // compute transformation on GPU
  std::transform(dz.begin(), dz.end(), ez.begin(),
                 [](float d) { return d / 1.3f; });
}

// FIXME(Step 1):
// remove this function
std::vector<float> copy_to_host(const thrust::device_vector<float> &d_vec) {
  std::vector<float> vec(d_vec.size());
  thrust::copy(d_vec.begin(), d_vec.end(), vec.begin());
  return vec;
}

// Do not change the signature of this function
void simulate(int cells_along_dimension, float dx, float dy, float dt,
              thrust::device_vector<float> &d_hx,
              thrust::device_vector<float> &d_hy,
              thrust::device_vector<float> &d_dz,
              thrust::device_vector<float> &d_ez) {
  // FIXME(Step 1):
  // remove host containers and compute in the incoming device containers
  std::vector<float> hx = copy_to_host(d_hx);
  std::vector<float> hy = copy_to_host(d_hy);
  std::vector<float> dz = copy_to_host(d_dz);
  std::vector<float> ez = copy_to_host(d_ez);

  // FIXME(Step 2):
  // Remove `cell_ids` vector and use counting iterator instead
  int cells = cells_along_dimension * cells_along_dimension;
  std::vector<int> cell_ids(cells);
  for (int i = 0; i < cells; i++) {
    cell_ids[i] = i;
  }

  // FIXME(Step 2):
  // Remove `buffer` vector and use fancy iterators instead
  std::vector<float> buffer(cells);

  for (int step = 0; step < dli::steps; step++) {
    update_hx(cells_along_dimension, dx, dy, dt, hx, ez, buffer);
    update_hy(cells_along_dimension, dx, dy, dt, hy, ez, buffer);
    update_dz(cells_along_dimension, dx, dy, dt, hx, hy, dz, cell_ids);
    update_ez(ez, dz);
  }

  // FIXME(Step 1):
  // remove copy to host containers, compute in the incoming device containers
  d_hx = hx;
  d_hy = hy;
  d_dz = dz;
  d_ez = ez;
}
```



## Original Code - Step 3
```cpp
%%writefile Sources/coarse.cu
#include "dli.h"

__global__ void kernel(dli::temperature_grid_f fine,
                       dli::temperature_grid_f coarse) {
  int coarse_row = blockIdx.x / coarse.extent(1);
  int coarse_col = blockIdx.x % coarse.extent(1);
  int row = threadIdx.x / dli::tile_size;
  int col = threadIdx.x % dli::tile_size;
  int fine_row = coarse_row * dli::tile_size + row;
  int fine_col = coarse_col * dli::tile_size + col;

  float thread_value = fine(fine_row, fine_col);

  // FIXME(Step 3):
  // Compute the sum of `thread_value` across threads of a thread block
  // using `cub::BlockReduce`
  float block_sum = ...;

  // FIXME(Step 3):
  // `cub::BlockReduce` returns block sum in thread 0, make sure to write
  // result only from the first thread of the block
  coarse(coarse_row, coarse_col) = block_average;
}

// Don't change the signature of this function
void coarse(dli::temperature_grid_f fine, dli::temperature_grid_f coarse) {
  kernel<<<coarse.size(), dli::block_threads>>>(fine, coarse);
}
```


## Original Code - Step 4