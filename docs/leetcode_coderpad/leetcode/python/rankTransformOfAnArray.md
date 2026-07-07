---
title: rankTransformOfAnArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# rankTransformOfAnArray

```python
class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        seen = set()
        minHeap = []
        numToIdx = defaultdict(list)        
        for idx, num in enumerate(arr):
            if num not in seen:
                heapq.heappush(minHeap, num)
                seen.add(num)
            
            numToIdx[num].append(idx)
        

        resp = [0] * len(arr)
        
        currRank = 1
        while minHeap:
            currSmallest = heapq.heappop(minHeap)
            for numIdx in numToIdx[currSmallest]:
                resp[numIdx] = currRank
            
            currRank += 1
        
        return(resp)
        
```