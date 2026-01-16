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

Another one of having to relearn this crap
```python
from math import ceil

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # Find k such that koko can eat as slowly as possible while eating all bananas
        # Search space would be over banana eating rate, which min would be 1 banana
        #   and max would be the maximum pile size of bananas (can only eat that much
        #   since koko won't move on to next pile)
        low = 1
        high = max(piles)

        # Looking for lowest rate, not exact, so it's left bias
        while low < high:
            mid = (low + high) // 2
            # If mid is valid, go left and look for lower numbers
            if self.check(mid, piles, h):
                high = mid
            # mid for sure doesn't work, so move bound up one
            else:
                low = mid + 1
        
        # if high < low, then low was the last one we saw that was valid
        #   1. low never changed, and so it's the lowest possible min
        #   2. low did change, it became some mid + 1 in search space
        #       if this is true, and high < low, that means the mid calculation
        #       was done on 2 numbers next to each other (3 + 4) // 2 = 3
        #       (3 + 5) // 2 = 4
        #   So this only happens if we've exhausted our search space down
        return(low)
    
    def check(self, rate, piles, h):
        total_time = 0
        for pile in piles:
            total_time += ceil(pile / rate)
        
        return(total_time <= h)
```