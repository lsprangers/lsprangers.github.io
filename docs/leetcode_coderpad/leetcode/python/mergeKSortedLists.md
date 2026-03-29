---
title: mergeKSortedLists
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# mergeKSortedLists

This is $O(N K)$, but was able to do it on first try
```python
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return(None)

        resp = ListNode()

        ptrs = [l for l in lists if l]

        curr = resp
        while any(ptrs):
            curr_min_ptr = ListNode(float("inf"))
            # using curr_min_ptr.next doesn't update p?
            chg_idx = -1
            for idx, p in enumerate(ptrs):
                if p and p.val < curr_min_ptr.val:
                    curr_min_ptr = p
                    chg_idx = idx

            curr.next = ListNode(curr_min_ptr.val)
            curr = curr.next
            curr_min_ptr = curr_min_ptr.next
            ptrs[chg_idx] = curr_min_ptr
        
        return(resp.next)
```


Defining the new `HeapNode` class and just looping over the lists and creating them is where I was caught up. Need the `<` operator defined to have heap implemented

```python
class HeapNode:
    def __init__(self, node):
        self.node = node

    def __lt__(self, other):
        # Define comparison based on ListNode's value
        return self.node.val < other.node.val


class Solution:
    def mergeKLists(
        self, lists: List[Optional[ListNode]]
    ) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        heap = []

        # Initialize the heap
        for l in lists:
            if l:
                heapq.heappush(heap, HeapNode(l))

        # Extract the minimum node and add its next node to the heap
        while heap:
            heap_node = heapq.heappop(heap)
            node = heap_node.node
            current.next = node
            current = current.next
            if node.next:
                heapq.heappush(heap, HeapNode(node.next))

        return dummy.next
```