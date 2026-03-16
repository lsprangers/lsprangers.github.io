---
title: countGoodNodesBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countGoodNodesBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        self.resp = 0

        def dfs(node: TreeNode, maxx: int):
            if not node:
                return
                
            if maxx <= node.val:
                self.resp += 1
            
            maxx = max(maxx, node.val)
            dfs(node.left, maxx)
            dfs(node.right, maxx)
        
        dfs(root, -float("inf"))
        return(self.resp)
```