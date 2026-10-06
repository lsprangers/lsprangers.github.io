---
title: minimumAddToMakeParenthesesValid
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumAddToMakeParenthesesValid

```python
class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        stack = []
        resp = 0

        for _char in s:
            if _char == '(':
                stack.append(_char)
            else:
                if stack:
                    stack.pop()
                else:
                    resp += 1
        
        resp += len(stack)
        return(resp)
```