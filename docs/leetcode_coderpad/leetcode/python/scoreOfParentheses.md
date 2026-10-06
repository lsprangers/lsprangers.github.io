---
title: scoreOfParentheses
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# scoreOfParentheses

```python
class Solution:
    def scoreOfParentheses(self, s: str) -> int:
        # once we reach a balanced item we need to remove it and add score to stack
        # we'll drain stack and add together, and then we'd need to drain stack for inside multiplier

        # ((())()())
        # turns into
        #   (()) + () + ()
        # inside of outer ()

        # ( ()() )
        # [4]
        stack = []
        for idx, _char in enumerate(s):
            if _char == '(':
                stack.append(_char)
            else:
                if stack[-1] == '(':
                    stack.pop()
                    stack.append('1')
                else:
                    curr = 0
                    while stack[-1].isnumeric():
                        curr += int(stack.pop())

                    # get the (
                    stack.pop()
                    stack.append(str(2 * curr))

        resp = 0
        while stack:
            c = stack.pop()
            if not c.isnumeric():
                return(-1)
            
            resp += int(c)
        
        return(resp)
        
```