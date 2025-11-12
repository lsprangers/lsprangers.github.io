---
title: smallestNumberInInfiniteSet
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestNumberInInfiniteSet

```python

class SmallestInfiniteSet:

    def __init__(self):
        self.curr = 1
        self.added = []
        self.added_lookup = set()

    def getSmallestInAdded(self) -> Union[int, None]:
        if len(self.added) > 0:
            resp = heapq.heappop(self.added)
            self.added_lookup.remove(resp)
        else:
            resp = None

        return(resp)

    def popSmallest(self) -> int:
        smallest_added = self.getSmallestInAdded()
        if smallest_added:
            # you won't addBack a number larger than self.curr, so 
            # if something is in here it should be smaller
            resp = smallest_added
        else:
            resp = self.curr
            self.curr += 1
        
        return(resp)

    def addBack(self, num: int) -> None:
        if num < self.curr and not num in self.added_lookup:
            self.added_lookup.add(num)
            heapq.heappush(self.added, num)
        


# Your SmallestInfiniteSet object will be instantiated and called as such:
# obj = SmallestInfiniteSet()
# param_1 = obj.popSmallest()
# obj.addBack(num)

```