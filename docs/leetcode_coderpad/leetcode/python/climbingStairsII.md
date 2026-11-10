---
title: climbingStairsII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# climbingStairsII

```python
class Solution:
    def climbStairs(self, n: int, costs: List[int]) -> int:
        # [0, n]
        # 1 indexed costs
        # n = 4
        # steps = [0, 1, 2, 3, 4]
        # costs = [1, 2, 3, 4]
        # dp    = [0, 2, N, N, N]

        @cache
        def dp(n):
            if n == 0:
                return(0)
            elif n == 1:
                return(costs[0] + 1)

            minCost = min(
                dp(n-1) + costs[n - 1] + ((n - (n-1))**2),
                dp(n-2) + costs[n - 1] + ((n - (n-2))**2)
            )
            if n > 2:
                minCost = min(
                    minCost,
                    dp(n-3) + costs[n - 1] + ((n - (n-3))**2),                    
                )                

            return(minCost)
        
        return(dp(n))
```