---
title: maxNumberOfVowelsInASubstringOfGivenLength
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxNumberOfVowelsInASubstringOfGivenLength

```python
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = set(['a', 'e', 'i', 'o', 'u'])
        if len(s) < k:
            return(
                sum([1 for c in s if c in vowels])
            )
        
        curr_count = sum([1 for c in s[0:k] if c in vowels])
        resp = curr_count
        for idx in range(k, len(s)):
            curr_count -= 1 if s[idx - k] in vowels else 0
            curr_count += 1 if s[idx] in vowels else 0
            resp = max(resp, curr_count)
        
        return(resp)
```