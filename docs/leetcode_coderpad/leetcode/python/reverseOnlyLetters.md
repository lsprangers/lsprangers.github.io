---
title: reverseOnlyLetters
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseOnlyLetters

```python
class Solution:
    def reverseOnlyLetters(self, s: str) -> str:
        s_l = [c for c in s if c.isalpha()]
        resp = []
        for c in s:
            if c.isalpha():
                resp.append(s_l.pop())
            else:
                resp.append(c)
        
        return("".join(resp))
```