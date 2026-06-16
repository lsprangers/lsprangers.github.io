---
title: processStringWithSpecialOperationsI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# processStringWithSpecialOperationsI

```python
class Solution:
    def processStr(self, s: str) -> str:
        resp = []
        for idx in range(len(s)):
            c = s[idx]
            if c.isalpha():
                resp.append(c)
            elif c == "*" and resp:
                resp.pop()
            elif c == "#":
                resp = resp + resp
            elif c == "%":
                resp = resp[::-1]
        
        return("".join(resp))
```