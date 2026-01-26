---
title: binaryTreeRightSideView
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# binaryTreeRightSideView

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root == None:
            return([])
        
        q = deque([root])
        resp = []

        while q:
            level_size = len(q)
            for idx in range(level_size):
                curr_node = q.popleft()
                if curr_node.left:
                    q.append(curr_node.left)
                if curr_node.right:
                    q.append(curr_node.right)
            resp.append(curr_node.val)
        
        return(resp)
```