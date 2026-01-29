---
title: minDepthBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minDepthBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root == None:
            return(0)
        
        if root.left is None and root.right is None:
            return(1)
        elif root.left is None and root.right:
            return(
                1 + self.minDepth(root.right)
            )
        elif root.right is None and root.left:
            return(
                1 + self.minDepth(root.left)
            )     
        else:
            return(
                1 + min(
                    self.minDepth(root.left),
                    self.minDepth(root.right)
                )
            )
```