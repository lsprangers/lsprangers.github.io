---
title: trappingRainWater
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# trappingRainWater

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        # Invariant: for any index with height h, the most it can trap is equal to a downstream index j with heght h* >= h would
        #   be min(h, h*)
        # The situation where we have something like 2, 0, 1 we need to somehow capture it handles 1 unit of rainwater
        #   and then situation of 2, 0, 1, 2, we would trap 1 unit + 2 units = 3 units
        # If we only pop off an index, or move left pointer, once we've seen a larger index to the right, that ensures we capture all
        #   possible downstream "water" - so in 2, 1, 0, 1, 2 we'd pop off the first 1 when we see the second 1, capture it's a 1 unit change,
        #   and pop off the first 2 with the second 2 and capture it as 3 units, so we can in total find 4 without complicated math
        # What gets weird is a situation at end of array with 2, 0, 1. Or in general in a case like 2, 0, 1, 2 - here we'd need to treat
        #   this like a monotonic stack or next day less than ours where we pop off the 1 


        # The mid valley tracking is what fucked me up in the first pass
        resp = 0
        stack = []
        for rightIdx in range(len(height)):
            while stack and height[rightIdx] > height[stack[-1]]:
                # item to left can be used as valley, adjacent's don't contribute to total size
                valleyIdx = stack.pop()

                while stack and height[rightIdx] > height[valleyIdx]:
                    leftIdx = stack[-1]

                    # only pop left off if it's bounded by right side, otherwise leave it in for future
                    if height[rightIdx] >= height[leftIdx]:
                        stack.pop()
                        
                    width = rightIdx - leftIdx - 1
                    minHeight = min(height[rightIdx], height[leftIdx]) - height[valleyIdx]
                    resp += max(width * minHeight, 0)

                    valleyIdx = leftIdx
            stack.append(rightIdx)
        
        return(resp)
```