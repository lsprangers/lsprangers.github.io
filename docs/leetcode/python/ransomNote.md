---
title: ransomNote
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# ransomNote

```python
# 383
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        magCounter = Counter(magazine)
        for letter in ransomNote:
            if magCounter[letter] < 1:
                return(False)
            
            magCounter[letter] -= 1
        
        return(True)```
