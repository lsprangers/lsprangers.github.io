---
title: wordBreak
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# wordBreak

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # at each index we may have found a valid segment, but this may also be apart of a larger segment - app / apple 
        #   we need to see if, for each index, we can segment it based on ending segment of previous indexes 

        # during traversal, we just need to check if any index is apart of dict / set segment
        wordSet = set(wordDict)
        n = len(s)

        # (app, apple, lepe, pen)
        # [a, p, p, l, e, p, e, n, a, p, p, l, e]
        # [F, F, T, F, T, F, F, T, F, F, T, F, T]
        # [0, 0, 1, 0, 1, 0, 2, 2, 0, 0, 3, 0, 3]
        
        # shift by 1 so we don't have to check starting words idx == len(word) - 1 later on
        dp = [False] * (n + 1)
        dp[0] = True

        for idx in range(n + 1):
            for word in wordSet:
                # can't be long enough
                if idx < len(word) - 1:
                    continue
                
                # if we ended at a valid word before
                if dp[idx - len(word) + 1]:
                    # and from that last ended word to our current index is this word
                    if s[idx - len(word) + 1 : idx + 1] == word:
                        # we've ended at a word
                        dp[idx + 1] = True

        # if this is true, it must mean we have some word that started from either 0 or another
        #   valid word, and that word either started from 0 or another valid word, or....
        return(dp[-1])
```