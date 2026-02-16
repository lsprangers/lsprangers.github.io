---
layout: technical
title: 7. Divide & Conquer
category: Data Structures & Algorithms
difficulty: Advanced
description: Divide & Conquer
show_back_link: true
---

## Divide And Conquer
The divide and conquer family of DSA is all around splitting up the problem into subproblems that are easily solvable, and then merging at the end (if needed)

A fair amount of sorting algorithms, particularly [merge sort](/docs/dsa/11.%20sorting/index.md#merge-sort) and [quick sort](/docs/dsa/11.%20sorting/index.md#quick-sort) are divide and conquer algorithms, usually taking $O(n \log n)$ time to do something by breaking down a problem of $n$ into individual sub-components and merging them back together

### GCD and LCM
Euclidean Algorithm: 

$\text{if } b \neq 0: GCD(A, B) = GCD(B, A \mod m)$

So you recursively break down our 2 components, A and B, until one of them is 0 which ultimately gives us the final result