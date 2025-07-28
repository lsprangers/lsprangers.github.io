---
title: moveZeroes
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# moveZeroes

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        non_zeros = [nums[idx] for idx in range(len(nums)) if nums[idx] != 0]
        
        non_zero_idx = 0
        curr_idx = 0
        for nz in non_zeros:
            nums[curr_idx] = nz
            curr_idx += 1
        
        while curr_idx < len(nums):
            nums[curr_idx] = 0
            curr_idx += 1
        
        return
```