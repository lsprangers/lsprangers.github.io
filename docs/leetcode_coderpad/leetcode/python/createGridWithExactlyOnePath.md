---
title: createGridWithExactlyOnePath
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# createGridWithExactlyOnePath

```python
class Solution:
    def createGrid(self, m: int, n: int) -> list[str]:
        nRows = m
        nCols = n
        resp = []

        resp.append('.' * nCols)
        
        for row in range(1, nRows):
            
            resp.append(('#' * (nCols - 1)) + '.')
        
        return(resp)

```