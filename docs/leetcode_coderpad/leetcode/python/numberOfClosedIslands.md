---
title: numberOfClosedIslands
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfClosedIslands

```python
class Solution:
    def closedIsland(self, grid: list[list[int]]) -> int:
        self.dirs = [
            [1,0],
            [-1,0],
            [0,1],
            [0,-1]
        ]

        self.seen = set()
        self.nRows = len(grid)
        self.nCols = len(grid[0])
        self.resp = 0

        for row in range(self.nRows):
            for col in range(self.nCols):
                if (row, col) in self.seen or grid[row][col] == 1:
                    continue
                self.resp += self.dfs(row, col, grid)
        
        return(self.resp)
                
    def dfs(self, row, col, grid) -> int:
        stack = [(row, col)]
        foundEdge = False

        while stack:
            currRow, currCol = stack.pop()
            if currRow == 0 or currRow == self.nRows - 1 or currCol == 0 or currCol == self.nCols - 1:
                foundEdge = True

            self.seen.add((currRow, currCol))
            for dx, dy in self.dirs:
                newRow = currRow + dx
                newCol = currCol + dy
                if self.isValid(newRow, newCol) and (newRow, newCol) not in self.seen and grid[newRow][newCol] == 0:
                    stack.append((newRow, newCol))
            
        return(0 if foundEdge else 1)



    def isValid(self, row, col) -> bool:
        return(
            -1 < row < self.nRows and
            -1 < col < self.nCols and
            (row, col) not in self.seen
        )
```