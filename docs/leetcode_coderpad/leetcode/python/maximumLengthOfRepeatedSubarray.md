---
title: maximumLengthOfRepeatedSubarray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumLengthOfRepeatedSubarray

```python
class Solution:
    def findLength(self, nums1: List[int], nums2: List[int]) -> int:
        # dp[i][j] will be the longest common prefix of A[i:] and B[j:]
        n = len(nums1)
        m = len(nums2)
        dp = [ [0] * (m+1) for _ in range(n + 1)]
        # m m m m m
        # m m m m m
        # ... 
        # m m m m m
        # n times
        resp = 0
        for nIdx in range(n - 1, -1, -1):
            for mIdx in range(m - 1, -1, -1):
                if nums1[nIdx] == nums2[mIdx]:
                    dp[nIdx][mIdx] = dp[nIdx + 1][mIdx + 1] + 1
                
                resp = max(resp, dp[nIdx][mIdx])
        
        return(resp)
```