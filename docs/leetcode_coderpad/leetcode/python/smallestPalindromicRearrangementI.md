---
title: smallestPalindromicRearrangementI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestPalindromicRearrangementI

```python
class Solution:
    def smallestPalindrome(self, s: str) -> str:
        # since it's guaranteed to be palindrome, we can just 
        #   find the palindrome for half of it
        midIdx = len(s) // 2
        leftHalf = sorted(s[ : midIdx])

        # if mid exists, it must be the % 2 == 1 frequency
        #   item. And only one can exist
        # It must also be the middle of the response then

        mid = [s[midIdx]] if len(s) % 2 == 1 else []
        rightHalf = leftHalf[::-1]

        return("".join(leftHalf + mid + rightHalf))
```