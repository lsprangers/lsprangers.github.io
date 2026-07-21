---
title: shift2DGrid
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# shift2DGrid

```python
class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        # 3x4
        nRows = len(grid)
        nCols = len(grid[0])

        # 12
        totalEntries = (nRows * nCols)

        # O(R x W) space to just do a single pass calculation
        resp = [[None] * nCols for _ in range(nRows)]

        for currRow in range(nRows):
            for currCol in range(nCols):
                numPlaceholder = grid[currRow][currCol]

                currIdx = currRow * nCols + currCol
                newIdx = (currIdx + k) % totalEntries
                newCol = newIdx % nCols
                newRow = newIdx // nCols

                resp[newRow][newCol] = numPlaceholder

        return(resp)
```