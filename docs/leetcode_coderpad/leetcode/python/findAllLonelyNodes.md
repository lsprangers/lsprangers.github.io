---
title: findAllLonelyNodes
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findAllLonelyNodes

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def getLonelyNodes(self, root: Optional[TreeNode]) -> List[int]:
        self.resp = []

        def dfs(node: Optional[TreeNode]):
            if node == None:
                return(node)
            
            left = dfs(node.left)
            right = dfs(node.right)
                        
            # one exclusive child
            if (bool(left) ^ bool(right)):
                if left:
                    self.resp.append(left.val)
                else:
                    self.resp.append(right.val)
            
            return(node)
            

        dfs(root)
        return(self.resp)
```