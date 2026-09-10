---
title: countNodesEqualToAverageOfSubtree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countNodesEqualToAverageOfSubtree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfSubtree(self, root: TreeNode) -> int:
        # post order allows us to get sum of left and right
        #   along with count, and then compare to current node
        self.resp = 0
        self.postorder(root)
        return(self.resp)

    def postorder(self, node: Optional[TreeNode]) -> tuple[int, int]:
        if not node:
            return(0, 0)
        
        leftSum, leftCount = self.postorder(node.left)
        rightSum, rightCount = self.postorder(node.right)
        thisTotal = node.val + leftSum + rightSum
        thisCount = 1 + leftCount + rightCount
        if thisTotal // thisCount == node.val:
            self.resp += 1
        
        return(thisTotal, thisCount)
```