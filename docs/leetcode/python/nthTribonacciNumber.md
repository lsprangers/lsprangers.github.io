---
title: nthTribonacci Number
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# nthTribonacci Number

```python
# problem 1137
class Solution:
    def tribonacci(self, n: int) -> int:
        dp = [0, 1, 1]
        for idx in range(3, n+1):
            dp.append(
                dp[idx - 3] +
                dp[idx - 2] +
                dp[idx - 1]
            )
        return(dp[n])
```