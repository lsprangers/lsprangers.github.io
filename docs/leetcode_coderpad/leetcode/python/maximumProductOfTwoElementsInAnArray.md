---
title: maximumProductOfTwoElementsInAnArray
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumProductOfTwoElementsInAnArray

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:

        # O(n) - avoid the bullshit
        for idx in range(len(nums)):
            nums[idx] -= 1
        
        # O(n logn)
        nums.sort()

        # Either the last two if all positive
        #   or the first two if two negatives
        return(max(
            nums[-2] * nums[-1],
            nums[0] * nums[1]
        ))
```