---
title: dailyTemperatures
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# dailyTemperatures

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        resp = [0] * len(temperatures)
        stack = []
        for i in range(len(temperatures)):
            # [2, 3, 4, ]
            # [1, 1]
            while stack and temperatures[stack[-1]] < temperatures[i]:
                j = stack.pop()
                resp[j] = i - j
            stack.append(i)
        return(resp)
```