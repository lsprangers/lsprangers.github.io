---
title: printImmutableLinkedListInReverse
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# printImmutableLinkedListInReverse

```python
# """
# This is the ImmutableListNode's API interface.
# You should not implement it, or speculate about its implementation.
# """
# class ImmutableListNode:
#     def printValue(self) -> None: # print the value of this node.
#     def getNext(self) -> 'ImmutableListNode': # return the next node.

class Solution:
    def printLinkedListInReverse(self, head: 'ImmutableListNode') -> None:
        # O(n ^ 2) would be getting length, and iterating over everything whiel
        #   reducing print index 
        # iterate to n, print
        # iterate to n - 1, print
        # ...
        # iterate to 1, print
        # n^2 operations
        # length of list is [1,1000]
        
        # constant space complexity would be O(n^2), linear time would be materializing values
        
        vals = []
        curr = head
        n = 0
        while curr:
            n += 1
            curr = curr.getNext()
        
        
        for idx in range(n - 1, -1, -1):
            node = self.getLLIdx(head, idx)
            node.printValue()
            
    
    def getLLIdx(self, curr, idx):
        cIdx = 0
        while cIdx < idx:
            cIdx += 1
            curr = curr.getNext()
        
        return(curr)

```