---
title: maximumNumberOfBalloons
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumNumberOfBalloons

```python
class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        freqs = collections.Counter(text)
        resp = 0
        while freqs['b'] > 0 and \
            freqs['a'] > 0 and \
            freqs['l'] > 1 and \
            freqs['o'] > 1 and \
            freqs['n'] > 0:
            freqs['b'] -= 1
            freqs['a'] -= 1
            freqs['l'] -= 2
            freqs['o'] -= 2
            freqs['n'] -= 1
            resp += 1
        
        return(resp)
```