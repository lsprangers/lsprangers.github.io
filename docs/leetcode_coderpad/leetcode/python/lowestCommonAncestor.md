---
title: template
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# template
This one utilizes [DFS](/docs/dsa/8.%20trees%20&%20graphs/index.md#depth-first-search) where the other problem [lcaBinaryTree](/docs/leetcode_coderpad/leetcode/python/lcaBinaryTree.md) uses a queue, seems they are different problems with the same name

This question shows up friggin everywhere - the `return n_left or n_right or resp` is what allows recursion. `resp` can never be 2 without `n_left` or `n_right` also having a value, so we set `self.resp = root` if currently `resp = 2`, and then we return `n_left, n_right, OR resp` up the chain:
- If we have found both, then either `n_left` or `n_right` will move up the chain
- If we've only found one, then one of the 3, including `resp`, would move up the chain
- If none are found, `resp = 0` moves up the chain

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
        if left:
            return(left)
        
        # otherwise we either found right, or we send up None
        return(right)
```

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        self.resp = root

        def dfs(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode'):
            if not root:
                return(0)
            
            n_left = dfs(root.left, p, q)
            n_right = dfs(root.right, p, q)
            resp = n_left + n_right

            if root == p or root == q:
                resp += 1
            
            if resp >= 2:
                self.resp = root
            
            # don't return resp, return just 1
            return n_left or n_right or resp
        
        dfs(root, p, q)
        return(self.resp)
```