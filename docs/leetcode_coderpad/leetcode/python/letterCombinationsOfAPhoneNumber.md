---
title: letterCombinationsOfAPhoneNumber
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# letterCombinationsOfAPhoneNumber

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if digits is None:
            return([])
        
        n = len(digits)
        phone_board = {
            1: [],                2: ['a', 'b','c'],    3: ['d','e','f'],
            4: ['g','h','i'],     5: ['j','k','l'],     6: ['m','n','o'],
            7: ['p','q','r','s'], 8: ['t','u','v'],     9: ['w','x','y','z']
        }        
        resp = []
        seen = set() #sometimes this is not needed, it depends on problem

        def backtrack(idx, path):
            if len(path) == n and tuple(path) not in seen:
                resp.append("".join(path[:]))
                seen.add(tuple(path))
                return
            
            for i in phone_board[int(digits[idx])]:
                path.append(i)
                backtrack(idx + 1, path)
                path.pop()
        
        backtrack(0, []) # set things in motion
        return(resp)
```