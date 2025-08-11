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

What you need in a Dynamic Programming problem:
- A function / array that represents the answer to the problem from a given state
    - This is typically called `dp` in any problem
- A function / relation to transition between states
    - Getting from `dp[i]` to `dp[i + 1]` or vice versa
    - This is typically the hardest part to find in any DP problem
- A base case!
    - Starting at `dp[0]` (front) or `dp[len(input)]` (back) is typicaly the easiest to start with

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


[The Longest Increasing Subsequence](/docs/leetcode/python/longestIncreasingSubsequence.md) is another good problem showcasing subsequences and `dp` recurrence relations. In this there's even [a way to use binary search to make it $O(N \dot \log(N))$](/docs/leetcode/python/longestIncreasingSubsequence.md#binary-search)