---
title: longestCommonSubsequence
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

## longestCommonSubsequence

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # DP
        # 2D n+1, m+1 table of zeros
        n = len(text1)
        m = len(text2)
        dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        # O(n*m) time and space
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(
                        dp[i - 1][j],
                        dp[i][j - 1],
                        dp[i][j]
                    )
        return(dp[-1][-1])
```

# Walkthrough
Dynamic programming problem - in here we'll need to setup table

## Setup
- String A: `abcde`
- String B: `acfe`
- Matrix $M$ of rows $i$ and columns $j$ for $str_a$ and $str_b$
- If a cell $m_{i,j}$ has $str_{a}[i] = str_{b}[j]$, meaning the row and column letters are equal, then you take the last diagonal $m_{i-1, j-1}$ and add 1 to it
    - This corresponds to "given our last longest subsequence, you found another entry for it"
- If the cells do not match you need to take the $Max(m_{i-1, j}, m_{i-1, j-1}, m_{i, j-1})$ and just bring along the last largest subsequence we've found


***Table***:
|   |   | a | c | f | e |
|---|---|---|---|---|---|
|   | 0 | 0 | 0 | 0 | 0 |
| a | 0 | **1** | 1 | 1 | 1 |
| b | 0 | 1 | 1 | 1 | 1 |
| c | 0 | 1 | **2** | 2 | 2 |
| d | 0 | 1 | 2 | 2 | 2 |
| e | 0 | 1 | 2 | 2 | **3** | 