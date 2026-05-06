---
title: shortestDistanceAfterRoadAdditionQueriesI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# shortestDistanceAfterRoadAdditionQueriesI

```python
class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        for idx in range(n):
            if idx == n - 1:
                graph[idx] = []
            else:
                graph[idx] = [(idx + 1, 1)]

        resp = []
        for query in queries:
            queryStart, queryEnd = query
            graph[queryStart].append((queryEnd, 1))
            currLengthToTarget = self.djikstra(graph, n - 1, n) # could remove target here, just n - 1 always
            resp.append(currLengthToTarget)
        
        return(resp)

    def djikstra(self, graph, target, n):

        # distance, node
        distances = {node: float("inf") for node in range(n)}
        distances[0] = 0

        minHeap = [(0, 0)]
        while minHeap:
            currDist, currNode = heapq.heappop(minHeap)

            if currDist > distances[currNode]:
                continue

            for neighbor, weight in graph[currNode]:
                neighborWeight = currDist + weight
                if neighborWeight < distances[neighbor]:
                    distances[neighbor] = neighborWeight
                    heapq.heappush(minHeap, (neighborWeight, neighbor))
        
        return(distances[target])

```