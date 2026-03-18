---
title: longestZigZagPathBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestZigZagPathBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        # From root node, there's only 2 routes - it's not actually traversing all nodes
        # Actually that's wrong, there's a chance there is a subtree that has longest
        #   path that isn't reachable from root
        self.resp = 0

        def dfs(curr: Optional[TreeNode], goLeft: bool, steps: int):
            if not curr:
                return
            
            # might be a subtree with longest path, so we need to track in function calls and not at the end
            self.resp = max(self.resp, steps)
            if goLeft:
                dfs(curr.left, False, steps + 1)
                dfs(curr.right, True, 1) # restart subtree
            else:
                dfs(curr.left, False, 1) # restart subtree
                dfs(curr.right, True, steps + 1)
        
        # can be true or false
        dfs(root, False, 0)
        return(self.resp)
```