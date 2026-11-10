---
title: countServersThatCommunicate
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countServersThatCommunicate

```python
class Solution:
    def countServers(self, grid: list[list[int]]) -> int:
        # for each computer need to count if other computers are in it's row 
        #   or column
        rowSum = [sum(grid[row]) for row in range(len(grid))]
        colSum = [sum(col) for col in zip(*grid)]
        resp = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 1 and (rowSum[row] > 1 or colSum[col] > 1):
                    resp += 1
        
        return(resp)
```