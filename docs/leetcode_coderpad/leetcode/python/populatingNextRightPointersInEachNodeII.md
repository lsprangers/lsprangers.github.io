---
title: populatingNextRightPointersInEachNodeII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# populatingNextRightPointersInEachNodeII

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
"""

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        if not root:
            return
        
        dq = deque([root])

        while dq:
            levelSize = len(dq)
            for nodeIdx in range(levelSize):
                currNode = dq.popleft()
                if nodeIdx != levelSize - 1:
                    currNode.next = dq[0]
                
                if currNode.left:
                    dq.append(currNode.left)
                if currNode.right:
                    dq.append(currNode.right)
                
        return(root)
```