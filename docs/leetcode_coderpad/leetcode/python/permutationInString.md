---
title: permutationInString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# permutationInString
Should have done sliding window of fixed size instead of doing full re-do on each string - mine is N * M, fixed size of N + M

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        self.s1Freqs = defaultdict(int)
        for c in s1:
            self.s1Freqs[c] += 1
        
        self.s2Idxs = defaultdict(list)
        for idx, c in enumerate(s2):
            self.s2Idxs[c].append(idx)
        
        
        for startChar in self.s1Freqs.keys():
            if startChar not in self.s2Idxs:
                return(False)

        
        for startChar in self.s1Freqs.keys():
            for s2Idx in self.s2Idxs[startChar]:
                if self.check(startChar, s2Idx, s2):
                    return(True)
        
        return(False)
    
    def check(self, startChar, s2Idx, s2):
        s1Copy = self.s1Freqs.copy()
        
        while s2Idx < len(s2):
            s2Char = s2[s2Idx]
            if s2Char not in s1Copy:
                return(False)
            
            s1Copy[s2Char] -= 1
            if s1Copy[s2Char] == 0:
                del s1Copy[s2Char]
        
            if len(s1Copy) == 0:
                return(True)
            
            s2Idx += 1
        
        return(len(s1Copy) == 0)
```