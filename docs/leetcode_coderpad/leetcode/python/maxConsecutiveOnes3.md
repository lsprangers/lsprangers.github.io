---
title: maxConsecutiveOnes3
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxConsecutiveOnes3

```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        n_zero = 0
        resp = 0
        for right in range(len(nums)):
            if nums[right] == 0:
                n_zero += 1
            
            while n_zero > k:
                if nums[left] == 0:
                    n_zero -= 1
                left += 1
            
            resp = max(resp, right - left + 1)
        
        return(resp)
```