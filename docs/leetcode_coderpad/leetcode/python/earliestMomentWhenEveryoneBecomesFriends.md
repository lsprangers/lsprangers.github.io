---
title: earliestMomentWhenEveryoneBecomesFriends
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# earliestMomentWhenEveryoneBecomesFriends

```python
class unionFind:
    def __init__(self, n):
        self.n = n
        self.rank = [1] * n
        self.parent = [x for x in range(n)]
    
    def get_parent(self, node: int):
        if node == self.parent[node]:
            return(node)
        
        self.parent[node] = self.get_parent(self.parent[node])
        return(self.parent[node])
    
    def union_components(self, x: int, y: int):
        rootX = self.get_parent(x)
        rootY = self.get_parent(y)
        if rootX == rootY:
            return(False)
        else:
            # rootX is "deeper", so pin Y under X
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootY] > self.rank[rootX]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            
            return(True)

    
    def is_connected(self, x: int, y: int):
        return(self.find(x) == self.find(y))
            

class Solution:
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        logs.sort(key = lambda x: x[0])
        union_find = unionFind(n)
        components = n
        
        for timestamp, x, y in logs:
            if union_find.union_components(x, y):
                components -= 1
            
            if components == 1:
                return(timestamp)
            
        
        return(-1)
        
```