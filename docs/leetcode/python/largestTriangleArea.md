---
title: largestTriangleArea
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# largestTriangleArea

```python
class Solution:
    def largestTriangleArea(self, points: List[List[int]]) -> float:
        # find largest base and height

        # combinations as ordering isn't unique
        resp = -float("inf")
        for combo in itertools.combinations(points, 3):

            # (x1, y1), (x2, y2), and (x3, y3) 
            # 1/2 * |x1(y2 − y3) + x2(y3 − y1) + x3(y1 − y2)|
            resp = max(
                resp,
                0.5 * abs(
                    (combo[0][0] * (combo[1][1] - combo[2][1])) +
                    (combo[1][0] * (combo[2][1] - combo[0][1])) +
                    (combo[2][0] * (combo[0][1] - combo[1][1]))
                )
            )
        
        return(resp)
```