---
title: maxNumberOfKSumPairs
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxNumberOfKSumPairs

```python
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        idxs = defaultdict(list)

        for idx, num in enumerate(nums):
            idxs[num].append(idx)
        
        resp = 0
        for idx, num in enumerate(nums):
            if idxs[num] and idxs[k - num]:
                if num == k - num and len(idxs[num]) < 2: continue
                idxs[num].pop()
                idxs[k - num].pop()
                resp += 1
        
        return(resp)
```