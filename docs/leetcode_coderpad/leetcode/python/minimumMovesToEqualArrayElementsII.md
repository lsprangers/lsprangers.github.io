---
title: minimumMovesToEqualArrayElementsII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumMovesToEqualArrayElementsII

```python
class Solution:
    def minMoves2(self, nums: list[int]) -> int:
        # [1,1,1,1,1,1,8]
        # median = 1
        # I don't know how to prove that the median is the right number
        #   it just feels like that's the right number
        # The median minimizes the sum of absolute differences
        #   so moving 6 number 1's towards something else costs more
        #   than moving the single 8 down to the 1's
        # If we chose 2, we know we'd need to do 6 increases to 2, and in doing
        #   so we only save 1 single 8 reduction (go to 2 instead of 1)
        #   so we need to find the optimal point of reducing the sum of absolute
        #   differences
        median = statistics.median(nums)
        resp = 0
        for n in nums:
            resp += abs(median - n)
        
        return(int(resp))

```