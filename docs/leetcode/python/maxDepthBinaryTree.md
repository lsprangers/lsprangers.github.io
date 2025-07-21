---
title: maxDepthBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxDepthBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        s = []
        if root is not None:
            s.append((1, root))

        resp = 0
        while s != []:
            curr_depth, curr_node = s.pop()
            if curr_node is not None:
                resp = max(resp, curr_depth)
                s.append((curr_depth + 1, curr_node.left))
                s.append((curr_depth + 1, curr_node.right))
        
        return(resp)
```