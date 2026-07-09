---
title: deepestLeavesSum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# deepestLeavesSum

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deepestLeavesSum(self, root: Optional[TreeNode]) -> int:
        dq = collections.deque([root])
        resp = 0
        
        while dq:
            levelSize = len(dq)
            resp = 0
            
            for _ in range(levelSize):
                currNode = dq.popleft()
                resp += currNode.val
                if currNode.left:
                    dq.append(currNode.left)
                if currNode.right:
                    dq.append(currNode.right)
        
        return(resp)            
```