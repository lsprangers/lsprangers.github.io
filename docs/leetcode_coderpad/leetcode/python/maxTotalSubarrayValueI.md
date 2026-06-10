---
title: maxTotalSubarrayValueI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxTotalSubarrayValueI

```python
class Solution:
    def maxTotalValue(self, nums: List[int], k: int) -> int:
        maxx = max(nums)
        minn = min(nums)
        return((maxx - minn) * k)
```