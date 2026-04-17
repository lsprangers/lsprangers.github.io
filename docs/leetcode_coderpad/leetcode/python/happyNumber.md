---
title: happyNumber
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# happyNumber

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set([1])
        while n not in seen:
            seen.add(n)
            n = sum([int(c) ** 2 for c in str(n)])
        
        return(n == 1)
```