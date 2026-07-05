---
title: minScoreOfPathBetweenTwoCities
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minScoreOfPathBetweenTwoCities

```python
class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        # need to keep a min of connected component
        graph = defaultdict(list)
        for fromNode, toNode, distance in roads:
            graph[fromNode].append([toNode, distance])
            graph[toNode].append([fromNode, distance])
        
        minDistance = float("inf")
        
        # vertex, min seen
        stack = [1]
        seen = set()
        while stack:
            currNode = stack.pop()
            
            for neighborNode, neighborDistance in graph[currNode]:
                if neighborNode not in seen:
                    stack.append(neighborNode)
                seen.add(neighborNode)

                minDistance = min(minDistance, neighborDistance)
        
        return(minDistance)
```