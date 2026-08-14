---
title: maximumLengthSubstringWithTwoOccurrences
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumLengthSubstringWithTwoOccurrences

```python
class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        left = 0
        freqs = defaultdict(int)
        resp = 0

        for right in range(len(s)):
            _char = s[right]
            freqs[_char] += 1
            while left <= right and freqs[_char] > 2:
                freqs[s[left]] -= 1
                left += 1
            
            resp = max(right - left + 1, resp)

        return(resp)
```