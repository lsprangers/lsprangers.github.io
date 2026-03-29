---
title: minimumSizeSubarraySum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumSizeSubarraySum

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        right = 0
        curr = 0
        resp = float("inf")

        # [2,3,1,2,4,3]
        while right < len(nums):
            # 8,    0, 3
            curr += nums[right]

            
            while curr >= target:
                # 4
                resp = min(resp, right - left + 1)
                curr -= nums[left]
                left += 1
            
            right += 1
        
        return(0 if resp == float("inf") else resp)
```