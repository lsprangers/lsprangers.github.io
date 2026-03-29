---
title: minimumCommonValue
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumCommonValue

```python
class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        left1 = 0
        left2 = 0

        while left1 < len(nums1) and left2 < len(nums2):
            if nums1[left1] == nums2[left2]:
                return(nums1[left1])
            elif nums1[left1] < nums2[left2]:
                left1 += 1
            else:
                left2 += 1
        
        return(-1)
```