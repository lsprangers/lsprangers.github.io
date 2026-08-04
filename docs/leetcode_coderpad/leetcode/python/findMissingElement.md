---
title: findMissingElement
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findMissingElement

```python
class Solution:
    def findMissingElements(self, nums: List[int]) -> List[int]:
        smallest = min(nums)
        largest = max(nums)
        seen = set(nums)
        resp = []
        for n in range(smallest, largest + 1):
            if n not in seen:
                resp.append(n)
        
        return(resp)
```