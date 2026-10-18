---
title: customSortString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# customSortString

```python
class Solution:
    def customSortString(self, order: str, s: str) -> str:
        ordering = deque([])
        for o in order:
            ordering.append(o)
        
        s_lookup = collections.Counter(s)
        
        resp = []
        while ordering:
            curr = ordering.popleft()
            if curr in s_lookup:
                freq = s_lookup[curr]
                del s_lookup[curr]
                resp += [curr] * freq
        
        for _char, freq in s_lookup.items():
            
            resp += [_char] * freq
        
        return("".join(resp))
```