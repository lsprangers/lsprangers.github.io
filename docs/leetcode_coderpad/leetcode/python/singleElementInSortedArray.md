---
title: singleElementInSortedArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# singleElementInSortedArray

```python
class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        # sorted array
        n = len(nums)
        if n < 2:
            return(nums[0])
        
        left = 0
        right = n
        
        # nums to left have first entry in even
        # [1, 1, 2, 2, ...]
        # nums to right have first entry in odd
        # [1, 1, bad, 2, 2, 3, 3]
        
        while left < right:
            mid = left + (right - left) // 2
            
            # check mid
            if 0 < mid < n - 1:
                if nums[mid] != nums[mid - 1] and nums[mid] != nums[mid + 1]:
                    return(nums[mid])
            
            elif mid == 0 and nums[mid] != nums[mid + 1]:
                    return(nums[mid])
            elif mid == n - 1 and nums[mid] != nums[mid - 1]:
                    return(nums[mid])
            
            
            # decide which way to go
            # if mid is even, and it's the same as it's right counterpart, answer to right
            if mid % 2 == 0:
                if mid < n - 1:
                    if nums[mid] == nums[mid + 1]:
                        left = mid + 1
                    else:
                        right = mid
                else:
                    print("bad 0")
                
            elif mid % 2 != 0:
                if mid > 0:
                    if nums[mid] == nums[mid - 1]:
                        left = mid + 1
                    else:
                        right = mid
                else:
                    print("bad 1")
        
        return(-1)
```