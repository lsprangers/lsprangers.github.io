---
title: searchInsertPosition
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# searchInsertPosition

```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        return(bisect.bisect_left(nums, target))
```