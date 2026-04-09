---
title: longestConsecutiveSubsequence
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestConsecutiveSubsequence

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)

        resp = 0
        for num in numSet:
            # can't be starter
            if num - 1 in numSet:
                continue
            
            currLen = 0
            currNum = num
            while currNum in numSet:
                currLen += 1
                currNum += 1
        
            resp = max(resp, currLen)
        
        return(resp)
```