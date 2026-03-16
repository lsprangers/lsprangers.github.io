---
title: equalRowAndColumnPair
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# equalRowAndColumnPair

```python
class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        resp = 0
        row_freq = collections.Counter(tuple(row) for row in grid)
        
        for colIdx in range(len(grid[0])):
            col = tuple([row[colIdx] for row in grid])
            resp += row_freq[col]

        return(resp)
```