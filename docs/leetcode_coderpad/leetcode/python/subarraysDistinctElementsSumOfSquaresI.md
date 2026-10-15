---
title: subarraysDistinctElementsSumOfSquaresI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# subarraysDistinctElementsSumOfSquaresI

```python
class Solution:
    def sumCounts(self, nums: List[int]) -> int:
        # just need to generate every subarray possible
        #   for each subarray want to easily count the number
        #   of distinct elements
        n = len(nums)
        resp = 0

        for i in range(n):
            for j in range(i, n):
                resp += (len(set(nums[i : j + 1])))**2
        
        return(resp)
```