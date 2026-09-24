---
title: smallestIndexWithDigitSumEqualToIndex
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestIndexWithDigitSumEqualToIndex

```python
class Solution:
    def smallestIndex(self, nums: List[int]) -> int:
        for idx, num in enumerate(nums):
            if self.sumOfDigit(num) == idx:
                return(idx)
        
        return(-1)
    
    def sumOfDigit(self, num):
        resp = 0
        while num:
            currDigit = num % 10
            num //= 10
            resp += currDigit
        
        return(resp)
```