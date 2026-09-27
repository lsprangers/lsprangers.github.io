---
title: reverseSubstringBetweenEachPairOfParentheses
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseSubstringBetweenEachPairOfParentheses

```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        stack = []
        curr = []
        for _char in s:
            if _char == '(':
                # start a new tracker
                stack.append(curr)
                curr = []
            
            elif _char == ')':
                curr = curr[::-1]
                lastSeen = stack.pop()
                lastSeen += curr
                curr = lastSeen
            
            else:
                curr.append(_char)
        
        return(
            "".join(curr)
        )
```