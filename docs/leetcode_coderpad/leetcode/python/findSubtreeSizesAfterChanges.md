---
title: findSubtreeSizesAfterChanges
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findSubtreeSizesAfterChanges

```python
class Solution:
    def findSubtreeSizes(self, parent: List[int], s: str) -> List[int]:
        # loop over all, find closest node. Needs to run on original
        # then create response
        self.parentCopy = parent.copy()
        n = len(s)

        self.parentToChildren = defaultdict(list)
        for node in range(n):
            self.parentToChildren[parent[node]].append(node)

        seen = [None] * 26
        self.findClosestAncestor(0, parent, s, seen)
        
        self.parentToChildren = defaultdict(list)
        for node in range(n):
            self.parentToChildren[self.parentCopy[node]].append(node)

        self.resp = [0] * n
        self.findSubtreeSize(0) # start with root
        
        return(self.resp)
    
    def findSubtreeSize(self, node: int):
        nodeSubtreeSize = 0
        for child in self.parentToChildren[node]:
            nodeSubtreeSize += 1
            nodeSubtreeSize += self.findSubtreeSize(child)
        
        self.resp[node] = nodeSubtreeSize + 1
        return(nodeSubtreeSize)
    
    def findClosestAncestor(self, node: int, parent: List[node], s: str, seen: List[int]):
        def getKey(node: int):
            return(
                ord(s[node]) - ord('a')                
            )

        if seen[getKey(node)] != None:
            self.parentCopy[node] = seen[getKey(node)]
        
        seen[getKey(node)] = node
        for child in self.parentToChildren[node]:
            self.findClosestAncestor(child, parent, s, seen[:])
        
        return
```