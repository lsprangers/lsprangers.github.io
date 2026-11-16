---
title: minimumPositiveSumSubarray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumPositiveSumSubarray

```python
class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        resp = float("inf")
        n = len(nums)
        for left in range(n):

            for right in range(left + l, left + r + 1):
                if right > n:
                    continue
                currSum = sum(nums[left : right])
                if currSum > 0:
                    resp = min(resp, currSum)
        
        return(resp if resp != float("inf") else -1)
```