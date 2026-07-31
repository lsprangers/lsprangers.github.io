---
title: cutOffTreesForGolfEvent
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# cutOffTreesForGolfEvent

```python
class Solution:
    def cutOffTree(self, forest: List[List[int]]) -> int:
        #[
        #   [2,3,4],
        #   [0,0,5],
        #   [8,7,6]]
        #heights are distinct
        minHeap = []
        nRows = len(forest)
        nCols = len(forest[0])
        heapq.heappush(minHeap, (forest[0][0], 0 ,0))
        
        for row in range(nRows):
            for col in range(nCols):
                if forest[row][col] > 1:
                    heapq.heappush(minHeap, (forest[row][col], row, col))
        
        resp = 0
        currRow, currCol = 0, 0

        while minHeap:
            _, tr, tc = heapq.heappop(minHeap)
            dist = self.bfs(currRow, currCol, tr, tc, nRows, nCols, forest)
            if dist == -1:
                return -1
            resp += dist
            forest[tr][tc] = 1
            currRow, currCol = tr, tc
        
        return(resp)

        
    def bfs(self, fromRow, fromCol, toRow, toCol, nRows, nCols, forest):
        dirs = [
            [1, 0],
            [0, 1],
            [-1, 0],
            [0, -1]
        ]
        # bfs would give us the shortest path
        dq = collections.deque([(fromRow, fromCol, 0)])

        seen = set()
        while dq:
            currRow, currCol, currStep = dq.popleft()
            if currRow == toRow and currCol == toCol:
                return(currStep)
                
            if (currRow, currCol) in seen:
                continue
            
            seen.add((currRow, currCol))

            for dx, dy in dirs:
                nextRow = currRow + dx
                nextCol = currCol + dy
                if (nextRow, nextCol) not in seen and -1 < nextRow < nRows and -1 < nextCol < nCols and forest[nextRow][nextCol] != 0:
                    dq.append((nextRow, nextCol, currStep + 1))
            
        
        return(-1)
```