---
title: totalWavinessOfNumbersInRangeI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# totalWavinessOfNumbersInRangeI

```python
class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        # peak greater than both neighbors
        # valley less than both neighbors
        # first and last can't be peaks / valleys
        # Any number with 3 digits has waviness of 0
        # Waviness is total peaks and valleys

        def waviness(num: int) -> int:
            if num < 100:
                return(0)
            

            resp = 0

            # walk from ones backwards
            prevPrev = num % 10
            num //= 10
            prev = num % 10
            num //= 10
            while num:
                curr = num % 10
                num //= 10
                if curr < prev > prevPrev:
                    resp += 1
                elif curr > prev < prevPrev:
                    resp += 1
                
                prevPrev = prev
                prev = curr
            
            return(resp)


        resp = 0
        for currNum in range(num1, num2 + 1):
            resp += waviness(currNum)
        
        return(resp)
```