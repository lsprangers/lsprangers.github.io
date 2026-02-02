---
title: maxLevelSumBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxLevelSumBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        maxx = -float('inf')
        curr_level = 0
        resp = -1
        q = deque([root])

        while q:
            curr_level_size = len(q)
            curr_sum = 0
            curr_level += 1
            for _ in range(curr_level_size):
                curr = q.pop()
                curr_sum += curr.val
                if curr.left:
                    q.appendleft(curr.left)
                if curr.right:
                    q.appendleft(curr.right)
            if curr_sum > maxx:
                maxx = curr_sum
                resp = curr_level
        
        return(resp)

```