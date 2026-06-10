---
title: minimumDeleteSum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumDeleteSum
Can't believe I ripped this out after a few weeks

```python
class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        # probably has to be dynamic programming
        n = len(s1)
        m = len(s2)

        # sea
        # eat
        # at s, e we need min of sea + at or eat and ea since they aren't equal

        # cache makes it O(N * M) time and space
        @cache
        def dp(s1, s2) -> int:
            if not s1 and not s2:
                return(0)
            elif not s1:
                return(sum([ord(c) for c in s2]))
            elif not s2:
                return(sum([ord(c) for c in s1]))

            # there's something in both strings

            # if they equal here, continue on
            if s1[0] == s2[0]:
                return(
                    dp(s1[1:], s2[1:])
                )
            
            # else divide and return min
            return(
                min(
                    ord(s1[0]) + dp(s1[1:], s2),
                    ord(s2[0]) + dp(s1, s2[1:])
                )
            )
        
        return(dp(s1, s2))
```