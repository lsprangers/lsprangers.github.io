---
title: maximizeActiveSectionWithTradeI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximizeActiveSectionWithTradeI

```python
class Solution:
    def maxActiveSectionsAfterTrade(self, s: str) -> int:
        # perform a group by
        groups = [(1,0)]
        left = 0
        nOnes = 0
        while left < len(s):
            right = left
            while right < len(s) and s[left] == s[right]:
                right += 1
            
            # (key - 0 or 1, size)
            # size of 0 for augmented multipliers
            groups.append((int(s[left]), right - left))
            nOnes += groups[-1][0] * groups[-1][1]
            left = right
        
        groups.append((1, 0))
        
        # [000100111]
        # [(0,3), (1,1), (0,2), (1,3)...]
        resp = nOnes
        
        for idx in range(1, len(groups) - 1):
            if groups[idx - 1][0] == 0 and groups[idx][0] == 1 and groups[idx + 1][0] == 0:
                resp = max(resp, nOnes + groups[idx - 1][1] + groups[idx + 1][1])


        return(resp)
```