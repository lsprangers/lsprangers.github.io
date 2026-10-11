---
title: intersectionOfTwoArraysII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# intersectionOfTwoArraysII

```python
class Solution:
    def intersect(self, nums1: list[int], nums2: list[int]) -> list[int]:
        # sort and iterate would be longer runtime, but smaller memory
        # frequency counting would be shorter runtime but larger memory
        #   we can do this because it allows for any order
        f1 = collections.Counter(nums1)
        f2 = collections.Counter(nums2)
        
        resp = []
        
        for k1, v1 in f1.items():
            if k1 not in f2:
                continue
            
            v2 = f2[k1]
            freq = min(v1, v2)
            for _ in range(freq):
                resp.append(k1)
        
        return(resp)
```