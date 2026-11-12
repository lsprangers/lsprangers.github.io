---
title: longestStrictlyIncreasingOrStrictlyDecreasingSubsequence
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestStrictlyIncreasingOrStrictlyDecreasingSubsequence

```python
class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        curr = 1
        resp = 1
        while curr < len(nums):
            if nums[curr] == nums[curr - 1]:
                curr += 1
                continue
            
            tmp = curr
            inc = nums[curr] > nums[curr - 1]
            while tmp < len(nums):
                if inc and nums[tmp] > nums[tmp - 1]:
                    tmp += 1
                elif not inc and nums[tmp] < nums[tmp - 1]:
                    tmp += 1
                else:
                    break
            resp = max(resp, tmp - curr + 1)
            curr = tmp

        return(resp)
```