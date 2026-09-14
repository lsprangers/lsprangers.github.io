---
title: search2dMatrixII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# search2dMatrixII

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            idx = bisect.bisect_left(row, target)
            if idx < 0 or idx > len(row) - 1:
                continue
            if row[idx] == target:
                return(True)
        
        return(False)
```