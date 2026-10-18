---
title: sortColors
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# sortColors

```python
class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        freqs = collections.Counter(nums)
        curr = 0
        for num in [0, 1, 2]:
            for _ in range(freqs[num]):
                nums[curr] = num
                curr += 1
        
        return
```