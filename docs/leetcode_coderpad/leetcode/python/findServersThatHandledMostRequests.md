---
title: findServersThatHandledMostRequests
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findServersThatHandledMostRequests

```python
class Solution:
    def busiestServers(self, k: int, arrival: list[int], load: list[int]) -> list[int]:
        self.k = k
        self.serverHandledCount = defaultdict(int)
        self.availableServers = sortedcontainers.SortedList(range(k))
        # minHeap based (finishedTime, serverIdx)
        self.busyServers = []

        # strictly increasing arrival time
        for arrivalIdx, arrivalTs in enumerate(arrival):
            self.currSecond = arrivalTs
            self.drainBusy()
            arrivalLoad = load[arrivalIdx]
            serverIdx = self.getServer(arrivalIdx)
            
            # dropped load
            if serverIdx is None:
                continue
            
            self.serverHandledCount[serverIdx] += 1
            finishTs = arrivalTs + arrivalLoad
            self.availableServers.remove(serverIdx)
            heapq.heappush(self.busyServers, [finishTs, serverIdx])
            

        resp = []
        maxHandled = max(self.serverHandledCount.values())
        for k, v in self.serverHandledCount.items():
            if v == maxHandled:
                resp.append(k)
        
        return(resp)

    def drainBusy(self):
        while self.busyServers and self.busyServers[0][0] <= self.currSecond:
            finishTs, finishedServerIdx = heapq.heappop(self.busyServers)
            self.availableServers.add(finishedServerIdx)        

    def getServer(self, arrivalIdx: int) -> int | None:
        if not self.availableServers:
            return None

        preferred = arrivalIdx % self.k
        pos = self.availableServers.bisect_left(preferred)
        if pos == len(self.availableServers):
            pos = 0

        return self.availableServers[pos]
```