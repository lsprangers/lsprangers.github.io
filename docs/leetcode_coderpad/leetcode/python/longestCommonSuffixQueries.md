---
title: longestCommonSuffixQueries
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestCommonSuffixQueries
I am shocked I got this one myself on daily

```python
class ExtraTrie:
    def __init__(self):
        self.root = ExtraTrieNode()
        self.currWordsIncluded = 0
    
    def getLongestCommonSuffix(self, word):
        curr = self.root
        for idx in range(len(word)):
            _char = word[idx]
            if curr.hasNextChar(_char):
                curr = curr.getNextCharNode(_char)
            else:
                break

        return(curr.choiceHere)

                            
    def hasWord(self, word):
        curr = self.root
        for idx in range(len(word)):
            _char = word[idx]
            if curr.hasNextChar(_char):
                curr = curr.getNextCharNode(_char)
            else:
                return(False)
        
        return(curr.isEnd)

    def addWord(self, word):
        if self.hasWord(word):
            return

        # update root node
        curr = self.root        
        if not curr.choiceHere or len(word) < len(curr.choiceHere):
            curr.choiceHere = word


        for idx in range(len(word)):
            _char = word[idx]
            if not curr.hasNextChar(_char):
                curr.addNextChar(_char)
            
            curr = curr.getNextCharNode(_char)

            if idx == len(word) - 1:
                curr.isEnd = True
                
            if not curr.choiceHere or len(word) < len(curr.choiceHere):
                curr.choiceHere = word
            elif len(word) == len(curr.choiceHere):
                # choiceHere must have come first in word addition,
                #   so keep it in
                continue                
        
        return


class ExtraTrieNode:
    def __init__(self):
        self.next = {}
        self.isEnd = False
        self.choiceHere = None

    def addNextChar(self, _char) -> 'ExtraTrieNode':
        key = ord(_char) - ord('a')
        if key not in self.next:
            self.next[key] = ExtraTrieNode()
        
        return(self.next[key])
    
    def hasNextChar(self, _char):
        key = ord(_char) - ord('a')
        if key in self.next:
            return(True)
        return(False)
    
    def getNextCharNode(self, _char):
        key = ord(_char) - ord('a')
        if not self.hasNextChar(_char):
            raise ValueError("no key")

        return(self.next[key])       


class Solution:
    def stringIndices(self, wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
        trie = ExtraTrie()
        wordToIdx = {}
        for idx, word in enumerate(wordsContainer):
            wordRev = word[::-1]
            trie.addWord(wordRev)
            if wordRev not in wordToIdx:
                wordToIdx[wordRev] = idx

        resp = []
        for query in wordsQuery:
            bestWord = trie.getLongestCommonSuffix(query[::-1])
            resp.append(wordToIdx[bestWord])
        
        return(resp)

```