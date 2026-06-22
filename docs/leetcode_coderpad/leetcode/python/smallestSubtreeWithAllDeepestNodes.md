---
title: smallestSubtreeWithAllDeepestNodes
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# smallestSubtreeWithAllDeepestNodes

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # find deepest level
        # get LCA of all nodes
        if not root:
            return(root)
        
        dq = collections.deque([root])
        deepest = None
        while dq:
            currLevelSize = len(dq)
            deepest = dq.copy()
            for _ in range(currLevelSize):
                currNode = dq.popleft()
                if currNode.left:
                    dq.append(currNode.left)
                if currNode.right:
                    dq.append(currNode.right)
        
        lca = deepest[0]
        if len(deepest) == 1:
            return(lca)
        
        for node in deepest:
            lca = self.getLCA(root, lca, node)
        
        return(lca)
    
    
    def getLCA(self, curr: TreeNode, p: TreeNode, q: TreeNode):
        if not curr:
            return(None)
        
        if curr == p or curr == q:
            return(curr)
        
        right = self.getLCA(curr.right, p, q)
        left = self.getLCA(curr.left, p, q)
        
        if right and left:
            return(curr)
        elif right:
            return(right)
        
        return(left)
        
        
        
```