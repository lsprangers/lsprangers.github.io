---
title: kokoEatingBananas
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# kokoEatingBananas

```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # min is 1 because there's a chance only eat 1 banana per hour, but
        #   there's enough hours to eat everything
        # max is max(piles):
        #   - If there were only 1 piles you could use sum(piles), 
        #       but has to stop at each hour and not eat more
        #   - Therefore, max(piles) ensures you eat every banana at each hour
        low = 1
        high = max(piles)
        
        # need to find last valid (highest) value
        while low < high:
            mid = (low + high) // 2
            # if this rate works, pull window in but may still be valid so keep it
            if self.check(mid, piles, h):
                high = mid
            # else, is not valid shrink search space
            else:
                low = mid + 1
        
        return(low)
    
    def check(self, rate: int, piles: List[int], h: int) -> bool:
        resp = 0
        for pile_size in piles:
            resp += math.ceil(pile_size / rate)
            if resp > h:
                return(False)
        
        # return(resp <= h)
        return(True)
```