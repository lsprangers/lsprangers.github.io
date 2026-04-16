---
title: jumpGameII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# jumpGameII

## What the F
What? Who tf comes up with this and expects anyone who isn't sitting in a corner grinding leetcode to come up with this?

```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 1:
            return(0)

        resp = 0

        furthestFromCurrentJump = 0
        furthestReachableindex = 0

        # Iterate over the range of current jump, and reach furthestFromCurrentJump. Then continue
        #   iterating over reachable indexes that are larger than furthestFromCurrentJump, up to 
        #   furthestReachableindex. Skip any overlaps in the middle

        # Current jump ends when we reach index furthestFromCurrentJump, in the middle we continuously update
        #   furthestReachableindex. At the end of this current jump, increment answer and set 
        #   furthestFromCurrentJump = furthestReachableindex for the next jump

        for idx in range(n - 1):
            # nums[idx] + idx represents furthest jump landing
            furthestReachableindex = max(furthestReachableindex, nums[idx] + idx)

            if idx == furthestFromCurrentJump:
                resp += 1
                furthestFromCurrentJump = furthestReachableindex
        
        return(resp)
```

## Using DP
```python
class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 1:
            return(0)

        dp = [float("inf")] * n
        dp[n - 1] = 0
        
        # [2, 3, 1, 1, 4]
        # [2, 1, 2, 1, 0]
        # O(n)
        for idx in range(n - 2, -1, -1):
            # Potentially O(n)
            dp[idx] = 1 + min(
                dp[idx : idx + nums[idx] + 1]
            )
        
        return(dp[0])
```