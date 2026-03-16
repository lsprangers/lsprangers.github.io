---
title: findPeakElement
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findPeakElement

```python
# If this element happens to be lying in a descending sequence of numbers. 
# or a local falling slope(found by comparing nums[i] to its right neighbour), 
# it means that the peak will always lie towards the left of this element. 
# Thus, we reduce the search space to the left of mid(including itself) and 
# perform the same process on left subarray.
# If the middle element, mid lies in an ascending sequence of numbers, 
# or a rising slope(found by comparing nums[i] to its right neighbour), 
# it obviously implies that the peak lies towards the right of this element. 
# Thus, we reduce the search space to the right of mid and perform the same 
# process on the right subarray.


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        low = 0
        high = len(nums) - 1
        while low < high:
            midIdx = low + (high - low) // 2
            mid = nums[midIdx]
            left = -float("inf")   
            right = -float("inf")     

            if midIdx < len(nums) - 1:
                right = nums[midIdx + 1]
            if midIdx > 0:
                left = nums[midIdx - 1]
                
            if mid > left and mid > right:
                return(midIdx)
            # if ascending, we don't need mid anymore it can't be a peak
            elif right >= left:
                low = midIdx + 1
            # if descending, include mid as it could be a peak
            else:
                high = midIdx
        
        return(low)
```
