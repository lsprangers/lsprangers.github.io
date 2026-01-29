---
title: maxDifferenceBetweenNodeAndAncestor
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxDifferenceBetweenNodeAndAncestor

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        # At each node need to host the max and min, and then update
        #   result to be max(result, biggest_diff_at_node)
        self.result = 0

        def dfs(node: Optional[TreeNode], curr_max: int, curr_min: int):
            # at leaf, the max and min will be node
            #   and diff will be 0
            if node == None:
                return(-float("inf"), float("inf"))
            
            left_max, left_min = dfs(node.left, curr_max, curr_min)
            right_max, right_min = dfs(node.right, curr_max, curr_min)
            
            curr_max = max(node.val, left_max, right_max)
            curr_min = min(node.val, left_min, right_min)
            
            self.result = max(
                self.result,
                abs(node.val - curr_max),
                abs(node.val - curr_min)
            )
            return(curr_max, curr_min)
            
            
        
        dfs(root, -float("inf"), float("inf"))
        return(self.result)
```