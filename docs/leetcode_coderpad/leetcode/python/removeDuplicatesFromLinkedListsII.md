---
title: removeDuplicatesFromLinkedListsII
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# removeDuplicatesFromLinkedListsII

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        resp = ListNode()
        resp.next = None
        prev = resp

        while head:
            foundDupe = False
            while head and head.next and head.val == head.next.val:
                foundDupe = True
                head = head.next
            
            # Set to None until we find another non-dupe later on
            if not foundDupe:
                prev.next = head
                prev = head
            else:
                prev.next = None

            head = head.next
        
        return(resp.next)
```