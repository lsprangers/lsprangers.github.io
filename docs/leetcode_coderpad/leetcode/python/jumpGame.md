---
title: jumpGame
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# jumpGame

## Greedy
```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return(True)

        furthestReachable = 0
        for idx in range(n):
            if idx > furthestReachable:
                return(False)
            
            furthestReachable = max(furthestReachable, idx + nums[idx])
        
        return(furthestReachable >= n - 1)
```

## Using DP 
```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return(True)

        dp = [False] * n
        dp[n - 1] = True

        # O(n) time and space
        mostLeftTrue = n - 1
        for idx in range(n - 1, -1, -1):
            if nums[idx] + idx >= mostLeftTrue:
                dp[idx] = True
                mostLeftTrue = idx
        
        return(dp[0])
```