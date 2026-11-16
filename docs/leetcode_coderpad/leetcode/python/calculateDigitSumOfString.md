---
title: calculateDigitSumOfString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# calculateDigitSumOfString

```python
from itertools import batched

class Solution:
    def digitSum(self, s: str, k: int) -> str:
        curr = [int(c) for c in s]
        while len(curr) > k:
            splits = list(batched(curr, k))
            curr = [sum(c) for c in splits]
            curr = [int(d) for num in curr for d in str(num)]
        
        return("".join([str(c) for c in curr]))
```