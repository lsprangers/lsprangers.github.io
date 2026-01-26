---
title: gcdOfStrings
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# gcdOfStrings

```python
# 1071
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # check if there's a pattern
        if str1 + str2 != str2 + str1:
            return("")
        
        # if there's a pattern, get the length of it
        pattern_length = gcd(len(str1), len(str2))

        return str1[0 : pattern_length]```
