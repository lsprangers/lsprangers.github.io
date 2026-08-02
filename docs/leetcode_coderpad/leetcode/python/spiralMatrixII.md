---
title: spiralMatrixII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# spiralMatrixII

```python
class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        self.nextDir = {
            'RIGHT': 'DOWN',
            'DOWN': 'LEFT',
            'LEFT': 'UP',
            'UP': 'RIGHT'
        }
        
        self.dirToChange = {
            # x, y
            'RIGHT': [1, 0],
            'DOWN': [0, 1],
            'LEFT': [-1, 0],
            'UP': [0, -1]
        }
        
        # set it up as we need to change to start off
        currPoint = (-1, 0)
        currDir = 'RIGHT'
        grid = [[None] * n for _ in range(n)]
        
        for val in range(1, (n * n) + 1):
            nextPoint = self.getNext(currPoint, currDir)
            while not self.isValid(nextPoint, n, grid):
                currDir = self.nextDir[currDir]
                nextPoint = self.getNext(currPoint, currDir)
            
            grid[nextPoint[1]][nextPoint[0]] = val
            currPoint = nextPoint
        
        return(grid)
            
                
    
    def getNext(self, currPoint, currDir):
        dx, dy = self.dirToChange[currDir]
        nextPoint = (currPoint[0] + dx, currPoint[1] + dy)
        return(nextPoint)
    
    def isValid(self, point, n, grid):
        x, y = point
        return(
            -1 < x < n and
            -1 < y < n and
            grid[y][x] == None
        )
```