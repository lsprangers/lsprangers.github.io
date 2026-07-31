---
title: minimumNumberOfPushesToTypeWordI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumNumberOfPushesToTypeWordI

```python
class Solution:
    def minimumPushes(self, word: str) -> int:

        # since we can remap to anything, we want the 
        #   most frequent letters to have only one push
        charFreqs = collections.Counter(word)
        minHeap = []
        for char, freq in charFreqs.items():
            heapq.heappush(minHeap, (-freq, char))

        nCharsSeen = 0
        resp = 0

        while minHeap:
            freq, char = heapq.heappop(minHeap)
            freq *= -1

            # 8 total buttons we can use, the 4th ones on 7 and 9 we can just treat
            #   as being anywhere
            totalPush = (nCharsSeen // 8) + 1
            resp += (freq * totalPush)
            nCharsSeen += 1
        
        return(resp)
```