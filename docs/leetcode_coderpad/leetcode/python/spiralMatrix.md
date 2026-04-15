---
title: spiralMatrix
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# spiralMatrix

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        self.dirsToNext = {
            'RIGHT': 'DOWN',
            'DOWN': 'LEFT',
            'LEFT': 'UP',
            'UP': 'RIGHT'
        }
        self.dirsChange = {
            'RIGHT': [0, 1],
            'DOWN': [1, 0],
            'LEFT': [0, -1],
            'UP': [-1, 0]
        }
        self.nRows = len(matrix)
        if self.nRows < 1:
            return([])
        self.nCols = len(matrix[0])
        if self.nCols < 1 or self.nRows < 1:
            return(matrix[0])

        self.seen = set()
        currDir = 'RIGHT'
        curr = (0, 0)
        resp = []
        
        while self.isValid(curr[0], curr[1]):
            self.seen.add(curr)
            currRow, currCol = curr[0], curr[1]

            resp.append(
                matrix[currRow][currCol]
            )

            dx, dy = self.dirsChange[currDir]
            nextRow = currRow + dx
            nextCol = currCol + dy

            while not self.isValid(nextRow, nextCol) and len(self.seen) < self.nRows * self.nCols:
                currDir = self.dirsToNext[currDir]
                dx, dy = self.dirsChange[currDir]
                nextRow = currRow + dx
                nextCol = currCol + dy

            curr = (nextRow, nextCol)

        return(resp)
    
    def isValid(self, row, col):
        return(
            -1 < row < self.nRows and
            -1 < col < self.nCols and
            (row, col) not in self.seen
        )
```