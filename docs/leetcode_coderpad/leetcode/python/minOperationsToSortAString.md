---
title: minOperationsToSortAString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minOperationsToSortAString

```python
class Solution:
    def minOperations(self, s: str) -> int:
        # darc -> da , rc -> ad , cr
        # doesn't work, we then need to swap
        #   a dc r
        # dbrca -> abcdr
        # bd acr
        # b acdr
        # ab cdr

        # if you can get the min or the max to either side
        #   and then sort the resulting other one, it's just 1 or 2
        #   every single time

        # You basically just need to figure out how many operations to
        #   get min or max to ends, and then add one more

        minChar = min(s)
        maxChar = max(s)
        resp = 0

        if len(s) < 3:
            return(0 if list(s) == sorted(s) else -1)
        
        if s[0] == minChar or s[-1] == maxChar:
            # O(n)
            return(0 if list(s) == sorted(s) else 1)
        
        # if anywhere in the middle has the min or max
        for idx in range(1, len(s) - 1):
            if s[idx] == minChar or s[idx] == maxChar:
                return(2)
        
        return(3)
```