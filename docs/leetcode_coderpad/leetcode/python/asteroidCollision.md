---
title: asteroidCollision
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# asteroidCollision
This one is funky - anything with a pair matching is usually done with stack though

```python
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        resp = []

        for asteroid in asteroids:
            if asteroid > 0:
                stack.append(asteroid)
            else:
                # negative goes through
                while stack and stack[-1] < abs(asteroid):
                    stack.pop()
                # left most is now negative
                if len(stack) < 1:
                    resp.append(asteroid)
                # if there's still a stack, check for mutual destruction
                elif stack[-1] == abs(asteroid):
                    stack.pop()
        
        resp += stack
        return(resp)
```