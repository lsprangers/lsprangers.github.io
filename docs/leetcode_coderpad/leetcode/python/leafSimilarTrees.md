---
title: leafSimilarTrees
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# leafSimilarTrees

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        leaf1 = []
        leaf2 = []

        def getLeaf(rootNode: TreeNode, append_to: List[int]):
            if not rootNode.left and not rootNode.right:
                append_to.append(rootNode.val)
                return
            
            if rootNode.left:
                getLeaf(rootNode.left, append_to)

            if rootNode.right:
                getLeaf(rootNode.right, append_to) 
            return              

        getLeaf(root1, leaf1)
        getLeaf(root2, leaf2)
        
        return(leaf1 == leaf2)
```