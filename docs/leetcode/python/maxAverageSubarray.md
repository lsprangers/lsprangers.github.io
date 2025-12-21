---
title: maxAverageSubarray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxAverageSubarray

```python
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        curr = sum(nums[:k])
        resp = curr
        for left in range(1, len(nums) - k + 1):
            curr -= nums[left - 1]
            curr += nums[left + k - 1]
            resp = max(resp, curr)
        
        return(resp / k)
```