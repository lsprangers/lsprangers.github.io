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
        s = s.strip()
        sList = s.split()
        left = 0
        right = len(sList) - 1
        while left <= right:
            sList[left], sList[right] = sList[right], sList[left]

            left += 1
            right -= 1
        
        return(" ".join(sList))
```