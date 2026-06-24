---
title: maxLengthConcatenatedStringWithUniqueCharacters
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxLengthConcatenatedStringWithUniqueCharacters

```python
class Solution:
    def maxLength(self, arr: List[str]) -> int:
        self.resp = 0
        self.n = len(arr)
        
        def backtrack(currSet, idx):
            if idx >= self.n:
                return
            
            for i in range(idx, self.n):
                theseCharsSet = set([c for c in arr[i]])
                
                # # if these characters aren't unique
                if len(theseCharsSet) < len(arr[i]):
                    continue
                
                sendSet = currSet
                if len(theseCharsSet.intersection(currSet)) == 0:
                    sendSet = sendSet.union(theseCharsSet)
                
                backtrack(sendSet, i + 1)
                self.resp = max(self.resp, len(sendSet))
                    
        
        backtrack(set(), 0)
        return(self.resp)
            
            
```