---
title: findLeavesOfBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findLeavesOfBinaryTree
First implementation time complexity would be $O(V)$ for initial pass, then $O(V - leaves)$ for second pass, etc so if there are $L$ levels think it's $O(L \ times V)$

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findLeaves(self, root: Optional[TreeNode]) -> List[List[int]]:
        # postorder traversal means we are at root after leaves
        self.resp = []
        self.curr = []
        # could also get levels and insert into levels on the fly instead of is_child,
        #   but hard to do if left is child, but right is 200 levels deep

        def dfs(node: Optional[TreeNode]):
            is_child = False

            if node == None:
                return(node, is_child)

            left, left_is_child = dfs(node.left)
            right, right_is_child = dfs(node.right)
            
            if not left and not right:
                self.curr.append(node.val)
                is_child = True
            
            if left_is_child:
                node.left = None
            if right_is_child:
                node.right = None
            
            return(node, is_child)

        while root:
            _, root_is_child = dfs(root)
            self.resp.append(self.curr)
            self.curr = []
            if root_is_child:
                break
        
        return(self.resp)
```

### Better DFS Implementation
This one used an inverted height so we don't have to do any sorting or anything - essentially uses any child as inverted height 0 and builds backwards from there

This is $O(n)$ time complexity, as we traverse all nodes twice in 2 separate function calls, and $O(n)$ space given response 

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findLeaves(self, root: Optional[TreeNode]) -> List[List[int]]:
        
        self.maxHeight = 0

        def getHeight(node: Optional[TreeNode], curr_height: int):
            # child nodes at bottom should be at 0, not 1
            if node == None:
                return(-1)
            
            left = getHeight(node.left, curr_height + 1)
            right = getHeight(node.right, curr_height + 1)
            curr_height = 1 + max(left, right)

            self.maxHeight = max(self.maxHeight, curr_height)
            return(curr_height)

        def dfs(node: Optional[TreeNode]):
            # child nodes at bottom should be at 0, not 1
            if node == None:
                return(-1)
            
            left_inverted_height  = dfs(node.left)
            right_inverted_height  = dfs(node.right)

            curr_inverted_height = 1 + max(left_inverted_height, right_inverted_height)
            self.resp[curr_inverted_height].append(node.val)

            return(curr_inverted_height)

        self.maxHeight = getHeight(root, 0)

        # need [[], [], []] for 3 levels, so + 1
        self.resp = [[] for _ in range(self.maxHeight + 1)]
        dfs(root)
        return(self.resp)
```

### Topological Sort Implementation
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def findLeaves(self, root: Optional[TreeNode]) -> List[List[int]]:
        self.parent_to_child = defaultdict(int) # really we just need to track count here, not mapping
        self.child_to_parent = defaultdict(TreeNode)
        self.curr_children = deque([])

        # Build out adj list - essentially make this a graph
        #   O(V + E)
        def dfs(node: Optional[TreeNode]):
            if node == None:
                return(node)
            
            if node.left != None:
                self.child_to_parent[node.left] = node
                self.parent_to_child[node] += 1 #.append(node.left)
            if node.right != None:
                self.child_to_parent[node.right] = node
                self.parent_to_child[node] += 1 #.append(node.right)
            
            left = dfs(node.left)
            right = dfs(node.right)

            # curr out_degree = 0 i.e. children
            if not left and not right:
                self.curr_children.appendleft(node)
            
            return(node)
        
        # child_to_parent = {2: 1, 3: 1, 4: 2, 5: 2}
        # parent_to_child = {1: 2, 2: 2}
        # curr_children = [5, 4]
        dfs(root)

        # O(V + E)
        resp = []
        while self.curr_children:
            level_size = len(self.curr_children)
            curr_level_children = []

            for _ in range(level_size):
                curr_child = self.curr_children.pop()
                curr_level_children.append(curr_child.val)
                curr_child_parent = self.child_to_parent[curr_child]
                self.parent_to_child[curr_child_parent] -= 1
                if self.parent_to_child[curr_child_parent] == 0:
                    self.curr_children.appendleft(curr_child_parent)
            
            resp.append(curr_level_children)
        
        return(resp)
```