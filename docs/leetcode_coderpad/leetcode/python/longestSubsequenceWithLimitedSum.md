---
title: longestSubsequenceWithLimitedSum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestSubsequenceWithLimitedSum

```python
class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        # [4,5,2,1]
        # [3,10,21]
        
        # [1,2,4,5]
        nums.sort()
        # [1,3,7,12]
        pfx_sum = [nums[0]]
        for n in nums[1:]:
            pfx_sum.append(pfx_sum[-1] + n)
        
        resp = []
        for query in queries:
            pfx_sum_idx = bisect.bisect_right(pfx_sum, query)
            
            resp.append(pfx_sum_idx)
        
        # should be [2,3,4]
        return(resp)
```