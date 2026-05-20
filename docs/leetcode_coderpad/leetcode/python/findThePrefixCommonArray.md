---
title: findThePrefixCommonArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findThePrefixCommonArray

```python
class Solution:
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        # C[i] equals count of numbers present at or before index i in both
        resp = []

        aVals = set()
        bVals = set()
        currOverlap = 0

        for idx in range(len(A)):
            aVal = A[idx]
            bVal = B[idx]
            if aVal in bVals:
                currOverlap += 1
            if bVal in aVals:
                currOverlap += 1
            
            if aVal == bVal:
                currOverlap += 1

            resp.append(currOverlap)
            aVals.add(aVal)
            bVals.add(bVal)
        
        return(resp)
```