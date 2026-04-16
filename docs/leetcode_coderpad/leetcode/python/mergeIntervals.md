---
title: mergeIntervals
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# mergeIntervals

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        n = len(intervals)
        if n < 2:
            return(intervals)

        # sort based on first key then second
        intervals.sort(key = lambda x: (x[0], x[1]))

        resp = []
        currStart, currEnd = intervals[0][0], intervals[0][1]
        for intervalStart, intervalEnd in intervals:
            # we sorted by start, so we just need to check if new start earlier than our end
            if intervalStart <= currEnd:
                currEnd = max(currEnd, intervalEnd)
            
            else:
                resp.append([currStart, currEnd])
                currStart, currEnd = intervalStart, intervalEnd
        
        resp.append([currStart, currEnd])

        return(resp)
```