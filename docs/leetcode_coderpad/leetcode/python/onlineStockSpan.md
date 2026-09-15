---
title: onlineStockSpan
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# onlineStockSpan

```python
class StockSpanner:
    # [7, 2, 1, 4, 8] --> a new value < 8 has no reason to include historic info
    #   but a new value like 9 does need to include it
    #   if we appended [1, 9, 1, 2], on the 1 if we deleted 
    #   tracking of 8 that's fine
    # [1, 1, 1, 3, 4]
    def __init__(self):
        self.stack = []
        self.currDay = 0

    def next(self, price: int) -> int:
        oldPrice, oldDay, oldStreak = price, self.currDay, 0

        while self.stack and self.stack[-1][0] <= price:
            oldPrice, oldDay, oldStreak = self.stack.pop()
        
        resp = self.currDay - oldDay + oldStreak + 1
        self.stack.append([price, self.currDay, resp - 1])
        self.currDay += 1
        return(resp)
        


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```