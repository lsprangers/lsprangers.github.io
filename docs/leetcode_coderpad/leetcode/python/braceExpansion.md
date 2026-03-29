---
title: braceExpansion
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# braceExpansion

```python
class Solution:
    def expand(self, s: str) -> List[str]:
        # [z, q, {, a, b, }, c, {d, e, }, f]
        chars = deque([c for c in s if c != ','])
        # [ [] ]
        resp = deque([[]])
        while chars:
            curr = chars.popleft()
            if curr.isalpha():
                for existing in resp:
                    # [ [z, a, c], [q, a, c], [z, b, c], [q, b, c]]
                    existing.append(curr)
            else:
                bracket_chars = []
                while chars[0].isalpha():
                    bracket_chars.append(chars.popleft())
                # char[0] is }
                chars.popleft()
                curr_resp_size = len(resp)
                for _ in range(curr_resp_size):
                    curr_existing = resp.popleft()
                    for bracket_char in bracket_chars:
                        new_existing = curr_existing[:]
                        new_existing.append(bracket_char)
                        resp.append(new_existing)                
        
        return(sorted(["".join(r) for r in resp]))
```