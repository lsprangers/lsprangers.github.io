---
title: averageLevelsOfBinaryTree
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# averageLevelsOfBinaryTree

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        if not root:
            return([])
        
        dq = deque([root])
        resp = []

        while dq:
            levelSize = len(dq)
            currSum = 0
            currCount = 0
            for _ in range(levelSize):
                currNode = dq.popleft()
                currSum += currNode.val
                currCount += 1
                
                if currNode.left:
                    dq.append(currNode.left)
                if currNode.right:
                    dq.append(currNode.right)
            
            resp.append(currSum / currCount)
        
        return(resp)
```