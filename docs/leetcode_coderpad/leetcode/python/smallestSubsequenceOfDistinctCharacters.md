---
title: smallestSubsequenceOfDistinctCharacters
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestSubsequenceOfDistinctCharacters

```python
class Solution:
    def smallestSubsequence(self, s: str) -> str:
        freq = collections.Counter(s)
        stack = []
        curr = set()
        for c in s:
            if c not in curr:
                while stack and stack[-1] > c:
                    # if this letter exists nowhere downstream, keep it
                    if freq[stack[-1]] <= 0:
                        break
                    
                    curr.remove(stack[-1])
                    stack.pop()

                if c not in curr:
                    stack.append(c)
                    curr.add(c)
            
            # move past this letter
            freq[c] -= 1            


        return("".join(stack))
```