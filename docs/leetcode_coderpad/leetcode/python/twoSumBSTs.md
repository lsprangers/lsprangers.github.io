---
title: twoSumBSTs
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# twoSumBSTs

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def twoSumBSTs(self, root1: Optional[TreeNode], root2: Optional[TreeNode], target: int) -> bool:
        # [1,5000]
        oneLookup = set()
        stack = [root1]
        
        while stack:
            currNode = stack.pop()
            oneLookup.add(currNode.val)
            if currNode.left:
                stack.append(currNode.left)
            if currNode.right:
                stack.append(currNode.right)
            
        
        stack = [root2]
        
        while stack:
            currNode = stack.pop()
            need = target - currNode.val
            if need in oneLookup:
                return(True)
            
            if currNode.left:
                stack.append(currNode.left)
            if currNode.right:
                stack.append(currNode.right)        
        
        return(False)
```