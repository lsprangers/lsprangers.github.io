---
title: 10. Dynamic Programming
category: Data Structures & Algorithms
difficulty: Advanced
description: Examples, definitions, and general knowledge around Dynamic Programming
show_back_link: true
---

## Dynamic Programming
Why Dynamic Programming?

When a question asks us to minimize, maximize, or find the number of ways to do something, it doesn't always mean that dynamic programming is the best approach, but it is usually a good indicator that we should at least consider using a dynamic programming approach.

In many programming languages, iteration is faster than recursion. Therefore, we often want to convert a top-down memoization approach into a bottom-up dynamic programming one (some people go directly to bottom-up, but most people find it easier to come up with a recursive top-down approach first and then convert it; either way is fine).

### Memoization Vs Top-Down



### Subsequences
One of the most common use cases is subsequence problems

Why this makes sense is because at any point we can "drag along" info from previous subsequences

Substrings must be ***contiguous***, but since subsequences aren't there are times we may want to compare two different subsequences - that is typically done in the dynamic programming 2D chart arrangement

[This Leetcode solution](/docs/leetcode/python/longestCommonSubsequence.md) showcases the below setup
- String A: `abcde`
- String B: `acfe`
- Matrix $M$ of rows $i$ and columns $j$ for $str_a$ and $str_b$
- If a cell $m_{i,j}$ has $str_{a}[i] = str_{b}[j]$, meaning the row and column letters are equal, then we take the last diagonal $m_{i-1, j-1}$ and add 1 to it
    - This corresponds to "given our last longest subsequence, we found another entry for it"
- If the cells do not match we need to take the $Max(m_{i-1, j}, m_{i-1, j-1}, m_{i, j-1})$ and just bring along the last largest subsequence we've found


***Table***:
|   |   | a | c | f | e |
|---|---|---|---|---|---|
|   | 0 | 0 | 0 | 0 | 0 |
| a | 0 | **1** | 1 | 1 | 1 |
| b | 0 | 1 | 1 | 1 | 1 |
| c | 0 | 1 | **2** | 2 | 2 |
| d | 0 | 1 | 2 | 2 | 2 |
| e | 0 | 1 | 2 | 2 | **3** | 
