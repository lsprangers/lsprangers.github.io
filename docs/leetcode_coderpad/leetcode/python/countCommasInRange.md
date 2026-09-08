---
title: countCommasInRange
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countCommasInRange

```python
class Solution:
    def countCommas(self, n: int) -> int:
        # 1 x number in thousands, ten thousands, hundred thousands
        # 2 x number in millions, ten millions, hundred millions

        resp = 0
        while n > 0:
            currCommaCount = math.floor(math.log(n, 1000))
            # smallest number with currCommaCount commas
            currFloor = 1000 ** currCommaCount
            nNumbersInRange = n - currFloor + 1
            resp += (nNumbersInRange * currCommaCount)
            # 999,999
            n = currFloor - 1
            
        
        return(resp)
```