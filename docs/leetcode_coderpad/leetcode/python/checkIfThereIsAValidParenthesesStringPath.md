---
title: checkIfThereIsAValidParenthesesStringPath
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# checkIfThereIsAValidParenthesesStringPath

```python
class Solution:
    def hasValidPath(self, grid: list[list[str]]) -> bool:
        moves = [
            [1, 0], # "up" a row, i.e. move down 2d grid
            [0, 1] # "up" a col, i.e. move right 2d grid
        ]
        

        # row, col, bal
        stack = [(0, 0, 0)]
        seen = set()

        nRows = len(grid)
        if nRows < 1:
            return(True)

        nCols = len(grid[0])

        while stack:
            currRow, currCol, currBal = stack.pop()
            currBal += 1 if grid[currRow][currCol] == '(' else -1

            if currBal < 0:
                continue

            state = (currRow, currCol, currBal)

            if state in seen:
                continue

            seen.add(state)

            if currRow == nRows - 1 and currCol == nCols - 1:
                if currBal == 0:
                    return True
                continue

            for dx, dy in moves:
                nextRow = currRow + dx
                nextCol = currCol + dy

                if 0 <= nextRow < nRows and 0 <= nextCol < nCols:
                    stack.append((nextRow, nextCol, currBal))

        return False
```