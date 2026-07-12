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

```python
class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        # minHeap would be O(n) to build, then for every item (n) do O(log n) pop so O(n logn). O(n) SC
        # copying array, sorting, and iterating would be O(n) + O(n logn) + O(n) with O(n) space

        # O(2n)
        minHeap = [(arr[idx], idx) for idx, num in enumerate(arr)]
        heapq.heapify(minHeap)

        # O(n logn)
        currRank = 1
        currElem = None
        while minHeap:
            num, idx = heapq.heappop(minHeap)
            if currElem != None and currElem != num:
                currRank += 1
            
            arr[idx] = currRank
            currElem = num
        
        return(arr)
```

```python
class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        arrCopy = [(num, idx) for idx, num in enumerate(arr)]
        arrCopy.sort(key=lambda x: x[0])

        currRank = 1
        currElem = None
        for num, idx in arrCopy:
            if currElem != None and currElem != num:
                currRank += 1
            
            currElem = num
            arr[idx] = currRank
        
        return(arr)
```