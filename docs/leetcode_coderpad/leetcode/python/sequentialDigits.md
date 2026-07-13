---
title: sequentialDigits
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# sequentialDigits

```python
class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        self.low = low
        self.high = high
        self.nDigitsLow = len(str(self.low))
        self.nDigitsHigh = len(str(self.high))

        self.resp = []
        for nDigits in range(self.nDigitsLow, self.nDigitsHigh + 1):
            self.generate(nDigits)
        
        return(self.resp)
    
    def generate(self, nDigits):
        curr = collections.deque([x for x in range(1, nDigits + 1)])
        currNum = self.listToNum(curr)

        while curr[-1] < 10:
            if self.check(currNum):
                self.resp.append(currNum)
            curr.popleft()
            curr.append(curr[-1] + 1)
            currNum = self.listToNum(curr)

        return

    
    def listToNum(self, curr):
        currCopy = curr.copy()
        currPow = 0
        resp = 0
        while currCopy:
            resp += currCopy.pop() * (10 ** currPow)
            currPow += 1
        
        return(resp)

    def check(self, num):
        return(
            self.low <= num <= self.high
        )

```