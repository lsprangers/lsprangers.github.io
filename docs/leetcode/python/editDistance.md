---
title: editDistance
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# editDistance

This is literally a pull of [Levenshtein Distance](/docs/dsa/implementations/levenshtein.md)

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        dp = [ [0 for _ in range(len(word2) + 1)] for _ in range(len(word1) + 1)]
        
        # fill left col
        for i in range(len(word1) + 1):
            dp[i][0] = i
        
        # fill top row
        for i in range(len(word2) + 1):
            dp[0][i] = i

        for row in range(1, len(word1) + 1):
            for col in range(1, len(word2) + 1):
                dp[row][col] = min(
                    dp[row - 1][col - 1], 
                    dp[row - 1][col],
                    dp[row][col - 1]
                ) + (0 if word1[row - 1] == word2[col - 1] else 1)

        return(dp[-1][-1])  
```