---
title: removeMethodsFromProject
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# removeMethodsFromProject

```python
class Solution:
    def remainingMethods(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        graph = {}
        for node in range(n):
            graph[node] = set()
        
        for _from, _to in invocations:
            graph[_from].add(_to)
        
        stack = [k]
        suspicious = set()
        while stack:
            currMethod = stack.pop()
            if currMethod in suspicious:
                continue
            
            suspicious.add(currMethod)
            for nextMethod in graph[currMethod]:
                if nextMethod not in suspicious:
                    stack.append(nextMethod)

        resp = []
        canRemove = True
        for node in range(n):
            if node in suspicious:
                continue
            
            if len(graph[node].intersection(suspicious)) > 0:
                canRemove = False
            
            resp.append(node)
        
        if not canRemove:
            resp += list(suspicious)

        return(resp)
```