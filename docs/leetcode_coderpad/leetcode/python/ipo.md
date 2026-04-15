---
title: ipo
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# ipo

```python
class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        # want to be greedy with the amount of profit dependent on capital constraints
        #   so pick highest profit with capital < currentCapital
        currentCapital = w

        # O(n) heapify, break capital tie via profits
        capitalHeap = [(capAmt, idx) for idx, capAmt in enumerate(capital)]
        maxProfitHeap = []
        heapq.heapify(capitalHeap)

        for currProjectIdx in range(k):

            # technically only runs O(n) times
            while capitalHeap and capitalHeap[0][0] <= currentCapital:
                # popped at most once
                capAmt, idx = heapq.heappop(capitalHeap)
                # pushed at most once
                heapq.heappush(maxProfitHeap, (-profits[idx], idx))
                
            # not enough capital
            if not maxProfitHeap:
                break

            negMaxProfit, maxProfitIdx = heapq.heappop(maxProfitHeap)
            currentCapital += -negMaxProfit


        return(currentCapital)
```