---
title: stoneGameIII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# stoneGameIII

```python
class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        # [1, 2, 3, 4, 18]
        # In this case, for Alice to play optimally, she would only choose [1]
        #   as this would ensure Bob can't get to 18
        # This means she can't be greedy, and we have to store state
        # The state of the game should be currPlayerScores, player, idx
        #   [1,0], Bob, 1
        #   [1,9], Alice, 4
        #   [19,9] Bob, 5
        #   return Alice

        # How does Alice get to that state by looking forward at array and playing optimally?
        # State at index i relates to max we can gain from pulling [i, i+1], [i, i+2], [i, i+3]
        #   and each of those in turn will relate down the chain until we get to a singular number
        # As usual in stone game we'd need to track player 

        # To efficiently use the cache, we just need to track the max at any specific idx. To actually
        #   pass that score to one player would be dependent on a few things...

        n = len(stoneValue)

        @cache
        def dp(idx):
            if idx >= n:
                return(0)
            
            best = -float("inf")
            curr = 0

            for k in range(3):
                if idx + k >= n:
                    break
                curr += stoneValue[idx + k]
                best = max(best, curr - dp(idx + k + 1))

            return best

            return(maxHere)

        diff = dp(0)

        if diff > 0:
            return "Alice"
        elif diff < 0:
            return "Bob"
        else:
            return "Tie"
```