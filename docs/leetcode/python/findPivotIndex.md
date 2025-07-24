---
title: findPivotIndex
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

## findPivotIndex

```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        if len(nums) < 1:
            return(-1)

        idx = 0
        leftSum = 0
        rightSum = sum(nums[1:])
        while idx < len(nums) - 1 and leftSum != rightSum:
            idx += 1
            leftSum += nums[idx - 1]
            rightSum -= nums[idx]

        if leftSum == rightSum:
            return(idx)

        return(-1)        
```