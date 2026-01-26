---
title: isSubsequence
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# isSubsequence

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        sptr = 0
        tptr = 0
        while sptr <= tptr and sptr < len(s) and tptr < len(t):
            if s[sptr] == t[tptr]:
                sptr += 1
            
            tptr += 1
        
        return(sptr == len(s))
```