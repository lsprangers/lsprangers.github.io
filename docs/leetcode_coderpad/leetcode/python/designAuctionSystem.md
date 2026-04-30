---
title: designAuctionSystem
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# designAuctionSystem

```python
class AuctionSystem:

    def __init__(self):
        # itemId -> heap[ (bidAmount, userId, version) ]
        self.bidForItem = {}

        # (userId, itemId) -> int
        self.userBidVersion = {}

    def addBid(self, userId: int, itemId: int, bidAmount: int) -> None:
        userBidKey = (userId, itemId)
        if userBidKey not in self.userBidVersion:
            self.userBidVersion[userBidKey] = 1
        else:
            self.userBidVersion[userBidKey] += 1
        

        # amount, userId, currVersion
        # sorted by -amount, -userId for maxHeap based on amount, userId
        heapKey = (-bidAmount, -userId, self.userBidVersion[userBidKey])
        
        if itemId not in self.bidForItem:
            self.bidForItem[itemId] = [heapKey]
        else:
            heapq.heappush(self.bidForItem[itemId], heapKey)

    def updateBid(self, userId: int, itemId: int, newAmount: int) -> None:
        self.addBid(userId, itemId, newAmount)

    def removeBid(self, userId: int, itemId: int) -> None:
        # 1 <= bidAmount, so we are treating 0 as a tombstone
        self.addBid(userId, itemId, 0)

    def getHighestBidder(self, itemId: int) -> int:
        if itemId not in self.bidForItem or len(self.bidForItem[itemId]) == 0:
            return(-1)

        bidsForItem = self.bidForItem[itemId]
        # will clear this heap out for now
        # self.bidForItem[itemId][-1] = (-amount, -userId, version)

        # while heap exists, and highest value isn't current version, and current largest isn't 0
        while bidsForItem and (bidsForItem[0][2] != self.userBidVersion[(-bidsForItem[0][1], itemId)] or -bidsForItem[0][0] == 0):
            heapq.heappop(bidsForItem)
        
        self.bidForItem[itemId] = bidsForItem
        if not bidsForItem:
            return(-1)
        
        return(-bidsForItem[0][1])

        


# Your AuctionSystem object will be instantiated and called as such:
# obj = AuctionSystem()
# obj.addBid(userId,itemId,bidAmount)
# obj.updateBid(userId,itemId,newAmount)
# obj.removeBid(userId,itemId)
# param_4 = obj.getHighestBidder(itemId)
```