---
title: slidingWindowMaximum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# slidingWindowMaximum

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # how to keep track of window max efficiently?
        maxHeap = []
        n = len(nums)
        
        # initial addition
        if n <= k:
            return([max(nums)])
        
        for idx in range(k):
            num = nums[idx]
            heapq.heappush(maxHeap, (-num, idx))
        
        
        resp = [-maxHeap[0][0]]
        for idx in range(k, n):
            num = nums[idx]
            heapq.heappush(maxHeap, (-num, idx))
            
            while maxHeap and maxHeap[0][1] < idx - (k - 1):
                heapq.heappop(maxHeap)
            
            resp.append(-maxHeap[0][0])
            
        return(resp)
            
            
```