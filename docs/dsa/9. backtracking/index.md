---
title: 9. Backtracking
category: Data Structures & Algorithms
difficulty: Advanced
description: Examples, definitions, and general knowledge around Backtracking
show_back_link: true
---

## Backtracking
Nearly impossible to do Big O notation!

Backtracking deals with traversing a hierarchical tree from left to right, while moving back and forth between the left and right levels

A common examlpe is a [Trie](/docs/dsa/implementations/trie.md) where we have some suffix `abc` and we want traverse all other combinations moving back and forth such as going to `abcd` and realizing we don't want that, we want `abce` 

Pseudocode:
```python
def problem(self, arr) -> List[str]:
    if check_edge_case_initially():
        return([])
    
    resp = []
    seen = set() #sometimes this is not needed, it depends on problem

    def backtrack(idx, path):
        if condition(path) and path not in seen:
            resp.append(path)
            seen.add(path)
            return
        
        for i in arr[idx]:
            path.append(i)
            backtrack(idx + 1, path)
            path.pop()
    
    backtrack(0, []) # set things in motion
    return(resp)
```

So as you can see above we will recursively go through until some `condition(path)` is met, and then that would return on callstack and we'd immediately get to `path.pop()` which would allow us to test the next test case

A good example is permutations of a list `[1, 3, 5, 7]` of length 3
We'd have callstack of:
```
backtrack(0, []) -> backtrack(1, [1]) -> backtrack(2, [1, 3]) -> backtrack(3, [1, 3, 5])

at this point we'd reach the condition(path), add `135` to resp, and pop off

Then we'd get to backtrack(3, [1, 3, 7]) becuase we are in a loop of for i in arr[idx]

Lastly that'd pop off, it would return, and we'd get into backtrack(2, [1, 5]) -> backtrack(3, [1, 5, 7])
```

### Permutations vs Combinations
### Trie