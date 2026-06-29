---
title: numberOfStringsThatAppearAsSubstrings
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfStringsThatAppearAsSubstrings

```python
class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        resp = 0
        self.charToIdx = defaultdict(list)
        for idx, _char in enumerate(word):
            self.charToIdx[_char].append(idx)
        
        for pattern in patterns:
            resp += self.check(pattern, word)
        
        return(resp)
    
    def check(self, pattern, word):
        for startIdx in self.charToIdx[pattern[0]]:
            endIdx = startIdx + len(pattern)
            if endIdx <= len(word) and word[startIdx : endIdx] == pattern:
                return(1)
        
        return(0)
```