---
title: rectangleOverlap
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# rectangleOverlap

```python
class Solution:
    def isRectangleOverlap(self, rec1: List[int], rec2: List[int]) -> bool:
        # x x x
        # x x x
        # x x x     # 
        
        lower = []
        higher = []
        lefter = []
        righter = []
        # which one is lower
        if rec1[1] < rec2[1]:
            lower = rec1
            higher = rec2
        else:
            lower = rec2
            higher = rec1
        
        if rec1[0] < rec2[0]:
            lefter = rec1
            righter = rec2
        else:
            lefter = rec2
            righter = rec1
        
        # if lower ones top is not overlapping with higher ones bottom
        # or lefter's right side is not overlapping with righter's left side
        if (lower[3] <= higher[1]) or (lefter[2] <= righter[0]):
            return(False)
        
        return(True)
```