---
title: pairOfSongsWithTotalDurartionsDivisibleBy60
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# pairOfSongsWithTotalDurartionsDivisibleBy60

```python
class Solution:
    def numPairsDivisibleBy60(self, time: list[int]) -> int:
        bucketToNum = defaultdict(list)
        resp = 0
        for idx, num in enumerate(time):
            bucket = num % 60
            needed = (60 - bucket) % 60
            resp += len(bucketToNum[needed])            
            bucketToNum[bucket].append((num, idx))
        
        return(resp)
```