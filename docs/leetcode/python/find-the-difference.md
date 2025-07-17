---
title: find-the-difference
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# find-the-difference

```python
class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        for sl in s:
            if sl in t:
                t = t.replace(sl, "", 1)
        return t```
