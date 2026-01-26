---
title: successfulPairsAndPotions
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# successfulPairsAndPotions

```python
class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        pairs = [0] * len(spells)
        potions.sort()

        for idx, spell in enumerate(spells):
            min_potion = math.ceil(success / spell)
            potion_idx = self.b_search(potions, min_potion)
            pairs[idx] = len(potions) - potion_idx
        
        return(pairs)
    
    def b_search(self, potions: List[int], min_potion: int):
        left = 0
        right = len(potions)
        # duplicates are involved
        while left < right:
            mid = left + (right - left) // 2
            # if it's g.t, it may be the last valid one
            #   so only squish window back to it
            if potions[mid] >= min_potion:
                right = mid
            # if it's not, then we know for sure it's not
            #   and can pass window forward
            else:
                left = mid + 1
        
        return(left)

```


Using `bisect_left`
- The bisect_left(a, x, ...) function takes a sorted list a and a value x and returns an index i such that: 
    - All elements to the left of the index (a[:i]) are less than x
    - All elements to the right of and at the index (a[i:]) are greater than or equal to x

```python
class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        pairs = [0] * len(spells)
        potions.sort()

        for idx, spell in enumerate(spells):
            min_potion = math.ceil(success / spell)
            # bisect_left gives us leftmost index or insertion point
            potion_idx = bisect.bisect_left(potions, min_potion)
            pairs[idx] = len(potions) - potion_idx
        
        return(pairs)
```        