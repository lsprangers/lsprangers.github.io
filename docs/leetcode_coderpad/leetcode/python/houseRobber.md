---
title: houseRobber
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# houseRobber

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 2:
            return(max(nums))

        dp = [0] * n

        dp[0], dp[1], dp[2] = nums[0], nums[1], nums[0] + nums[2]

        for houseIdx in range(3, n):
            dp[houseIdx] = nums[houseIdx] + max(dp[houseIdx - 2], dp[houseIdx - 3])
        
        return(max(dp[n - 1], dp[n - 2]))
```