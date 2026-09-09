---
title: countCommasInRangeII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countCommasInRangeII
Fucking `math.log` and floats?

```python
class Solution:
    def integer_log(self, n, base):
        if n <= 0 or base <= 1:
            raise ValueError("Invalid inputs")
        count = 0
        while n >= base:
            n //= base
            count += 1
        return count

    def countCommas(self, n: int) -> int:
        resp = 0

        while n > 0:
            currCommaCount = self.integer_log(n, 1000)
            currFloor = 1000 ** currCommaCount

            resp += (n - currFloor + 1) * currCommaCount

            n = currFloor - 1

        return resp
```