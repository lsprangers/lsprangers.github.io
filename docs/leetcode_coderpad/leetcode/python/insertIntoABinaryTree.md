---
title: insertIntoABinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# insertIntoABinaryTree

The proper python script:
```python
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return(TreeNode(val))
        
        if val > root.val:
            root.right = self.insertIntoBST(root.right, val)
        else:
            root.left = self.insertIntoBST(root.left, val)
        
        return(root)
```

My shitty little script that passes
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root:
            return(TreeNode(val))
        
        resp = root
        while root:
            if root.val < val:
                if root.right:
                    root = root.right
                else:
                    root.right = TreeNode(val)
                    break

            elif root.val > val:
                if root.left:
                    root = root.left
                else:
                    root.left = TreeNode(val)
                    break

        return(resp)    
```