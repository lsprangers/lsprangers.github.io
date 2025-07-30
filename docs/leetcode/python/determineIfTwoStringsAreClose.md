---
title: determineIfTwoStringsAreClose
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# determineIfTwoStringsAreClose
Definition:
Two strings are considered close if you can attain one from the other using the following operations:

    Operation 1: Swap any two existing characters.
        For example, abcde -> aecdb
    Operation 2: Transform every occurrence of one existing character into another existing character, and do the same with the other character.
        For example, aacabb -> bbcbaa (all a's turn into b's, and all b's turn into a's)


This one's screwy:
- Operation1 equates to "must have the same letters in the strings" b/c we can't get to an unknown character in str2 if it's not in str1
- Operation2 equates to frequency counts because we can swap any existing frequencies, but we can't generate new characters if they don't exist

```python
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        w1_set = set([ch for ch in word1])
        w2_set = set([ch for ch in word2])

        if w1_set != w2_set:
            return(False)
        
        w1_freqs = Counter(word1)
        w2_freqs = Counter(word2)
        
        w1_swap = defaultdict(int)
        for cnt in w1_freqs.values():
            w1_swap[cnt] += 1

        w2_swap = defaultdict(int)
        for cnt in w2_freqs.values():
            w2_swap[cnt] += 1
        
        if w1_swap != w2_swap:
            return(False)
        
        return(True)
```