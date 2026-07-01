---
title: designAnExpressionTreeWithAnEvaluationFunction
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# designAnExpressionTreeWithAnEvaluationFunction

```python
import abc 
from abc import ABC, abstractmethod 
"""
This is the interface for the expression tree Node.
You should not remove it, and you can define some classes to implement it.
"""

class Node(ABC):
    def __init__(self, nodeType: int, val: str, left: Optional['Node'], right: Optional['Node']):
        self.nodeType = nodeType
        self.val = val
        self.left = left
        self.right = right        

    def evaluate(self) -> int:
        if self.nodeType == 1:
            return(int(self.val))
        
        l = self.left.evaluate()
        r = self.right.evaluate()
        
        match self.val:
            case '+':
                return(l + r)
            case '-':
                return(l - r)
            case '/':
                return(int(l // r))
            case '*':
                return(int(l * r))                                             


"""    
This is the TreeBuilder class.
You can treat it as the driver code that takes the postinfix input
and returns the expression tree representing it as a Node.
"""

class TreeBuilder(object):
    def buildTree(self, postfix: List[str]) -> 'Node':
        stack = []
        for it in postfix:
            if it.isnumeric():
                numNode = Node(1, it, None, None)
                stack.append(numNode)
            else:
                rightNode = stack.pop()
                leftNode = stack.pop()
                opNode = Node(0, it, leftNode, rightNode)
                stack.append(opNode)
        
        return(stack[0])
		
"""
Your TreeBuilder object will be instantiated and called as such:
obj = TreeBuilder();
expTree = obj.buildTree(postfix);
ans = expTree.evaluate();
"""
```