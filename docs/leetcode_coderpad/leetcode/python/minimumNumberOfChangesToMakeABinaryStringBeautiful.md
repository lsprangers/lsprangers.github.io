---
title: minimumNumberOfChangesToMakeABinaryStringBeautiful
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minimumNumberOfChangesToMakeABinaryStringBeautiful

```python
class Solution:
    def minChanges(self, s: str) -> int:
        # 1011 --> 1
        # 1000 --> 1
        # 101010 --> 3
        # think greedy works, I don't see why it wouldn't
        # 100101
        # 110101 --> 1 change
        # 110001 --> 2 changes
        # 110011 --> 3 changes --> min amount
        currIdx = 0
        resp = 0
        n = len(s)
        while currIdx < n:
            currVal = s[currIdx]
            tmpIdx = currIdx
            # if we had to do this for n it would just be a loop over the n window
            while tmpIdx < n and s[tmpIdx] == s[tmpIdx + 1] and s[tmpIdx] == s[currIdx]:
                tmpIdx += 2
            
            if tmpIdx == currIdx:
                resp += 1
                currIdx += 2
            else:
                currIdx = tmpIdx
        
        return(resp)
```