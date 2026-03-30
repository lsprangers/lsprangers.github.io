---
title: deleteNodeInBST
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# deleteNodeInBST

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        if not root:
            return root

        if root.val > key:
            root.left = self.deleteNode(root.left, key)
        elif root.val < key:
            root.right = self.deleteNode(root.right, key)
        else:
            # we're at the node
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            
            # 2 children
            successor = self.get_node_inorder_successor(root)
            root.val = successor.val
            # alter this if it's not inorder successor
            # we need to remove the node we overwrote root
            #   with
            root.right = self.deleteNode(root.right, successor.val)  

        return(root)          
        
    # Use this to get a node's successor before deletion
    def get_node_inorder_successor(self, node):
        node = node.right
        # inorder successor - get smallest value in right
        #   subtree. This is next greater value than current
        #   node
        while node and node.left is not None:
            node = node.left
        return(node)

# Replacement:
# Case 1: No children, just delete the node
# Case 2: One child, just replace deletion node with child
# Case 3: Two children
#   The inorder successor — the smallest value in the right subtree, which is the next greater value than the target node.
#   The inorder predecessor — the largest value in the left subtree, which is the next smaller value than the target node.
#   Once the replacement node is chosen, we replace the target node’s value with that node’s value, and then delete the 
#       replacement node, which will now fall under Case 1 (no children) or Case 2 (one child).
```