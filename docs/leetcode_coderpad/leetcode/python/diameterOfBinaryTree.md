---
title: diameterOfBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# diameterOfBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.resp = 0
        
        def dfs(node: Optional[TreeNode]):
            if node == None:
                return(0)
            
            left = dfs(node.left)
            right = dfs(node.right)
            max_here = max(left, right)
            
            self.resp = max(
                self.resp,
                left + right
            )
            return(max_here + 1)
        
        dfs(root)
        
        return(self.resp)
```