---
title: sumOfGCDOfFormedPairs
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# sumOfGCDOfFormedPairs

```python
class Solution:
    def gcdSum(self, nums: list[int]) -> int:
        pfxMax = [nums[0]]
        pfxGCD = [nums[0]]
        for num in nums[1:]:
            pfxMax.append(
                max(
                    pfxMax[-1],
                    num
                )
            )
            pfxGCD.append(math.gcd(num, pfxMax[-1]))
        

        pfxGCD.sort()
        
        left = 0
        right = len(pfxGCD) - 1
        resp = 0

        while left < right:
            lNum = pfxGCD[left]
            rNum = pfxGCD[right]
            resp += math.gcd(lNum, rNum)
            left += 1
            right -= 1
        
        return(resp)
```