---
layout: technical
title: 4.. Linked Lists
category: Data Structures & Algorithms
difficulty: Advanced
description: Linked Lists
show_back_link: true
---

## Linked Lists

$O(n)$ access but $O(1)$ append and pop!

### Fast and Slow
This is usually the easiest way to get to the "middle" of a linked list in $O(n)$ time (since fast would have traversed the entire thing)

Pseudocode:
```python
resp = ListNode()
resp.next = head
fast = resp
slow = resp

while fast.next and fast.next.next:
    slow = slow.next
    fast = fast.next.next

# At this point slow.next is the middle
do_something_here(slow.next)

return(resp.next)
```

There's an example of [Deleting The Middle Node Of A Linked List](/docs/leetcode/python/deleteMiddleNodeOfLinkedList.md) that does just this!