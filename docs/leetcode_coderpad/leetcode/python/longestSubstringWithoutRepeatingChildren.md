---
title: longestSubstringWithoutRepeatingChildren
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestSubstringWithoutRepeatingChildren

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        resp = 0
        seen = set()
        for right in range(len(s)):
            
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            
            seen.add(s[right])
            resp = max(resp, right - left + 1)
        
        return(resp)
```