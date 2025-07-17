---
title: topKFrequentElements
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# topKFrequentElements

```python
#  347
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        int_to_count = [(-count, x) for x, count in Counter(nums).items()]
        heapify(int_to_count)

        resp = []
        while len(resp) < k:
            resp.append(heappop(int_to_count)[1])
        return(resp)```
