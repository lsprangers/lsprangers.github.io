---
title: partitionArraySuchThatMaxDifferenceIsK
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# partitionArraySuchThatMaxDifferenceIsK

```python
class Solution:
    def partitionArray(self, nums: List[int], k: int) -> int:
        nums.sort()
        resp = 1
        
        currPtr = 0
        for right in range(len(nums)):
            if nums[right] - nums[currPtr] <= k:
                continue
            
            resp += 1
            currPtr = right
        
        return(resp)
```