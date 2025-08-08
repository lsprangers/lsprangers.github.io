---
title: deleteMiddleNodeOfLinkedList
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# deleteMiddleNodeOfLinkedList
If it's uneven, i.e. 7 nodes:
$resp \rarr 1 \rarr 3 \rarr 4 \rarr 7 \rarr 6 \rarr 0 \rarr 5$
```
slow = resp, 1, 3, 4
fast = resp, 3, 7, 0
```
At this point fast.next is there, but fast.next.next is not and it'd end

Then, if it's even, i.e. 6 nodes:
$resp \rarr 1 \rarr 3 \rarr 4 \rarr 7 \rarr 6 \rarr 0$
```
slow = resp, 1, 3, 4
fast = resp, 3, 7, 0
```
At this point fast.next is not there, and therefore fast.next.next is not either, and both end at 4

Deleting `slow.next` from the list and returning `resp.next` will give us the answer!


```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) \rarr Optional[ListNode]:
        # O(n) to go get size and delete math.ceil(size / 2) after traversal
        # O(n) fast and slow
        resp = ListNode()
        resp.next = head

        slow = resp
        fast = resp
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        
        slow.next = slow.next.next
        return(resp.next)

```