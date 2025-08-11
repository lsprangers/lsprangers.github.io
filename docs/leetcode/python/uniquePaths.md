---
title: uniquePaths
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# uniquePaths

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # DP!
        # 1x1 grid = 0
        # 1x2 grid = 1
        # 2x1 grid = 1
        # 2x2 grid = (1x2) + (2x1) = 2
        # 3x1 = 1
        # 1x3 = 1
        # 2x3 = (1x3) + (2x2) = 3
        # Basically for any new cell, we just add together the two
        #    routes from above or left since robot can only move 
        #    in those 2 directions

        # Initial row and cols should all be 1
        dp = [[1 for col in range(n)] for row in range(m)]
        if m < 2 or n < 2:
            return(dp[-1][-1])
        
        for row in range(1, m):
            for col in range(1, n):
                dp[row][col] = dp[row-1][col] + dp[row][col - 1]
        
        return(dp[-1][-1])
```