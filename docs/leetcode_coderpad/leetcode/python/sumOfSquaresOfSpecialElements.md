---
title: sumOfSquaresOfSpecialElements
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# sumOfSquaresOfSpecialElements

```python
class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        resp = 0
        n = len(nums)
        for idx, num in enumerate(nums):
            if n % (idx + 1) == 0:
                resp += (num * num)
        
        return(resp)
```