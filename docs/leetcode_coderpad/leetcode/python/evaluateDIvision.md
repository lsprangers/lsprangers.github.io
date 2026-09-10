---
title: evaluateDIvision
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# evaluateDIvision

```python
class UnionFind:
    def __init__(self, nodes):
        self.root = {node : node for node in nodes}
        self.rank = {node : 0 for node in nodes}
    
    def find(self, x) -> str:
        if x not in self.root:
            self.root[x] = x
        
        if x != self.root[x]:
            self.root[x] = self.find(self.root[x])
        
        return(self.root[x])
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX == rootY:
            return(False)
        
        if self.rank[rootX] > self.rank[rootY]:
            self.root[rootY] = rootX
        elif self.rank[rootY] > self.rank[rootX]:
            self.root[rootX] = rootY
        else:
            self.rank[rootX] += 1
            self.root[rootY] = rootX
        
        return(True)
    
    def connected(self, x, y):
        return(
            self.find(x) == self.find(y)
        )

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        self.nodes = set()

        for idx, eq in enumerate(equations):
            self.nodes.add(eq[0])
            self.nodes.add(eq[1])
        
        self.graph = defaultdict(list)
        self.uf = UnionFind(self.nodes)

        for idx, eq in enumerate(equations):
            self.graph[eq[0]].append(
                (eq[1], float(values[idx]))
            )

            self.graph[eq[1]].append(
                (eq[0], float(1 / values[idx]))
            )

            self.uf.union(eq[0], eq[1])
        
        resp = []
        for query in queries:
            resp.append(
                self.dfs(query[0], query[1])
            )
        
        return(resp)


    def dfs(self, num, den):
        if not self.uf.connected(num, den) or num not in self.nodes or den not in self.nodes:
            return(float(-1))

        elif num == den:
            return(float(1))
        

        # a/b = 2
        # a/c = 3
        # a/d = 4
        # c/d = 5...
        # a/d == a/c * c/d == 3 * 5
        stack = [(num, float(1))]
        seen = set()

        while stack:
            currNode, currVal = stack.pop()

            if currNode in seen:
                continue
            
            seen.add(currNode)
            for neighbor, neighborVal in self.graph[currNode]:
                if neighbor in seen:
                    continue

                # seen.add(neighbor)
                neighborUpdate = currVal * neighborVal

                if neighbor == den:
                    return(neighborUpdate)

                stack.append((neighbor, neighborUpdate))

        return(float(-1))
```