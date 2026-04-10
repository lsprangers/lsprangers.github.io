---
title: minCostClimbingStairs
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minCostClimbingStairs

```python
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        if not cost:
            return(0)

        n = len(cost)
        if n <= 2:
            return(min(cost))

        dp = [0] * n
        dp[0], dp[1] = cost[0], cost[1]

        for step in range(2, n):
            dp[step] = cost[step] + min(dp[step - 1], dp[step - 2])
        
        return(min(dp[-1], dp[-2]))
```