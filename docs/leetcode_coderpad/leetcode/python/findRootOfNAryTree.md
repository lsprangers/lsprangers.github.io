---
title: findRootOfNAryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findRootOfNAryTree

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val: Optional[int] = None, children: Optional[List['Node']] = None):
        self.val = val
        self.children = children if children is not None else []
"""

class Solution:
    def findRoot(self, tree: List['Node']) -> 'Node':
        # the tree List is generated in arbitrary order
        #   if self.children is None it is a leaf node
        #   we need to find the value that has no parent
        # we need to return the constructued tree
        
        # each node has a unique value
        valToNode = {}
        nodeToParent = {}
        potentialRoots = set()

        # O(n) - altogether we iterate over each node, but if there's 1 node with all children
        #   then this becomes a single O(n^2). i.e. c=n
        for node in tree:
            valToNode[node.val] = node
            potentialRoots.add(node.val)
            
            # # O(c)
            for childNode in node.children:
                nodeToParent[childNode] = node
                
        
        for nodeVal, node in valToNode.items():
            if node in nodeToParent:
                potentialRoots.remove(nodeVal)
        
        if len(potentialRoots) > 1:
            print('crap')
        
        
        return(valToNode[potentialRoots.pop()])
        
```