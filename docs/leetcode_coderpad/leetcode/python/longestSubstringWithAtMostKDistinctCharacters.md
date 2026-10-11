---
title: longestSubstringWithAtMostKDistinctCharacters
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestSubstringWithAtMostKDistinctCharacters

```python
class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        if k == 0:
            return(0)
        
        resp = 0
        left = 0
        freqs = defaultdict(int)
        
        for right in range(len(s)):
            freqs[s[right]] += 1
            while left < right and len(freqs.keys()) > k:
                freqs[s[left]] -= 1
                if freqs[s[left]] == 0:
                    freqs.pop(s[left])
                
                left += 1
            
            resp = max(resp, right - left + 1)
        
        return(resp)
```