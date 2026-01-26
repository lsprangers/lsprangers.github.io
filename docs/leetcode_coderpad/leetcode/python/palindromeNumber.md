---
title: palindromeNumber
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# palindromeNumber

```python
# 9 
class Solution:
    def isPalindrome(self, x: int) -> bool:
        strx = str(x)
        lenx = len(strx)
        for i in range(lenx // 2):
            if strx[i] == strx[lenx - i - 1]:
                continue
            return False
        
        return True
        ```
