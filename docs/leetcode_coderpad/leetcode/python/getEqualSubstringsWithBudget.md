---
title: getEqualSubstringsWithBudget
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# getEqualSubstringsWithBudget

```python
class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        left = 0
        curr = 0
        resp = 0
        for right in range(len(s)):
            curr += abs(ord(s[right]) - ord(t[right]))
            while curr > maxCost:
                curr -= abs(ord(s[left]) - ord(t[left]))
                left += 1
            
            resp = max(resp, right - left + 1)
        
        return(resp)
```