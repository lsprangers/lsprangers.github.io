---
title: maximumNestingDepthOfParentheses
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumNestingDepthOfParentheses

```python
class Solution:
    def maxDepth(self, s: str) -> int:
        resp = 0
        curr = 0
        for _char in s:
            if _char == '(':
                curr += 1
            elif _char == ')':
                curr -= 1
            
            resp = max(resp, curr)
        
        return(resp)
```