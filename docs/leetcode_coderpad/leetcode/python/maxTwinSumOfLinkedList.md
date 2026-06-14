---
title: maxTwinSumOfLinkedList
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maxTwinSumOfLinkedList

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        fast, slow = head, head

        # always even
        # 5 -> 4 -> 2 -> 1
        # slow = 2
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
        
        right = slow
        left = head

        prev = None
        while right:
            nx = right.next
            right.next = prev
            prev = right
            right = nx
        
        right = prev
        resp = 0
        while right:
            resp = max(
                resp,
                left.val + right.val
            )
            left = left.next
            right = right.next
        
        return(resp)
```