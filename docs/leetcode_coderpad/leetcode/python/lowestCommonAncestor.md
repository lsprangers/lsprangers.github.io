---
title: template
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# template
This one utilizes [DFS](/docs/dsa/8.%20trees%20&%20graphs/index.md#depth-first-search) where the other problem [lcaBinaryTree](/docs/leetcode_coderpad/leetcode/python/lcaBinaryTree.md) uses a queue, seems they are different problems with the same name

```python
#236
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return(None)
        
        # This one is weird - in the case of 5,4 with 3 at the top, this will return
        #   5 right away without checking for 4..
        #       if 4 is below it, then 5 is still the answer
        #       if 4 is not a child of 5, we still return 5 here
        #       and the "3" node will see 5 come in from that call,
        #       but it will not have anything returned from right
        #       the right call to 1 will result in None, and so
        #       checking if left and right will not work, therefore
        #       we know it's not the 3 root node. Therefore, since 3's
        #       right didn't return ANYTHING, and the 5 did, the 4 can only
        #       be situated under the 5
        #   jfc
        if root == p or root == q:
            return(root)
        
        # traverse, if p or q are in here we'll find them
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # If we've found both, send root up the stack
        if left and right:
            return(root)
        
        # if we've only found left, send it up
        if right:
            return(right)
        
        # otherwise we either found right, or we send up None
        return(left)

```