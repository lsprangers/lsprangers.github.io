---
title: reverseVowelsOfAString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseVowelsOfAString

```python
# 345
class Solution:
    def reverseVowels(self, s: str) -> str:
        resp = [*s]
        vowels = set(["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"])

        # O(n)
        vowel_idxs = []
        for idx, ch in enumerate(s):
            if ch in vowels:
                vowel_idxs.append(idx)
        
        # O(n)
        left = 0
        right = len(vowel_idxs) - 1
        while left < right:
            tmp = resp[vowel_idxs[left]]
            resp[vowel_idxs[left]] = resp[vowel_idxs[right]]
            resp[vowel_idxs[right]] = tmp
            left += 1
            right -= 1
        
        # O(n) again, space O(n) which can probably get reduced but Python strings suck
        return("".join(resp))
```
