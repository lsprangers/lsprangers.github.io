---
title: reverseParentheses
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseParentheses

```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        # (ed(et(oc))el)
        # [[], [edocte], [el]]
        # (abcd)
        # [[dcba]]
        revStack = []
        curr = []
        for _char in s:
            if _char == "(":
                revStack.append(curr)
                curr = []
            elif _char == ")":
                revStack[-1] = revStack[-1] + curr[::-1]
                curr = revStack[-1]
                revStack.pop()
            else:
                curr.append(_char)

        return("".join(curr))
                
            
```