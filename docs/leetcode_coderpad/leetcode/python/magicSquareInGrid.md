---
title: magicSquareInGrid
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# magicSquareInGrid

```python
class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        self.nRows = len(grid)
        if self.nRows < 1:
            return(0)
        
        self.nCols = len(grid[0])
        if self.nRows < 3 or self.nCols < 3:
            return(0)

        # trying to gauge what we can cache
        self.cache = defaultdict(int)

        # in 4 rows we need to go up to 1 since we'll do 
        #   row + 3 for offset
        resp = 0
        for startRow in range(self.nRows - 3 + 1):
            for startCol in range(self.nCols - 3 + 1):

                # we could probably cache something here for reuse later
                if self.check(grid, startRow, startCol):
                    resp += 1
        return(resp)
    
    def check(self, grid, startRow, startCol):
        distinctVals = set()
        for row in range(startRow, startRow + 3):
            for col in range(startCol, startCol + 3):
                if grid[row][col] in distinctVals or 1 > grid[row][col] or grid[row][col] > 9:
                    return(False)
                else:
                    distinctVals.add(grid[row][col])
        

        val = sum([grid[startRow][col] for col in range(startCol, startCol + 3)])

        # check each row
        for otherRow in range(startRow, startRow + 3):
            if sum([grid[otherRow][col] for col in range(startCol, startCol + 3)]) != val:
                return(False)

        # check each col
        for otherCol in range(startCol, startCol + 3):
            if sum([grid[row][otherCol] for row in range(startRow, startRow + 3)]) != val:
                return(False)

        # check diagonals
        # top left to bottom right
        if sum([grid[startRow + diagonalOffset][startCol + diagonalOffset] for diagonalOffset in range(3)]) != val:
            return(False)
        
        # top right to bottom left
        if sum([grid[startRow + diagonalOffset][startCol + 2 - diagonalOffset] for diagonalOffset in range(3)]) != val:
            return(False)        

        return(True)
```