---
title: numberOfDaysBetweenTwoDays
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfDaysBetweenTwoDays

```python
class Solution:
    def daysBetweenDates(self, date1: str, date2: str) -> int:
        d1_dt = datetime.date.fromisoformat(date1)
        d2_dt = datetime.date.fromisoformat(date2)
        
        if d1_dt >= d2_dt:
            diff = d1_dt - d2_dt
        else:
            diff = d2_dt - d1_dt
        
        return(diff.days)
```