---
title: nearestExitFromEntranceInMaze
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# nearestExitFromEntranceInMaze

```python
class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        n_rows = len(maze)
        n_cols = len(maze[0])
        moves = [
            [0, 1],
            [1, 0],
            [0, -1],
            [-1, 0]
        ]

        q = deque([])
        q.append([entrance, 0])
        maze[entrance[0]][entrance[1]] = "+"

        while q:
            curr_node = q.popleft()
            curr_row = curr_node[0][0]
            curr_col = curr_node[0][1]
            curr_dist = curr_node[1]
            # check if exit
            for move in moves:
                next_row = curr_row + move[0]
                next_col = curr_col + move[1]
                
                # if valid next neighbor
                if 0 <= next_row < n_rows and 0 <= next_col < n_cols and maze[next_row][next_col] == ".":
                    
                    # if is exit
                    if next_row == 0 or next_col == 0 or next_row == n_rows - 1 or next_col == n_cols - 1:
                        return(curr_dist + 1) #greedy

                    maze[next_row][next_col] = "+"
                    q.append([[next_row, next_col], curr_dist + 1])
        
        return(-1)
```