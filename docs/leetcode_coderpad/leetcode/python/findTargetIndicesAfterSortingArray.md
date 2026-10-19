---
title: findTargetIndicesAfterSortingArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findTargetIndicesAfterSortingArray

```python
class Solution:
    def targetIndices(self, nums: list[int], target: int) -> list[int]:
        # try to do it with as little memory as possible
        lessThanTargetCount = 0
        greaterThanTargetCount = 0
        eqTargetCount = 0
        for n in nums:
            lessThanTargetCount += 1 if n < target else 0
            greaterThanTargetCount += 1 if n > target else 0
            eqTargetCount += 1 if n == target else 0

        resp = []
        for i in range(lessThanTargetCount, lessThanTargetCount + eqTargetCount):
            resp.append(i)
        
        return(resp)
```