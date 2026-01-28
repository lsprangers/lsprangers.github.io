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

The main benefit of this is that an insertion happens in $O(\log n)$ time, but getting the largest or smallest element is guaranteed $O(1)$ - you can think of these items as a sorted array, except arrays require $O(n)$ shuffling when items are inserted or removed, where heaps are stored as binary trees so this shuffling isn't $O(n)$, but $O(1)$


|Type        | Insert     | Search (Max only)     | Delete     |
|------------|------------|------------|------------|
|Best Case   | O(logn)       | O(1)       | O(logn)       |
|Average Case| O(logn)    | O(1)       | O(logn)    |
|Worst Case  | O(logn)       | O(1)       | O(logn)       |

- A Max Heap is a tree data structure which is a bit more specific than a Binary Search Tree, the Max Heap structure has the largest node as the root node, and any nodes children are less than it's node
- Allows us to get the max item very quickly, and insert and delete operations involve potentially rotating some items but altogether are O(logn) for worst, average, and best cases since you still traverse a general tree structure