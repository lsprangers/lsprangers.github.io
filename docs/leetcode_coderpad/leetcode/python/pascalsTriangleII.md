---
title: pascalsTriangleII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# pascalsTriangleII

```python
class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        dp = [[1]]
        while len(dp) < rowIndex + 1:
            lastRow = dp[-1]
            nextRow = [1]
            for currIdx in range(1, len(lastRow)):
                nextRow.append(lastRow[currIdx - 1] + lastRow[currIdx])
            
            nextRow.append(1)
            dp.append(nextRow)
        
        return(dp[-1])
```