---
title: minimumRectanglesToCoverPoints
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumRectanglesToCoverPoints

```python
class Solution:
    def minRectanglesToCoverPoints(self, points: List[List[int]], w: int) -> int:
        # greedy? Trying to think of when greedy would be incorrect
        # dq = deque(points)

        # O(n)
        heapq.heapify(points)
        
        n_rectangles = 0

        # O(n) - while
        # O(log n) - heapqheappop
        # O(n log n) total
        while points:
            curr_x, curr_y = heapq.heappop(points)
            # max_y = curr_y

            while points and abs(points[0][0] - curr_x) <= w:
                other_x, other_y = heapq.heappop(points)
                # max_y = max(max_y, curr_y)
            
            n_rectangles += 1
        
        return(n_rectangles)
```