---
title: sumGame
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# sumGame

```python
lass Solution:
    def sumGame(self, num: str) -> bool:
        # even length
        # problem reduces to if there are ways to ensure ?'s add up to each other
        # ?3295???
        #   [14, 1] vs [5, 3]
        #   [9, 1] vs [0, 3] --> Alice gets to choose first, she has 4 options in total
        #   and pretty much every option of hers will be to choose 0 or 9 based on if left
        #   half is less than or greater than right

        leftStruct = [0, 0]
        rightStruct = [0, 0]
        n = len(num)
        for idx in range(n):
            if idx >= n // 2:
                # right
                if num[idx].isnumeric():
                    rightStruct[0] += int(num[idx])
                else:
                    rightStruct[1] += 1
            else:
                # left
                if num[idx].isnumeric():
                    leftStruct[0] += int(num[idx])
                else:
                    leftStruct[1] += 1
        
        return (leftStruct[1] + rightStruct[1] % 2 == 1) or (leftStruct[0] - rightStruct[0] != (rightStruct[1] - leftStruct[1]) * 9 // 2)

```