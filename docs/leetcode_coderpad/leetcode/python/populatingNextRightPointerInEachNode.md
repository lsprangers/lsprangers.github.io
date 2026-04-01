---
title: populatingNextRightPointerInEachNode
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# populatingNextRightPointerInEachNode

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
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root:
            return(root)
        
        dq = deque([root])
        # [2, 3]
        while dq:
            # 2
            level_size = len(dq)
            # idx=0
            for idx in range(level_size):
                # 2
                curr = dq.popleft()
                
                # 2.right = 3
                if idx != level_size - 1:
                    curr.next = dq[0]
                
                if curr.left and curr.right:
                    dq.append(curr.left)
                    dq.append(curr.right)
        
        return(root)
```