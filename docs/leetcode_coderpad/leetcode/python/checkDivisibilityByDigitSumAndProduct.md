---
title: checkDivisibilityByDigitSumAndProduct
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# checkDivisibilityByDigitSumAndProduct

```python
class Solution:
    def checkDivisibility(self, n: int) -> bool:
        digitList = []
        nCopy = n
        
        while nCopy:
            currInt = nCopy % 10
            nCopy //= 10
            digitList.append(currInt)
        
        digitList = digitList[::-1]

        if n % (sum(digitList) + prod(digitList)) == 0:
            return(True)
        
        return(False)
```