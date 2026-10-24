---
title: countDaysTogether
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countDaysTogether

```python
class Solution:
    def countDaysTogether(self, arriveAlice: str, leaveAlice: str, arriveBob: str, leaveBob: str) -> int:
        daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        arriveAlice = datetime.datetime.strptime(arriveAlice, "%m-%d")
        leaveAlice = datetime.datetime.strptime(leaveAlice, "%m-%d")
        arriveBob = datetime.datetime.strptime(arriveBob, "%m-%d")
        leaveBob = datetime.datetime.strptime(leaveBob, "%m-%d")
        
        overlap = int(
            (min(leaveAlice, leaveBob) - max(arriveAlice, arriveBob)).days
        )
        return(max(overlap + 1, 0))
```