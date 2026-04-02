---
title: numberOfConnectedComponentsInUndirectedGraph
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfConnectedComponentsInUndirectedGraph

## Loop DFS
```python
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        seen = set()
        adj_list = [[] for i in range(n)]
        for e1, e2 in edges:
            adj_list[e1].append(e2)
            adj_list[e2].append(e1)
        
        resp = 0
        for node in range(n):
            if node in seen:
                continue
            
            seen.add(node)
            resp += 1
            stack = [node]
            while stack:
                curr = stack.pop()
                for neighbor in adj_list[curr]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            
        return(resp)
```