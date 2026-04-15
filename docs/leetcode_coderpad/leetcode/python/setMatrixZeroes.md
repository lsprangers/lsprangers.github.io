---
title: setMatrixZeroes
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# setMatrixZeroes

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # Can't utilize -1 as marker for future deletion. Need to store
        #   indexes of all 0's, and then loop over those cols and rows

        nRows = len(matrix)
        if nRows < 1:
            return
        nCols = len(matrix[0])

        zeroRows = set()
        zeroCols = set()
        for row in range(nRows):
            for col in range(nCols):
                if matrix[row][col] == 0:
                    zeroRows.add(row)
                    zeroCols.add(col)
        
        for zeroRow in zeroRows:
            for col in range(nCols):
                matrix[zeroRow][col] = 0

        for zeroCol in zeroCols:
            for row in range(nRows):
                matrix[row][zeroCol] = 0
        
        return
```