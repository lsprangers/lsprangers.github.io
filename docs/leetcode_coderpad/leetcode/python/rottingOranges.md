---
title: rottingOranges
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# rottingOranges

```python
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        q = deque()
        # get rotten oranges into q
        # get count of fresh
        n_fresh = 0
        n_rows, n_cols = len(grid), len(grid[0])
        if n_rows == 0:
            return(-1)
            
        for r in range(n_rows):
            for c in range(n_cols):
                if grid[r][c] == 2:
                    q.append((r, c))
                elif grid[r][c] == 1:
                    n_fresh += 1
        
        if n_fresh == 0:
            return(0)

        # while q, breadth out each pulse, update timestamp, update adjacent
        n_iters = 0
        while q and n_fresh > 0:
            n_iters += 1
            for _ in range(len(q)):
                rotten_row, rotten_col = q.popleft()
                for adj_move in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                    adj_row = rotten_row + adj_move[0]
                    adj_col = rotten_col + adj_move[1]
                    if  -1 < adj_row < n_rows and -1 < adj_col < n_cols and grid[adj_row][adj_col] == 1:
                        grid[adj_row][adj_col] = 2
                        q.append((adj_row, adj_col))
                        n_fresh -= 1
        
        return(
            n_iters if n_fresh == 0 else -1
        )
```