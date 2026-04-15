---
title: partitionList
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# partitionList

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:

        left = leftHead = ListNode(0)
        right = rightHead = ListNode(0)

        while head:
            if head.val < x:
                left.next = head
                left = left.next
            else:
                right.next = head
                right = right.next

            head = head.next
        
        right.next = None
        left.next = rightHead.next
        return(leftHead.next)
```