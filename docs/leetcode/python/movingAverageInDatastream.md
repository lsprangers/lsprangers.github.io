---
title: movingAverageInDatastream
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# movingAverageInDatastream

```python
class MovingAverage:

    def __init__(self, size: int):
        self.size = size
        self.sum = 0
        self.dq = deque([])

    def next(self, val: int) -> float:
        self.dq.append(val)
        self.sum += val
        while len(self.dq) > self.size:
            self.sum -= self.dq.popleft()
        
        return(
            self.sum / len(self.dq)
        )
```