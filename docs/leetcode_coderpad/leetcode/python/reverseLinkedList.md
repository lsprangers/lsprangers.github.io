---
title: reverseLinkedList
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reverseLinkedList

```python

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            # 2
            # helper = 3
            helper = curr.next
            # 2.next = 1
            curr.next = prev
            # prev = 2
            prev = curr
            # curr = 3
            curr = helper
            
        return(prev)
```