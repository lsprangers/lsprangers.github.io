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
        # shortest transformation sequence === bfs
        
        wordSet = set(wordList)
        seen = set([beginWord])
        if endWord not in wordSet:
            return(0)
        
        dq = deque([beginWord])
        # bfs level is response - start at 1
        level = 1
        resp = float("inf")
        while dq:
            levelSize = len(dq)
            for _ in range(levelSize):
                currWord = dq.popleft()
                currWordList = [c for c in currWord]
                
                # [h, o, t]
                for cIdx, c in enumerate(currWordList):
                    
                    for otherChar in string.ascii_lowercase:
                        potentialNextWordList = currWordList[:]
                        potentialNextWordList[cIdx] = otherChar
                        
                        potentialNextWord = "".join(potentialNextWordList)
                        if potentialNextWord == endWord:
                            resp = min(resp, level + 1)
                            
                        if potentialNextWord in wordSet and potentialNextWord not in seen:
                            seen.add(potentialNextWord)
                            dq.append(potentialNextWord)
            
            level += 1
        
        return(resp if resp != float("inf") else 0)
```