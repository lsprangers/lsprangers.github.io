---
title: dota2Senate
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# dota2Senate

```python
class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        # 'RDDRD'
        dq = deque([])
        freqs = {
            'R': 0,
            'D': 0
        }
        other = {
            'R': 'D',
            'D': 'R'
        }

        # [R,D,D,R,D]
        for c in senate:
            freqs[c] += 1
            dq.append(c)
        
        # next up would be popleft()
        while dq:
            next_senator = dq.popleft()
            if freqs[other[next_senator]] > 0:
                # O(n^2) here - Editorial specifies to keep list of indexes of each
                #   and then you can use binary search
                # Anything with O(N) "list.index()" find is suspect 
                #   and maybe useful for Binary Search
                next_other = dq.index(other[next_senator])
                del dq[next_other]
                freqs[other[next_senator]] -= 1
            else:
                return("Radiant" if next_senator == 'R' else "Dire")

            dq.append(next_senator)

        return("Radiant" if next_senator == 'R' else "Dire")
```