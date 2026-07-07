---
title: concatenateNonZeroDigitsAndMultiplyBySumI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# concatenateNonZeroDigitsAndMultiplyBySumI

```python
class Solution:
    def sumAndMultiply(self, n: int) -> int:
        concat = 0
        summ = 0
        currPow = 0
        while n:
            currInt = n % 10
            n //= 10
            if currInt == 0:
                continue

            concat += (currInt * (10 ** currPow))
            currPow += 1
            summ += currInt
        
        return(concat * summ)

```