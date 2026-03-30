---
title: twoSumIV
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# twoSumIV

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        if not root:
            return(False)
        
        self.freqs = defaultdict(int)
        self.k = k
        self.found = False
        
        def dfs(node):
            # exit early 
            if self.found or not node:
                return
            
            # k = 10, val = 7, need 3 elsewhere
            # k = -4, val = 8, need -4 - 8 = 12
            # k = -3, val = -6, need 3
            # k = 10, val = -3, need 13 elsewhere
            # k = 10, val = 13 need 10 - 13 = -3
            # if (k < 0 and node.val > 0) or (node.val < 0 and k > 0):
            #     need = abs(self.k - node.val)
            # else:
            need = self.k - node.val
            
            # checking this val first, so pre-order
            if self.freqs[need] > 0:
                self.found = True
            
            self.freqs[node.val] += 1
            
            dfs(node.left)
            dfs(node.right)
        
        dfs(root)
        
        return(self.found)
```