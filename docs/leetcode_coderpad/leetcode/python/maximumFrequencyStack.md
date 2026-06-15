---
title: maximumFrequencyStack
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumFrequencyStack

```python
class FreqStack:

    def __init__(self):
        # data structure to update counts, and keep a largest element 
        # tiebreaker via push counter
        self.freqs = {}
        self.maxHeap = []
        self.globalVersion = 0

    def push(self, val: int) -> None:
        if val not in self.freqs:
            self.versions[val] = 0
            self.freqs[val] = 0
        
        self.globalVersion += 1
        self.freqs[val] += 1
        
        # sort by max count and then latest timestamp / version
        heapq.heappush(self.maxHeap, (-self.freqs[val], -self.globalVersion, val))

    def pop(self) -> int:
        # guaranteed to have something
        thisCount, _, val = heapq.heappop(self.maxHeap)
        self.freqs[val] -= 1
        if self.freqs[val] == 0:
            del self.freqs[val]
        
        return(val)
        
        


# Your FreqStack object will be instantiated and called as such:
# obj = FreqStack()
# obj.push(val)
# param_2 = obj.pop()
```