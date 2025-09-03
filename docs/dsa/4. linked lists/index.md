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

### Reversal
Reversing a Linked List involves using temporary node holders and then just swapping prev and next values along the way

```python
# create an eventual response, which will point to resp.next (which would be tail!)
resp = ListNode(0, head)
curr = head
prev = resp

# 1 --> 2 --> 3
# curr = 1
# prev = resp() --> 1
while curr:
    # 2
    next_node = curr.next
    
    # resp <-- 1 
    # 2 --> 3
    curr.next = prev

    # prev = 1
    # curr = 2
    prev = curr
    curr = next_node

# This would return head of new, reversed, LinkedList
return(prev)

# This would return tail 
return(resp.next)
```