---
title: wordLadder
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# wordLadder

```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wordSet = set(wordList)
        if endWord not in wordSet:
            return(0)
        
        resp = float("inf")
        seen = set([beginWord])

        dq = deque([(beginWord, 1)])

        while dq:
            currWordStr, nTransform = dq.popleft()
            currWordList = [c for c in currWordStr]

            for idx, char in enumerate(currWordList):
                potentialWordList = currWordList[:]
                for letter in string.ascii_lowercase:
                    potentialWordList[idx] = letter
                    potentialWordStr = "".join(potentialWordList)
                    if potentialWordStr == endWord:
                        resp = min(resp, nTransform + 1)

                    if potentialWordStr not in seen and potentialWordStr in wordSet:
                        dq.append((potentialWordStr, nTransform + 1))
                        seen.add(potentialWordStr)
        
        return(0 if resp == float("inf") else resp)

```