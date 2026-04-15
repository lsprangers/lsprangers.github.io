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
        if len(nums) < 1:
            return(-1)

        # closed interval, we need access to right
        left = 0
        right = len(nums) - 1

        # 4,5,6,7,0,1,2
        # target 0, 3
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return(mid)

            # left sorted - check based on left
            if nums[left] <= nums[mid]:
                # left sorted, target in left side
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
                    
            
            # right sorted - check based on right
            else:
                # right sorted, but target in left side
                if nums[right] >= target > nums[mid]:
                    left = mid + 1
                else:
                    right = mid - 1

        return(-1)
```