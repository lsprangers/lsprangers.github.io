---
title: largestPerimiterArea
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# largestPerimiterArea

```python
class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        # a <= b <= c forms a triangle
        # a + b > c is required
        nums.sort()
        # start from largest
        for idx in range(len(nums) - 3, -1, -1):
            # if we found a valid triangle
            if nums[idx] + nums[idx + 1] > nums[idx + 2]:
                # it must be the answer because we greedily sorted
                return(nums[idx] + nums[idx + 1] + nums[idx + 2])
        
        return(0)
```