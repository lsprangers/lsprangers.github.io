---
title: binarySearchTreeToGreaterSumTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# binarySearchTreeToGreaterSumTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def bstToGst(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # any node is passedSum - leftSum
        #   pass node - curr.val to the right
        #   pass node + 
        
        self.dfs(root, self.getSum(root))
        return(root)

    def getSum(self, node: Optional[TreeNode]) -> int:
        if not node:
            return(0)
        
        totalSum = 0
        stack = [node]
        while stack:
            currNode = stack.pop()
            totalSum += currNode.val
            if currNode.left:
                stack.append(currNode.left)
            if currNode.right:
                stack.append(currNode.right)

        return(totalSum)

    # totalSum at root is 36
    def dfs(self, node: Optional[TreeNode], currSum: int) -> Optional[TreeNode]:
        if not node:
            return(None)
        currVal = node.val
        leftSum = self.getSum(node.left)
        node.val = currSum - leftSum
        
        node.left = self.dfs(node.left, currSum)
        node.right = self.dfs(node.right, currSum - leftSum - currVal)

        return(node)
```