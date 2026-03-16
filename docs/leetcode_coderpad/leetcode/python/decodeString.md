---
title: decodeString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# decodeString

```python
class Solution:
    def decodeString(self, s: str) -> str:
        # 3[a2[bc]]
        stack = []
        left = 0
        while left < len(s):
            if s[left] != ']':
                # [3, [, a, b, c, b, c]
                stack.append(s[left])
            else:
                tmp_str = []
                while stack and stack[-1] != '[':
                    tmp_str.append(stack[-1])
                    stack.pop()
                # at this point stack should have digit,[ as next 2 entries
                stack.pop()
                tmp_multiplier = []
                while stack and stack[-1].isdigit():
                    tmp_multiplier.append(stack[-1])
                    stack.pop()
                
                tmp_multiplier.reverse()
                tmp_str.reverse()
                # 2, [c, b]
                for n in int("".join(tmp_multiplier)) * tmp_str:
                    # [b, c, b, c]
                    # [3, [, a, b, c, b, c]
                    stack.append(n)
            left += 1

        return("".join(stack))

```