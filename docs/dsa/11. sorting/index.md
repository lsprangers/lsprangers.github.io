---
layout: technical
title: 11. Sorting
category: Data Structures & Algorithms
difficulty: Advanced
description: Divide & Conquer
show_back_link: true
---

## Sorting
Sorting encompasses a range of DSA using most of the techniques in other sections, so figured it was easier to put everything into here

| Algorithm       | Time Complexity (Best) | Time Complexity (Average) | Time Complexity (Worst) | Space Complexity | When to Use                                                                 |
|----------------|-------------------------|----------------------------|--------------------------|------------------|------------------------------------------------------------------------------|
| Bubble Sort    | $O(n)$                   | $O(n^2)$              |   $O(n^2)$            | $O(1)$       | Simple implementation, small datasets, rarely used in practice             |
| Selection Sort | $O(n^2)$                  | $O(n^2)$              |   $O(n^2)$            | $O(1)$       | Small datasets, when memory is limited                                     |
| Insertion Sort | $O(n)$                   | $O(n^2)$              |   $O(n^2)$            | $O(1)$       | Nearly sorted datasets, small datasets                                     |
| Merge Sort     | $O(n \log n)$             | $O(n \log n)$         |       $O(n \log n)$            | $O(n)$       | Stable sort, large datasets, external sorting                              |
| Quick Sort     | $O(n \log n)$             | $O(n \log n)$         |       $O(n^2)$            | $O(\log n)$      | Fastest in practice for average cases, in-memory sorting                   |
| Heap Sort      | $O(n \log n)$             | $O(n \log n)$         |       $O(n \log n)$            | $O(1)$       | Memory-constrained environments, when stability is not required            |
| Counting Sort  | $O(n + k)$               | $O(n + k)$           |    $O(n + k)$            | $O(k)$       | Small range of integers, stable sort, non-comparison-based sorting         |
| Radix Sort     | $O(nk)$                  | $O(nk)$              |   $O(nk)$            | $O(n + k)$       | Large datasets with integers or strings, non-comparison-based sorting      |
| Bucket Sort    | $O(n + k)$               | $O(n + k)$           |     $O(n^2)$            | $O(n)$       | Uniformly distributed data, when simplicity and speed are priorities       |


### Bubble Sort
### Selection Sort
### Insertion Sort
### Merge Sort
[Divide and Conquer](/docs/dsa/7.%20divide%20&%20conquer/index.md) and recursive algorithm based on breaking down a list into several sublists until each sublist contains a single element, afterwards merging each list in a way that resulting final set is sorted

Breaking down the entire list into $n$ sublists means we will need $O(n)$ space

The general algorithm uses 2 main functions:
- `mergeSort(array, startIndex, endIndex)` to divide and break problem down
- `merge(array, startIndex, middle, endIndex)` to merge together arrays

- For an array of size $n$ we need to split it in half each time, so there will be $O(\log n)$ calls to split it
- After that there will be $n$ resulting arrays we need to loop over and merge taking $O(n)$ time

Because of this, merge sort is typically used with smaller datasets where you want to ensure $O(n \logn)$ time is used, and you are able to utilize a good chunk of memory. It's labeled a stable sort because it's ***always*** the same time complexity, whereas other algorithms may collapse to $O(n)$ in some cases

<!-- Collapsible Python snippet -->
<details>
  <summary>Show Python Script</summary>

```python
def merge(leftArray, rightArray):
    resp = []
    leftIdx = 0
    rightIdx = 0

    while leftIdx < len(leftArray) and rightIdx < len(rightArray):
        if leftArray[leftIdx] < rightArray[rightIdx]:
            resp.append(leftArray[leftIdx])
            leftIdx += 1
        else:
            resp.append(rightArray[rightIdx])
            rightIdx += 1
    
    if leftIdx < len(leftArray):
        resp.extend(leftArray[leftIdx:])
    if rightIdx < len(rightArray):
        resp.extend(rightArray[rightIdx:])

    return(resp)          

def mergeSort(array):
    if len(array) <= 1:
        return(array)
    
    mid = len(array) // 2
    leftArray = array[0 : mid]
    rightArray = array[mid : ]
    return(
        # call to merge
        merge(
            mergeSort(leftArray), 
            mergeSort(rightArray)
        )
    )

arr = [1, 5, 3, 8, 2]
mergeSort(arr)

# [1, 5, 3, 8, 2]
# mid = 0 + (4-0) // 2 = 2
# left = [1, 5, 3], right = [8, 2]
# [1, 5], [3]
# ...
# [1], [5], [3], [8], [2]
# [1], [5], [3], [2, 8]
# [1, 5], [3], [2, 8]
# [1, 3, 5], [2, 8]
# [1, 2, 3, 5, 8]
```

</details>



### Quick Sort
Quick sort utilizes pivot elements and array swaps to sort an array - it only uses $O(1)$ space, and typically runs in $O(n \log n)$ time, but can become unstable and devolve into $O(n^2)$ for certain input arrays

Since the algorithm runs on the data structure itself, it could hypothetically be implemented on an array of any size that's stored on disk and partitioned across compute nodes

### Heap Sort
### Counting Sort
### Radix Sort
### Bucket Sort

## Distributed Sorting Algorithms
The algorithms above can run on local memory / singular node, but in terms of system design there are times we want to sort items across nodes

The algorithms are shown in the [Lecture 4 Distributed Sorting PDF](/arxiv_papers/DistributedSortingAlgorithms.pdf)

One specific example is the [Merge K Streams](/docs/leetcode_coderpad/coderpad_implementations/merge_k_sorted_streams.md) which is essentially the second half `merge` portion of merge sort ran over a number of $K$ streams coming in

Both [merge sort](#merge-sort) and [quick sort](#quick-sort) have distributed algorithm counterparts. Merge sort typically merges sorted chunks across nodes and keeps the merge process distributed so that final results can be written to distributed storage systems, while quick sort would sort the items across nodes keeping the storage local to each input node by partitioning data on a pivot and sort items on each node based on that pivot
- Distributed storage algorithms are used by Hadoop, Spark, and Flink type processing engines
- Both distributed merge sort and distributed quick sort are optimized to minimize data movement between nodes (shuffle) and to not bring all data onto a singular node

Most of these algorithms require coordinator leader nodes, worker nodes, and a fair amount of network shuffle and / or potential distributed file systems

### Distributed Merge Sort

### Distributed Quick Sort
Distributed Quick Sort Algorithm works by creating multiple partitions of the data, and then sorting each partition in parallel. By doing this, the algorithm can take advantage of multiple processors to sort the data more quickly

The chunk size is an important part of how the algorithm works; with too small or too large a chunk size, it will not perform well.


### Distributed Sample Sort