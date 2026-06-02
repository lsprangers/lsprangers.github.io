---
title: minCostOfBuyingCandiesWithDiscount
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minCostOfBuyingCandiesWithDiscount

```python
class Solution:
    def minimumCost(self, cost: List[int]) -> int:
        # [6,5,7,9,2,2]
        # [2,2,5,6,7,9]
        # 2, 5, get 2
        # 7, 9, get 6
        cost.sort()
        resp = 0
        while cost:
            if len(cost) > 2:
                resp += cost.pop()
                resp += cost.pop()
                cost.pop()
            else:
                resp += sum(cost)
                break
        
        return(resp)
```