---
title: combinationSum3
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# combinationSum3

```python
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        # combinations gives 9 choose 3 total amount
        #   O(n * C(n, 3))
        # otherwise, we can have N^2 double loop with sum and 
        #   check for last number
        #   O(n ^ 2)
        resp = []
        for combo in itertools.combinations(range(1, 10), k):
            if sum(combo) == n:
                resp.append(combo)
        
        return(resp)
```

Or without `itertools` we can do typical backtracking

```python
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        # combinations gives 9 choose 3 total amount
        #   O(n * C(n, 3))
        # otherwise, we can have N^2 double loop with sum and 
        #   check for last number
        #   O(n ^ 2)
        resp = []
        
        def backtrack(curr: List[int], start: int):
            if len(curr) == k and sum(curr) == n:
                resp.append(curr[:])
                return
            
            for other_num in range(start, 10):
                curr.append(other_num)
                backtrack(curr, other_num + 1) # force move forward
                curr.pop()
            
            return
        
        backtrack([], 1)
        return(resp)
```