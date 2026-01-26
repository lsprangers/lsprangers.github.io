---
title: search2dMatrix
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# search2dMatrix

Instead of doing it this way you can treat it as one big list by utilizing floor division and modulo

- Row can be found via `idx // n_cols`
    - Row `0` has elements `[0, n_cols - 1]`
    - Row `1` has elements `[n_cols, 2 * n_cols - 1]`
    - etc...
    - Therefore looking at index `6`, if we do `6 // 4` we get 1 which relates to row 1
- Col can be found via `idx % n_cols`
    - Because `idx // n_cols` brings back to start of array, the % operator naturally gives remainder, which would indicate the column

![3b4 matrix](/img/3b4_matrix.png)

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if target < matrix[0][0] or target > matrix[-1][-1]:
            return(False)
        rowIdx = self.searchRows(matrix, target)
        if rowIdx == -1:
            return(False)
        
        leftIdx = 0
        rightIdx = len(matrix[rowIdx]) - 1
        while leftIdx <= rightIdx:
            midIdx = leftIdx + (rightIdx - leftIdx) // 2
            if matrix[rowIdx][midIdx] == target:
                return(True)
            elif matrix[rowIdx][midIdx] > target:
                rightIdx = midIdx - 1
            else:
                leftIdx = midIdx + 1
        
        return(False)


    def searchRows(self, matrix, target):
        leftIdx = 0
        rightIdx = len(matrix) - 1
        while leftIdx <= rightIdx:
            midIdx = leftIdx + (rightIdx - leftIdx) // 2
            if matrix[midIdx][0] <= target and matrix[midIdx][-1] >= target:
                return(midIdx)
            elif matrix[midIdx][-1] < target:
                leftIdx = midIdx + 1
            elif  matrix[midIdx][0] > target:
                rightIdx = midIdx - 1
            else:
                print("missed a case")
        
        return(-1)

```