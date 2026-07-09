---
title: pathExistenceQueriesInGraphI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# pathExistenceQueriesInGraphI

```python
class UnionFind:
    def __init__(self, n):
        self.rank = [0] * n
        self.root = [i for i in range(n)]
    
    def find(self, x):
        if self.root[x] == x:
            return(self.root[x])
        
        self.root[x] = self.find(self.root[x])
        return(self.root[x])
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return(False)
        
        if self.rank[rootX] < self.rank[rootY]:
            self.root[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.root[rootY] = rootX
        else:
            self.root[rootY] = rootX
            self.rank[rootY] += 1
        
        return(True)
    
    def connected(self, x, y):
        return(
            self.find(x) == self.find(y)
        )


class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[bool]:
        nodes = [(node, num) for node, num in zip(range(n), nums)]
        # nodes.sort(key=lambda x: x[1]) # already sorted

        uf = UnionFind(n)
        for right in range(1, len(nodes)):
            if nodes[right][1] - nodes[right - 1][1] <= maxDiff:
                uf.union(right - 1, right)
            
        
        resp = []
        for query in queries:
            resp.append(uf.connected(query[0], query[1]))
        
        return(resp)
```