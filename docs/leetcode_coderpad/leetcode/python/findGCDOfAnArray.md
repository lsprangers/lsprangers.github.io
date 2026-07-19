---
title: findGCDOfAnArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findGCDOfAnArray

```python
class Solution:
    def findGCD(self, nums: List[int]) -> int:
        return(math.gcd(min(nums), max(nums)))
```