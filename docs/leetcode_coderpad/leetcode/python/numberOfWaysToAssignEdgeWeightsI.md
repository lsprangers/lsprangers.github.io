---
title: numberOfWaysToAssignEdgeWeightsI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfWaysToAssignEdgeWeightsI

```python
class Solution:
    def assignEdgeWeights(self, edges: List[List[int]]) -> int:
        if len(edges) < 1:
            return(0)
        
        maxDepth = self.getMaxDepth(edges)

        # need odd number of odd edges
        # d choose 1 + d choose 3 + ...
        # that sum above somehow turns into 2^(d-1),
        
        # there are 2^k total edge choices since each edge is either
        # E or O, for the first k-1 there's 2^(k-1), and depending on those
        # we must choose E if 2^(k-1) are O, or O if 2^(k-1) are E
        #
        return(
            (2**(maxDepth - 1)) % ((10**9) + 7)
        )
    
    def getMaxDepth(self, edges):
        graph = defaultdict(list)
        seen = set()
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        stack = [(1,0)]
        resp = 0
        while stack:
            currNode, currDepth = stack.pop()
            if currNode in seen:
                continue
            seen.add(currNode)
        
            resp = max(resp, currDepth)

            for child in graph[currNode]:
                stack.append((child, currDepth + 1))

        return(resp)
```