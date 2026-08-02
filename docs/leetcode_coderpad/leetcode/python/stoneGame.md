---
title: stoneGame
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# stoneGame

The general idea with these games is that the subtraction switches off between the two players. As long as you know who starts the game, you can get a general idea of the difference. If the difference is greater than 0, the person who starts wins

The first person gets to choose left or right - their total score here is that value minus whatever the next chosen value is, as that value is chosen by the other player

As we move into the next `dp` call, that represents Bob. His score again represents either left or right part of array minus whatever the next chosen value is, as that's Alice's 2nd choice. This all boils down to some last choice which is when `left == right`, and at that point we just return the value which starts back up the chain

It's a deterministic outcome if both players choose optimally

```python
class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        n = len(piles)

        @cache
        def dp(left, right):
            if left == right:
                return(piles[left])
            
            return(
                max(
                    piles[left] - dp(left + 1, right),
                    piles[right] - dp(left, right - 1)
                )
            )
        
        alice = dp(0, n-1)
        return(alice > 0)
```