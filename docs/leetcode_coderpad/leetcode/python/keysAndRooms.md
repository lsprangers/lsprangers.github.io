---
title: template
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# keysAndRooms

```python
class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        visited = set()
        keys = set()
        visited.add(0)

        def dfs(node, rooms):
            neighbors = rooms[node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor, rooms)
            return
        
        dfs(0, rooms)
        return(len(visited) == len(rooms))
```