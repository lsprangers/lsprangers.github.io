---
title: convertToBase7
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# convertToBase7

```python
class Solution:
    def convertToBase7(self, num: int) -> str:
        isNeg = num < 0
        num = abs(num)
        
        p = 0
        while 7**(p+1) <= num:
            p += 1
        
        
        resp = []
        if isNeg:
            resp.append("-")
        
        while p > -1:
            b = (7**p)
            mult = num // b
            resp.append(str(mult))
            num -= (mult * b)
            p -= 1
        
        return("".join(resp))
```