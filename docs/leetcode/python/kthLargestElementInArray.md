---
title: kthLargestElementInArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# kthLargestElementInArray

```python
#  215
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        
        return(heap[0])```
