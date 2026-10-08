---
title: removeOuterParentheses
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# removeOuterParentheses

```python
class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        primitives = []
        bal = 0
        curr = []
        for _char in s:
            bal += 1 if _char == '(' else -1
            curr.append(_char)
            if bal == 0:
                primitives.append(curr)
                curr = []
        
        resp = deque([])
        while primitives:
            thisPrimitive = primitives.pop()
            bal = 1
            curr = []
            for _char in thisPrimitive[1:]:
                bal += 1 if _char == '(' else -1
                if bal > 0:
                    curr.append(_char)
            
            resp.appendleft("".join(curr))
        
        return("".join(resp))
```