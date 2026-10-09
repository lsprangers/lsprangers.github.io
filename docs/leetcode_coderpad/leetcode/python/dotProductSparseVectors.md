---
title: dotProductSparseVectors
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# dotProductSparseVectors

```python
class SparseVector:
    def __init__(self, nums: List[int]):
        self.sparse = {}
        for idx, num in enumerate(nums):
            self.sparse[idx] = num
        

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        resp = 0
        for idx in self.sparse.keys():
            if idx in vec.sparse:
                resp += self.sparse[idx] * vec.sparse[idx]
        
        return(resp)


# Your SparseVector object will be instantiated and called as such:
# v1 = SparseVector(nums1)
# v2 = SparseVector(nums2)
# ans = v1.dotProduct(v2)
```
