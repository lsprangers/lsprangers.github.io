---
title: productOfArrayExceptSelf2
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# productOfArrayExceptSelf2

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        totalNonZeroProduct = 1
        totalProduct = 1
        zeros_idx = []
        # O(n) time space
        for idx, num in enumerate(nums):
            if num != 0:
                totalNonZeroProduct *= num
            else:
                zeros_idx.append(idx)
            totalProduct *= num
        
        # O(n) time space
        if len(zeros_idx) > 1:
            resp = [0] * len(nums)

        elif len(zeros_idx) == 1:
            resp = []
            for num in nums:
                if num == 0:
                    resp.append(totalNonZeroProduct)
                else:
                    resp.append(0)
        else:
            resp = [totalProduct // num for num in nums]
                

        return(resp)
```