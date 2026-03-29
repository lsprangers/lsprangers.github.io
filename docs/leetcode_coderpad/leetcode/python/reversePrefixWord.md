---
title: reversePrefixWord
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reversePrefixWord

```python
class Solution:
    def reversePrefix(self, word: str, ch: str) -> str:
        stack = []
        found = False
        for c in word:
            # inclusive, append first
            stack.append(c)
            if c == ch:
                found = True
                break
        
        if not found:
            return(word)
        
        resp = []
        ch_idx = len(stack)
        while stack:
            resp.append(stack.pop())
        
        resp.append(word[ch_idx:])
        return("".join(resp))
```