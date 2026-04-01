---
title: firstAndLastPositionOfElementInSortedArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# firstAndLastPositionOfElementInSortedArray

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        left = 0
        right = len(nums)
        
        # first valid X
        while left < right:
            mid = left + (right - left) // 2
            # may be first, or another
            if nums[mid] >= target:
                right = mid
            else:
                # mid surely isn't involved
                left = mid + 1
        
        if left >= len(nums) or nums[left] != target:
            return([-1, -1])
        
        curr_x_idx = left
        # 4
        while curr_x_idx < len(nums) and nums[curr_x_idx] == target:
            curr_x_idx += 1
        
        return([left, curr_x_idx - 1])
```