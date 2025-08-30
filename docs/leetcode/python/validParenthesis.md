---
title: validParenthesis
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# validParenthesis

```python
class Solution:
    def isValid(self, s: str) -> bool:
        closures = set([')', '}', ']'])
        closure_mapping = {
            ')': '(',
            '}': '{',
            ']': '[',      
        }

        stack = []
        for c in s:
            if c in closures:
                if stack and stack[-1] == closure_mapping[c]:
                    stack.pop()
                else:
                    return(False)
            else:
                stack.append(c)
        
        return(len(stack) == 0)
```