---
title: maximumSubarrayWithEqualProducts
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumSubarrayWithEqualProducts

```python
class Solution:
    def maxLength(self, nums: List[int]) -> int:
        resp = 0
        for left in range(len(nums)):
            for right in range(left, len(nums)):
                p = math.prod(nums[left : right + 1])
                l = math.lcm(*nums[left : right + 1])
                g = math.gcd(*nums[left : right + 1])
                if p == l * g:
                    resp = max(
                        resp,
                        right - left + 1
                    )
                elif p < l * g:
                    continue
                else:
                    break
        
        return(resp)
```