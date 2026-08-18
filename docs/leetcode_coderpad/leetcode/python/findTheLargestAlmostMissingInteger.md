---
title: findTheLargestAlmostMissingInteger
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findTheLargestAlmostMissingInteger

```python
class Solution:
    def largestInteger(self, nums: List[int], k: int) -> int:
        resp = -1
        n = len(nums)

        freqs = defaultdict(int)
        
        # if k  < n, only the ends can be involved because the middle values will all have count = k
        for left in range(n - k + 1):
            intsInvolved = set()
            for i in range(left, left + k):
                intsInvolved.add(nums[i])
            
            for involved in intsInvolved:
                freqs[involved] += 1
            
        
        for n, v in freqs.items():
            if v == 1:
                resp = max(resp, n)
        
        return(resp)
```