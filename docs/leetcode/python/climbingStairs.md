---
title: climbingStairs
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# climbingStairs
Take a single step from $i - 1$ or 2 steps from $i - 2$!

Same as fibonnaci

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        dp = []
        dp.append(0)
        dp.append(1)
        dp.append(2)
        dp.append(3)
        # take a single step from i - 1, take two steps from i - 2
        for i in range(4, n + 1):
            dp.append(dp[-1] + dp[-2])
        
        return(dp[n])
```