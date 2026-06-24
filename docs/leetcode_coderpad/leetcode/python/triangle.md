---
title: triangle
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# triangle

```python
class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        nRows = len(triangle)

        @cache
        def dfs(row, idx):
            if row == nRows - 1:
                return(triangle[row][idx])
            
            left = dfs(row + 1, idx)
            right = dfs(row + 1, idx + 1)
            return(triangle[row][idx] + min(left, right))

        return(dfs(0, 0))
```