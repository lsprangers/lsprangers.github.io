---
title: cheapestFlightsWithinKStops
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# cheapestFlightsWithinKStops

## Bellman-Ford
```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # k acts as the n-1 limitation now
        
        distances = [float("inf")] * n
        distances[src] = 0
        
        for _iter in range(k + 1):
            
            tmp = distances[:]
            for edge_from, edge_to, cost in flights:
                if distances[edge_from] < float("inf"):
                    tmp[edge_to] = min(
                        tmp[edge_to],
                        distances[edge_from] + cost
                    )
            distances = tmp
        
        return(
            distances[dst] if distances[dst] != float("inf") else -1
        )
```