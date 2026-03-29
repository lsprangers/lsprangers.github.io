---
title: reverseWordsInString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseWordsInString
`word[::-1]` is the most efficient way to reverse a string - don't do stack append + pop into helper, although that's faster than `reversed(word)`

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.split(" ")
        resp = []
        for word in words:
            resp.append(word[::-1])
        
        return(" ".join(resp))
```