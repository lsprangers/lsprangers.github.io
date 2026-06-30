---
title: maxConsecutiveOnesIII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxConsecutiveOnesIII

```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        nZero = 0
        left = right = 0
        resp = 0
        while right < len(nums):
            if nums[right] == 0:
                nZero += 1
            
            while nZero > k:
                if nums[left] == 0:
                    nZero -= 1
                left += 1
            
            resp = max(
                resp,
                right - left + 1
            )
            right += 1
        
        return(resp)
```