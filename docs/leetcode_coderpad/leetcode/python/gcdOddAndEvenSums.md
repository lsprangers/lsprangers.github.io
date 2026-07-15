---
title: gcdOddAndEvenSums
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# gcdOddAndEvenSums

```python
class Solution:
    def gcdOfOddEvenSums(self, n: int) -> int:
        # A + B = C + D + B ==> GCD(A, B) = GCD(C + D, B)
        odd = 0
        even = 0
        for num in range(1, (n * 2) + 1):
            if num % 2 == 0:
                even += num
            else:
                odd += num
        
        return(math.gcd(even, odd))
```