---
layout: technical
title: 5. Heap & Priority Queues
category: Data Structures & Algorithms
difficulty: Advanced
description: Heap & Priority Queues
show_back_link: true
---

## Heap / Priority Queue
Heaps and priority queues are similar to queues, except internally they are structured in a way to keep an ordering - max heaps has the largest item as the root node, and min heaps have the smallest item

The actual internal data structure is a binary tree where certain rotations, replacements, and updates are done on the tree when we run `heap.pop()` or `heap.push()`

The main benefit of this is that an insertion happens in $O(\log n)$ time, but peeking the largest or smallest element is guaranteed $O(1)$. Removing the actual max / min element is still $O(\log n)$ as you have to do more rotations now that the root is gone

You can think of these items as a sorted array, except arrays require $O(n)$ shuffling when items are inserted or removed, where heaps are stored as binary trees so this shuffling isn't $O(n)$, but $O(1)$


|Type        | Insert     | Search (Max only)     | Delete     |
|------------|------------|------------|------------|
|Best Case   | O(logn)       | O(1)       | O(logn)       |
|Average Case| O(logn)    | O(1)       | O(logn)    |
|Worst Case  | O(logn)       | O(1)       | O(logn)       |


### Implementation
A Heap is a tree where the root element is the minimum of all elements. It's also a [complete binary tree](/docs/dsa/8.%20trees%20&%20graphs/index.md#complete-and-perfect-binary-tree)


Requirements of Max Heap:
- For any node `A` that's a parent of `B`, it must be that `A.val >= B`
    - Directly implies root node is the largest node
    - Min Heap would be the opposite
- The tree must be **complete**, which means every level, except possibly the last, is completely filled
    - Ensures balanced tree to guarantee $O(\log n)$

![Max Heap](/img/max_heap.png)

The typical implementation is done via arrays that are able to utilize index arithmetic to access nodes and parent / child relationships
- `i` is the current node
- `(2i)+1` is the left child
- `(2i)+2` is the right child
- `(i-1)//2` is parent
    - `2i + 2 - 1 == 2i + 1` and `// 2` gives `i`
    - `2i // 2 = i`

So above max heap can be stored as `arr = [25, 17, 20, 10, 8, 12, 15, 3, 9]`

The fastest an arbitrary array can get turned into a heap is $O(n)$ via ***sift-down*** or ***bubbling up***. During inserts and deletes, rotations are needed to ensure `parent.val >= child.val` at all locations. The number of operations scales logarithmically with the number of elements in the heap, and so one off insertions / deletions are $O(\log n)$ while heapifying an arbitrary list itself is $O(n)$

Swapping the last nodes, we get
`arr = [9, 17, 20, 10, 8, 12, 15, 3, 25]`

![Swapped Max Heap](/img/swapped_max_heap.png)

Pseudocode:
- Start at root
- Swap node with max value child
- Continue following that node down
    - Stop if leaf node

```python
def maxHeapify(A, i):
    left = 2 * i + 1
    right = 2 * i + 2
    largest = i
    if left < len(A) and A[left] > A[largest]:
        largest = left
    if right < len(A) and A[right] > A[largest]:
        largest = right
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        A = maxHeapify(A,largest)
    return A
```

This would need to be ran from the bottom most level of parents (i.e. the bottom most level of non-leaf nodes). *This is why it's required to be a complete binary tree*
```python
def buildMaxHeap(A):
    for i in range(len(A)//2,-1,-1):
        A = maxHeapify(A,i)
    return A
```

`maxHeapify` is $O(\log n)$
`buildMaxHeap` is $O(n)$

### Redis Based ZSets
Walked through [Redis ZSets for Priority Queues](/docs/architecture_components/databases%20&%20storage/Redis/ZSETS.md)

Redis can be used as a non-local priority queue that has different memory restrictions, and is potentially more optimized than a local implementation, while giving the overall same time complexities and operations