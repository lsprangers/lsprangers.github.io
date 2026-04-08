---
title: leftmostColumnWithAtLeastAOne
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# leftmostColumnWithAtLeastAOne

```python
# """
# This is BinaryMatrix's API interface.
# You should not implement it, or speculate about its implementation
# """
#class BinaryMatrix(object):
#    def get(self, row: int, col: int) -> int:
#    def dimensions(self) -> list[]:

class Solution:
    def leftMostColumnWithOne(self, binaryMatrix: 'BinaryMatrix') -> int:
        self.n_rows, self.n_cols = binaryMatrix.dimensions()
        
        # open interval, first valid X
        left = 0
        right = self.n_cols
        
        while left < right:
            mid = left + (right - left) // 2
            # if this returns, there's a 1 in the column
            if self.check(binaryMatrix, mid):
                right = mid
            
            # there are absolutely no 0's in this column
            else:
                left = mid + 1
        
        # check if there's a 1 in left
        if left < self.n_cols:
            return(left)
        
        return(-1)
    
    # 1, 1, 1, 1, 1
    # 0, 0, 0, 1, 1
    # 0, 0, 1, 1, 1
    # 0, 0, 0, 0, 1
    # 0, 0, 0, 0, 0
    def check(self, binaryMatrix: 'BinaryMatrix', mid: int) -> bool:
        # we know rows are sorted, but not cols
        for row in range(self.n_rows):
            if binaryMatrix.get(row, mid) == 1:
                return(True)
        
        return(False)
        
```