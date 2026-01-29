---
title: lowestCommonAncestor2
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# lowestCommonAncestor2

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        self.resp = None

        def dfs(node: 'TreeNode', p: 'TreeNode', q: 'TreeNode'):
            if node == None:
                return(None)
            
            left = dfs(node.left, p, q)
            right = dfs(node.right, p, q)
            
            # If both in subtree, this is answer
            if left and right:
                self.resp = node
                return(node)
            # one in tree, and this node is other one
            elif (left or right) and (node == p or node == q):
                self.resp = node
                return(node)
            # this is one of them, but haven't found others
            elif (node == p or node == q):
                return(node)
            # otherwise return left if we've found it in left
            elif left:
                return(left)
            # else either right has it, or it's None, so lump those 2 together
            else:
                return(right)

        dfs(root, p, q)
        return(self.resp)
```