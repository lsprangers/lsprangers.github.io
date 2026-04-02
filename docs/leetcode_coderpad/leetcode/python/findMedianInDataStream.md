---
title: findMedianInDataStream
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findMedianInDataStream

```python
class MedianFinder:

    def __init__(self):
        self.count = 0
        # [1, 2, 3]
        # max heap
        self.leftPQ = []
        
        # [4, 5, 6]
        # min heap
        self.rightPQ = []

    def addNum(self, num: int) -> None:
        self.count += 1
        # left = [1, 4, 6]
        # leftPQ = [-6, -4, -1]
        # right = [7, 10, 12]
        # rightPQ = [7, 10, 12]
        # median is 7 + 6 / 2
        # if we want to add 5
        if len(self.leftPQ) == len(self.rightPQ):
            if self.leftPQ and -self.leftPQ[0] > num:
                heapq.heappush(self.rightPQ, -heapq.heappop(self.leftPQ))
                heapq.heappush(self.leftPQ, -num)
            
            # num is at least as large as largest in left, or both PQ empty
            else:
                heapq.heappush(self.rightPQ, num)
        
        # in this case, the lengths of both are not the same
        # left = [1]
        # right = [100, 1000]
        elif len(self.leftPQ) < len(self.rightPQ):
            # num = 105
            if num > self.rightPQ[0]:
                heapq.heappush(self.leftPQ, -heapq.heappop(self.rightPQ))
                heapq.heappush(self.rightPQ, num)
            # num = 2
            else:
                heapq.heappush(self.leftPQ, -num)

        # left = [-4]
        # right = [5, 10]                
        else:
            print("bad if here")
        

    def findMedian(self) -> float:
        if self.count % 2 == 0:
            return((-self.leftPQ[0] + self.rightPQ[0]) / 2)
        else:
            return(self.rightPQ[0])


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
```