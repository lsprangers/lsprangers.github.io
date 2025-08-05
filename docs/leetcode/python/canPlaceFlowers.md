---
title: canPlaceFlowers
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# canPlaceFlowers

```python
class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        if len(flowerbed) < 1:
            return(False)
        elif len(flowerbed) < 2:
            if n > 1:
                return(False)
            elif n == 1:
                return(flowerbed[0] == 0)
            else:
                return(True)

        plantable = 0
        for curr in range(len(flowerbed)):
            if 0 < curr < len(flowerbed) - 1:
                if flowerbed[curr - 1] == 0 and flowerbed[curr + 1] == 0 and flowerbed[curr] == 0:
                    plantable += 1
                    flowerbed[curr] = 1
            elif curr == 0:
                if flowerbed[curr + 1] == 0 and flowerbed[curr] == 0:
                    plantable += 1
                    flowerbed[curr] = 1
            else:
                if flowerbed[curr - 1] == 0 and flowerbed[curr] == 0:
                    plantable += 1
                    flowerbed[curr] = 1

        return(plantable >= n)
```