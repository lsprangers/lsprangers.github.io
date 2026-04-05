---
title: partitionLabels
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# partitionLabels

```python
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        indexes = defaultdict(list)
        
        # get first and last index of each character 
        # O(n) time space
        for idx, _char in enumerate(s):
            if _char not in indexes or len(indexes[_char]) == 1:
                indexes[_char] = [idx, idx]
            else:
                indexes[_char][1] = idx
            
        curr_seen = set()
        left = 0
        resp = []
        
        for right in range(len(s)):
            curr_char = s[right]
            curr_seen.add(curr_char)
            if indexes[curr_char][1] == right:
                curr_seen.remove(curr_char)
            
            # right = 8, left = 0
            # curr_seen = set()
            
            if len(curr_seen) == 0:
                resp.append(right - left + 1)
                left = right + 1
                # curr_seen = set()
        
        return(resp)
```