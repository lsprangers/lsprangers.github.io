---
title: shortestPathWithKMostConsecutiveCharacters
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# shortestPathWithKMostConsecutiveCharacters

```python
class Solution:
    def shortestPath(self, n: int, edges: List[List[int]], labels: str, k: int) -> int:
        neighbors = defaultdict(list)

        for u, v, w in edges:
            neighbors[u].append((v, w))
            # neighbors[v].append((u, w))

        heap = [
            # currWeight, node, currFreq
            (0, 0, 1)
        ]
        distances = defaultdict(lambda: float("inf"))
        distances[(0, 1)] = 0
        resp = float("inf")

        while heap:
            currWeight, currNodeIdx, currFreq = heapq.heappop(heap)
            if currWeight > distances[(currNodeIdx, currFreq)]:
                continue

            if currNodeIdx == n - 1:
                resp = min(resp, currWeight)
            
            for neighborIdx, neighborWeight in neighbors[currNodeIdx]:
                neighbor = labels[neighborIdx]
                
                if neighbor == labels[currNodeIdx] and currFreq + 1 > k:
                    continue
                 
                newFreq = (currFreq + 1) if neighbor == labels[currNodeIdx] else 1
                newWeight = currWeight + neighborWeight
                if newWeight < distances[(neighborIdx, newFreq)]:
                    distances[(neighborIdx, newFreq)] = newWeight
                    heapq.heappush(
                        heap, 
                        (newWeight, neighborIdx, newFreq)
                    )

        return(resp if resp != float("inf") else -1)
```