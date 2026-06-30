---
title: numberOfSubstringsContainingAllThreeCharacters
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfSubstringsContainingAllThreeCharacters

```python
class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        left = right = resp = 0
        freq = [0, 0, 0]

        while right < len(s):
            freq[ord(s[right]) - ord("a")] += 1

            while all(f > 0 for f in freq):
                resp += len(s) - right
                freq[ord(s[left]) - ord("a")] -= 1
                left += 1
        
            right += 1

        return(resp)
```