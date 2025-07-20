---
title: countingBits
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countingBits

I don't know bit manipulation well enough to do dynmaic programming

```python
class Solution:
    def countBits(self, n: int) -> List[int]:
        # fill array to n (size n+1)
        ans = []

        # O(n)
        for idx in range(n + 1):
            ans.append(self.count_set_bits(idx))

        # O(n logn)
        return(ans)

    # O(log n) - number of bits in x max log(x) + 1
    def count_set_bits(self, n):
        count = 0
        while n > 0:
            n &= (n - 1)  # Clears the least significant set bit
            count += 1
        return count```