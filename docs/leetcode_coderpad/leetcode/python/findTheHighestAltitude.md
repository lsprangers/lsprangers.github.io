---
title: findTheHighestAltitude
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findTheHighestAltitude

```python
# 1732
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        resp = 0
        pfxSum = [0]
        for next_gain in gain:
            curr = next_gain + pfxSum[-1]
            resp = max(resp, curr)
            pfxSum.append(curr)
        
        return(resp)
```
