---
title: binaryTreeMaxPathSum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# binaryTreeMaxPathSum

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.resp = -float("inf")
        self.dfs(root)

        return(self.resp)
    

    def dfs(self, node: Optional[TreeNode]):
        if not node:
            return(0)
        
        # children could be negative, which is useless. Root by itself would be 
        #   more
        leftTotal = max(0, self.dfs(node.left))
        rightTotal = max(0, self.dfs(node.right))

        # pass through middle - just check it here, send up max total through tree
        self.resp = max(
            self.resp,
            leftTotal + rightTotal + node.val
        )

        return(
            node.val + max(leftTotal, rightTotal)
        )

```