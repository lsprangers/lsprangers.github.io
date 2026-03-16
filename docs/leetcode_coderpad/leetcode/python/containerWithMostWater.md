---
title: containerWithMostWater
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# containerWithMostWater

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        resp = 0
        while left <= right:
            resp = max(
                resp,
                (right - left) * min(height[left], height[right])
            )
            # Always move lower one - the area formed is always
            #   limited by the height of the shorter line
            if height[left] > height[right]:
                right -= 1
            else:
                left += 1
        
        return(resp)
```

## Proof
The matrix representation / proof [here](https://leetcode.com/problems/container-with-most-water/solutions/6099/yet-another-way-to-see-what-happens-in-the-on-algorithm/) is probably the most intuitive in my opinion

Creating a matrix of size `height`, where the row represents `left` and the column represents `right`, gives us a matrix of `height x height` - lets say it's 6

All of the diagonals don't need to be computed as they're 0, and all of the lower left don't have to be computed as they're covered by the upper right

In the one below, we compute `[1, 6]` as it's the ends of the container, and it's the natural place to start. In this specific example, assume the container at 1 is shorter than 6, so we place `-----` there to show that there's no reason for us to check the rest 1-5. The reasoning is that since 6 is larger than 1, the volume we have is maximum for 1-6 based on 1, if 5 is larger than 6, there's no more we can get out of it (because 1 is smaller than 5 > 6 > 1), and we just lost one unit of width, and even worse if 5 is smaller than 1, then we lose one unit of width and we lose even more units of height
```
  1 2 3 4 5 6
1 x ------- o
2 x x
3 x x x 
4 x x x x
5 x x x x x
6 x x x x x x
```

If we cannot move anywhere along the 1 row axis, then our only logical step is to go and compute `[2, 6]`. There, assume that 2 > 6, and so we can completely rule out the column of 6

```
  1 2 3 4 5 6
1 x ------- o
2 x x       o
3 x x x     |
4 x x x x   |
5 x x x x x |
6 x x x x x x
```

So on and so forth we can traverse the only "optimal" paths, and only compute `n - 1` entries

```
  1 2 3 4 5 6
1 x ------- o
2 x x - o o o
3 x x x o | |
4 x x x x | |
5 x x x x x |
6 x x x x x x
```