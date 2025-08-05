---
title: searchInRotatedSortedArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# searchInRotatedSortedArray

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums) < 2:
            return(0 if nums[0] == target else -1)

        # find inflection point
        low = 0
        high = len(nums) - 1

        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] > nums[-1]:
                low = mid + 1
            else:
                high = mid - 1


        if target <= nums[-1]:
            low = mid
            high = len(nums) - 1
        else:
            low = 0
            high = mid

        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] == target:
                return(mid)
            elif nums[mid] > target:
                high = mid - 1
            else:
                low = mid + 1
        
        return(-1)
```