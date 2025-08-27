---
title: reverseWordsInAString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseWordsInAString
151

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        words = s.strip().split(" ")
        words = [word for word in words if word != '']

        # 4/2 = 2, 5/2 = 2 - if it's even we'll be 1 over
        mid = len(words) // 2

        # 0, 1 for even - good to switch
        # 0, 1 for odd - also good to switch
        for idx in range(mid):
            tmp = words[idx]
            words[idx] = words[len(words) - idx - 1]
            words[len(words) - idx - 1] = tmp
        
        return(" ".join(words))
```