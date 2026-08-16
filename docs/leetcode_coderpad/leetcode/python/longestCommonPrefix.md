---
title: longestCommonPrefix
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestCommonPrefix

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        idx = 0
        minLenWord = min([len(word) for word in strs])

        while idx < minLenWord:
            curr = strs[0][idx]
            for word in strs:
                if word[idx] != curr:
                    return(word[ : idx])
            idx += 1
        
        return(strs[0][ : idx])
```