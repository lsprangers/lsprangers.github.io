---
title: smallestMissingMultipleOfK
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestMissingMultipleOfK

```python
class Solution:
    def missingMultiple(self, nums: List[int], k: int) -> int:
        numSet = set(nums)
        mult = 1
        while mult * k in numSet:
            mult += 1
        
        return(mult * k)
```