---
title: Data Structures & Algorithms
layout: default
---

## DSA
This is a dump of all the DSA notes I had from school, coursework, and interviews

## Cheat Sheet
- Use prefix sum + hashmap for ***exact subarray sum*** questions: 
    - Count, existence, longest length, divisible/mod variants, especially when negatives may exist
    - Works for negative numbers, sliding window does not work for negative numbers
- Use sliding window for ***monotonic*** window problems based on ***at-most, or exact subarray*** questions:
    - At-most constraints, character frequency windows, and sum constraints on nonnegative arrays
    - Count valid subarrays with `right - left + 1`
- Prefix-sum init: 
    - `freq = {0: 1}` for counting 
    - `first = {0: -1}` for longest length
    - Usually keep only a running sum, not a full prefix array
- If negatives exist, standard sum-based sliding window is usually wrong; prefix sums still work

The number of subarrays between `left, right` is `right - left + 1`

---
- Use binary search on answer when the output is a min/max value and you can write a monotonic `check(mid)`
- If `check(x)` is true, then all smaller values are also true, or all larger values are also true
- Search the answer space, not the array: 
    - capacity, speed, sweetness, threshold, minimum/maximum feasible value
- Main job is not coding binary search; it is proving the monotonicity and writing `check(mid)` correctly
- Use half-open interval: search space is `[left, right)`
- For most problems, half open will work
    - `mid = left + (right - left) // 2`
    - Initialize with `left = 0`, `right = len(arr)`
    - Loop with `while left < right`
    - `if check(mid): right = mid else: left = mid + 1`
    - return `left` as first valid position or insertion point
- For last valid X, need to switch to:
    - `mid = left + right + 1 // 2`
    - `if check(mid): left = mid + 1`
    - `else: right = mid - 1`

---
- Union Find helps in quick retrieval of connected components
- Minimum Spanning Tree's give us the smallest fully connected graph (v + e's) based on weights
    - Kruskal's is best used on list of edges where we can sort edges and pick via connected components 
    - Prim's is best for adjacency lists where we traverse over nodes based on visited set
- BFS can natively find shortest path on an unweighted graph
    - Djikstra can find it in a weighted graph with non-negative weights
        - Store weights in min heap and traverse while min heap is alive. Automatically ensures shortest path (in terms of weights) are checked before larger weights. Still traverses every edge
    - Bellman-Ford works for any graph that doesn't have a negative weight cycle (infinitely negative if we loop). Just track an update with `distances[edge_to] = min(distances[edge_to], distances[edge_from] + edge_weight)` to find if coming from another node would result in a shorter path
        - Only need to traverse $N-1$ iterations, which allows avoiding a seen set so we can potentially find a longer number of hops with a smaller overall weight