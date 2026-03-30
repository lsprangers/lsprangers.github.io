---
title: guessNumberHigherLower
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# guessNumberHigherLower

Updated to use the `[left, right)` setup:
```python
class Solution:
    def guessNumber(self, n: int) -> int:
        left = 0
        right = n + 1 # [left, right)
        
        while left < right:
            mid = left + (right - left) // 2
            g_resp = guess(mid)
            if g_resp == 0:
                return(mid)
            
            # mid higher than chosen number
            elif g_resp == -1:
                right = mid   # [left, mid)
            else:
                left = mid + 1 # mid for sure isn't in, so [mid + 1, right)
        
        return(left)
```


```python
# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        left = 1
        right = n

        while left <= right:
            mid = left + (right - left) // 2
            
            resp = guess(mid)

            if resp < 0:
                right = mid - 1
            elif resp > 0:
                left = mid + 1
            else:
                return(mid)
        
        return(left)
```