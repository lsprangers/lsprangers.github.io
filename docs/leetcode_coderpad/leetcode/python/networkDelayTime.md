---
title: networkDelayTime
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# networkDelayTime

```python
class Solution:

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        dir_graph = defaultdict(list)
        for from_x, to_y, weight in times:
            dir_graph[from_x].append((to_y, weight))
        
        # shortest path from source node k to all other nodes
        distances = {vertex: float('inf') for vertex in range(1, n+1)}
        distances[k] = 0
        # store the node we used to get to this vertex (to reconstruct path later)
        previous_nodes = {vertex: None for vertex in range(1, n+1)}
        min_heap = [(0, k)]  # (distance, vertex)
        
        while min_heap:
            current_distance, current_node = heapq.heappop(min_heap)
            
            # less than or equal; we can continue
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, neighbor_weight in dir_graph[current_node]:
                neighbor_distance = current_distance + neighbor_weight
                if neighbor_distance < distances[neighbor]:
                    distances[neighbor] = neighbor_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(min_heap, (neighbor_distance, neighbor))
        
        if any([x for x in distances.values() if x == float("inf")]):
            return(-1)
        else:
            return(max(distances.values()))
```