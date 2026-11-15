---
title: numberOfSubarraysWithOddSum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfSubarraysWithOddSum

```python
class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        # need to find number of subarrays where
        #   count of odds is odd itself. 1, 3, 5
        #   etc are all valid

        # prefix sum template should work, but we track
        #   the total count of odd numbers

        # we just need to track 0 or 1

        # [1,2,3,4,5,6,7]
        # [1,1,2,2,3,3,4]
        # [2,3,4,5]
        # [0,1,1,2]
        lookups = {0: 1, 1: 0}
        currCount = 0
        resp = 0
        for num in arr:
            currCount += 1 if num % 2 == 1 else 0
            
            # if currCount is 1 we need 0, vice versa
            need = 1 - (currCount % 2)
            resp += lookups[need]
            lookups[currCount % 2] += 1
        
        return(resp % ((10**9) + 7))
```