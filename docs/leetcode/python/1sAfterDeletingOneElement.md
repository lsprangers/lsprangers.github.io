---
title: 1sAfterDeletingOneElement
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# 1sAfterDeletingOneElement

```python
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        resp = 0
        left = 0
        n_zeros = 0
        for right in range(len(nums)):
            n_zeros += 1 if nums[right] == 0 else 0
            while n_zeros > 1:
                n_zeros -= 1 if nums[left] == 0 else 0
                left += 1
            
            resp = max(resp, right - left)
        
        return(resp)
```