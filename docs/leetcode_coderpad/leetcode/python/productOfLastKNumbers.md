---
title: productOfLastKNumbers
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# productOfLastKNumbers

```python
class ProductOfNumbers:
    # [   2, 3, 5, 2]
    # [1, 2, 6, 30, 60]
    # last 4 = 60 / len(pfxMult) - 1 - 4
    #   = 60 / 1
    # lasr 3 = 60 / 2 = 30
    def __init__(self):
        self.pfxMult = [1]
        self.lastZeroIdx = None

    def add(self, num: int) -> None:
        if num == 0:
            self.lastZeroIdx = len(self.pfxMult)
            num = 1 # essentially restart    
    
        self.pfxMult.append(
            self.pfxMult[-1] * num
        )

    def getProduct(self, k: int) -> int:
        idx = len(self.pfxMult) - 1 - k
        if self.lastZeroIdx and idx < self.lastZeroIdx:
            return(0)
        
        return(
            self.pfxMult[-1] // self.pfxMult[idx]
        )


# Your ProductOfNumbers object will be instantiated and called as such:
# obj = ProductOfNumbers()
# obj.add(num)
# param_2 = obj.getProduct(k)
```