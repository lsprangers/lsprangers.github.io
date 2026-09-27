---
title: evaluateTheBracketPairsOfAString
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# evaluateTheBracketPairsOfAString

```python
class Solution:
    def evaluate(self, s: str, knowledge: list[list[str]]) -> str:
        lookup = {}
        for pair in knowledge:
            k, v = pair
            lookup[k] = v
        
        currIdx = 0
        resp = []
        curr = []
        while currIdx < len(s):
            currChar = s[currIdx]
            if currChar == '(':
                tmpIdx = currIdx + 1
                key = []
                while tmpIdx < len(s) and s[tmpIdx] != ')':
                    key += s[tmpIdx]
                    tmpIdx += 1
                
                key = "".join(key)
                if key in lookup:
                    resp.append(lookup[key])
                else:
                    resp.append('?')
                
                currIdx = tmpIdx
            
            # elif currChar == ')':
            #     currIdx += 1
            
            else:
                resp.append(currChar)
            
            currIdx += 1
        
        return("".join(resp))

```