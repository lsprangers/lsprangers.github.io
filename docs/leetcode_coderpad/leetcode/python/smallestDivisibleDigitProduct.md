---
title: smallestDivisibleDigitProduct
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestDivisibleDigitProduct

```python
class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        numList = []

        while n > 0:
            currDigit = n % 10
            n //= 10
            numList.append(currDigit)
        
        numList = numList[::-1]

        while math.prod(numList) % t != 0:
            numList = self.getNext(numList)
        
        _pow = 0
        resp = 0
        while numList:
            resp += (numList[-1] * (10 ** _pow))
            _pow += 1
            numList.pop()
        
        return(resp)
    
    def getNext(self, numList):
        idx = len(numList) - 1

        while idx > -1 and numList[idx] == 9:
            numList[idx] = 0
            idx -= 1
        
        if idx > -1:
            numList[idx] += 1
        
        else:
            numList = [1] + numList
        
        return(numList)

```