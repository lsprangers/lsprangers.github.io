---
title: maxAreaRectangleWithPointConstraints1
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxAreaRectangleWithPointConstraints1

```python
class Solution:
    def maxRectangleArea(self, points: List[List[int]]) -> int:
        x_to_y = defaultdict(set)

        # some folks sorting this and directly checking 4 adjacent points - if they don't form 
        #   a rectangle, then any other rectangle formed with those left points would have a point inside
        points.sort()

        for x, y in points:
            x_to_y[x].add(y)
        
        resp = -float("inf")
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]

                # valid diagonal
                if x1 != x2 and y1 != y2 and y2 in x_to_y[x1] and y1 in x_to_y[x2]:
                    found_bad = False
                    for potential_bad_x, y_list in x_to_y.items():
                        if x1 <= potential_bad_x <= x2:
                            for potential_bad_y in y_list:
                                if min(y1, y2) <= potential_bad_y <= max(y1, y2):
                                    if (potential_bad_x, potential_bad_y) not in ((x1, y1), (x2, y2), (x1, y2), (x2, y1)):
                                        found_bad = True
                                        break

                    if not found_bad:
                        resp = max(resp, abs(x2 - x1) * abs(y2 - y1))

        return(resp if resp != -float("inf") else -1)
```