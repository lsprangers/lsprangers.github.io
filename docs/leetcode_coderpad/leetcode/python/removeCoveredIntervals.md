---
title: removeCoveredIntervals
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# removeCoveredIntervals

```python
class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # sort by first item, then second - if tied one gets removed
        intervals.sort(key=lambda x: (x[0], -x[1]))
        n = len(intervals)

        # [1,4],[1,2],[3,4]
        idx = 0
        resp = 0
        while idx < n:
            checkIdx = idx + 1
            while checkIdx < n and intervals[idx][0] <= intervals[checkIdx][0] and intervals[idx][1] >= intervals[checkIdx][1]:
                checkIdx += 1
            
            idx = checkIdx
            resp += 1
        
        return(resp)

```