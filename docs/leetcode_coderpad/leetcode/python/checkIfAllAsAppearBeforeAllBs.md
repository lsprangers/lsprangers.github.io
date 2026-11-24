---
title: checkIfAllAsAppearBeforeAllBs
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# checkIfAllAsAppearBeforeAllBs

```python
class Solution:
    def checkString(self, s: str) -> bool:
        lastA = None
        firstOther = None

        for idx, _char in enumerate(s):
            if _char == 'a':
                lastA = idx
            
            elif firstOther == None:
                firstOther = idx
        
        if lastA == None or firstOther == None:
            return(True)
        
        return(firstOther > lastA)
```