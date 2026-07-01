---
title: boundaryOfBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# boundaryOfBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def boundaryOfBinaryTree(self, root: Optional[TreeNode]) -> List[int]:
        resp = [root.val]
        
        if root.left:
            resp += self.traverseLeft(root.left, [])
        
        if root.left or root.right:
            resp += self.getLeaves(root)
        
        if root.right:
            r = self.traverseRight(root.right, [])
            r.reverse()
            resp += r
        
        return(resp)
            
    def getLeaves(self, node: TreeNode):
        stack = [node]
        resp = []
        
        while stack:
            curr = stack.pop()
            if not curr.left and not curr.right:
                resp.append(curr.val)

            if curr.right:
                stack.append(curr.right)                
            if curr.left:
                stack.append(curr.left)

        
        return(resp)
                
    def traverseRight(self, node: TreeNode, curr):
        # if leaf
        if not node.left and not node.right:
            return(curr)
        
        if node.right:
            curr.append(node.val)
            curr = self.traverseRight(node.right, curr)
        
        elif node.left:
            curr.append(node.val)
            curr = self.traverseRight(node.left, curr)
        
        return(curr)
        
        
    def traverseLeft(self, node: TreeNode, curr):
        # if leaf
        if not node.left and not node.right:
            return(curr)
        
        if node.left:
            curr.append(node.val)
            curr = self.traverseLeft(node.left, curr)
        
        elif node.right:
            curr.append(node.val)
            curr = self.traverseLeft(node.right, curr)
        
        return(curr)
        
```