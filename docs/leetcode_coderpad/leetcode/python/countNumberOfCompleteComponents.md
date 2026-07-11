---
title: countNumberOfCompleteComponents
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countNumberOfCompleteComponents

```python
class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        # In a complete CC of n nodes, there's n(n-1) / 2 edges
        # A --- B
        # |  X  |
        # C --- D
        # Each node needs to talk to the other n-1 nodes
        #   therefore, for each n, there's n-1 edges
        #   and they're bi-directional, so we divide by 2
        # Also, in complete CC, each node has inDegree / outDegree = n-1
        graph = defaultdict(list)
        inorder = defaultdict(int)

        for x, y in edges:
            graph[x].append(y)
            inorder[x] += 1
            graph[y].append(x)
            inorder[y] += 1
        
        resp = 0
        seen = set()
        for node in range(n):
            if node in seen:
                continue
            
            smallestInorder = inorder[node]
            nNodesInCC = 0
            stack = [node]
            while stack:
                currNode = stack.pop()
                if currNode in seen:
                    continue
                
                nNodesInCC += 1
                seen.add(currNode)
                
                for neighbor in graph[currNode]:
                    stack.append(neighbor)
                    smallestInorder = min(smallestInorder, inorder[neighbor])
            
            if smallestInorder == nNodesInCC - 1:
                resp += 1
        
        return(resp)
```

```python
class UnionFind:
    def __init__(self, n):
        self.nNode = [1] * n
        self.root = [x for x in range(n)]
    
    def find(self, x):
        # path compression, ensure roots are true root
        #   up the hierarchy
        # 1 --> 2 --> 3 --> 4
        # 1=1 --> 1
        # 2's root is now 1, return 1
        # 3's root is 2, find(2) returns 1, 3's root is now 1
        # 4's root is 3, find(3) returns above, 4's root is now 1
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        
        return(self.root[x])
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return # so it doesn't reach else

        # rootX has lower overall hierarchy size, place it under Y
        if self.nNode[rootX] < self.nNode[rootY]:
            self.root[rootX] = rootY
            self.nNode[rootY] += self.nNode[rootX]
        else:
            self.root[rootY] = rootX
            self.nNode[rootX] += self.nNode[rootY]

    
    def connected(self, x, y):
        return(
            self.find(x) == self.find(y)
        )


class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        # In a complete CC of n nodes, there's n(n-1) / 2 edges
        # A --- B
        # |  X  |
        # C --- D
        # Each node needs to talk to the other n-1 nodes
        #   therefore, for each n, there's n-1 edges
        #   and they're bi-directional, so we divide by 2
        # Also, in complete CC, each node has inDegree / outDegree = n-1
        uf = UnionFind(n)
        componentEdgeCount = defaultdict(int)

        for x, y in edges:
            uf.union(x, y)
        
        # now we need to count edges in component
        for x, y in edges:
            root = uf.find(x)
            componentEdgeCount[root] += 1
        
        resp = 0
        for node in range(n):
            # if root - O(1)
            if uf.find(node) == node:
                nNode = uf.nNode[node]
                nEdge = componentEdgeCount[node]
                if nEdge == (nNode * (nNode - 1) // 2):
                    resp += 1
        return(resp)
```