---
title: miinimumAreaRectangle
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# miinimumAreaRectangle

```python
class Solution:
    def minAreaRect(self, points: List[List[int]]) -> int:
        x_to_y = defaultdict(set)

        for x, y in points:
            x_to_y[x].add(y)

        resp = float("inf")

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]

                # need to check if x1, y2 and x2, y1 exist
                # also need to ensure x's and y's aren't equal, rectangle area
                #   needs to be at least 1
                if x1 != x2 and y1 != y2 and y2 in x_to_y[x1] and y1 in x_to_y[x2]:
                    resp = min(
                        resp,
                        abs(x2 - x1) * abs(y2 - y1)
                    )
        
        return(resp if resp != float("inf") else 0)
```