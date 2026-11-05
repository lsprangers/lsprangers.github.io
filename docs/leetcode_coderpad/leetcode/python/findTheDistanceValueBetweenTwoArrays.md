---
title: findTheDistanceValueBetweenTwoArrays
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findTheDistanceValueBetweenTwoArrays

```python
class Solution:
    def findTheDistanceValue(self, arr1: list[int], arr2: list[int], d: int) -> int:
        resp = 0
        for i in range(len(arr1)):
            hasOne = False
            for j in range(len(arr2)):
                if abs(arr1[i] - arr2[j]) <= d:
                    hasOne = True
            
            resp += 0 if hasOne else 1

        return(resp)
```