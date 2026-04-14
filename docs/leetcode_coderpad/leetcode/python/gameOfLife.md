---
title: gameOfLife
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# gameOfLife

```python
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        dirs = [
            [1,0],
            [-1,0],
            [0,1],
            [0,-1],
            [1,1],
            [-1,1],
            [1,-1],
            [-1,-1],
        ]

        nRows = len(board)
        if nRows < 1:
            return

        nCols = len(board[0])

        for row in range(nRows):
            for col in range(nCols):
                currAliveNeighbors = 0
                for dx, dy in dirs:
                    neighborRow = row + dx
                    neighborCol = col + dy
                    if -1 < neighborRow < nRows and -1 < neighborCol < nCols:
                        if abs(board[neighborRow][neighborCol]) == 1:
                            currAliveNeighbors += 1

                
                # -1 means was alive and turned dead, allows abs(-1, 1) == 1 for alive neighbor check
                if board[row][col] == 1 and (currAliveNeighbors < 2 or currAliveNeighbors > 3):
                    board[row][col] = -1
                elif currAliveNeighbors == 3 and board[row][col] == 0:
                    board[row][col] = 2

        for row in range(nRows):
            for col in range(nCols):
                if board[row][col] > 0:
                    board[row][col] = 1
                else:
                    board[row][col] = 0        
        return
```