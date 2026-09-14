---
title: lruCache
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# lruCache

```python
class LLNode:
    def __init__(self, key, val):
        self.val = val
        self.key = key
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = LLNode(-1, -1)
        self.tail = LLNode(-1, -1)

        self.head.next = self.tail
        self.tail.prev = self.head

        self.size = 0

    def appendleft(self, newNode):
        curr = self.head.next

        self.head.next = newNode
        newNode.prev = self.head

        newNode.next = curr
        curr.prev = newNode


class LRUCache:

    def __init__(self, capacity: int):
        self.llist = LinkedList()
        self.map = {}
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1

        node = self.map[key]

        # Remove node
        node.prev.next = node.next
        node.next.prev = node.prev

        # Put at front
        node.next = None
        node.prev = None
        self.llist.appendleft(node)

        return node.val

    def put(self, key: int, value: int) -> None:

        # Existing key
        if key in self.map:
            node = self.map[key]

            node.val = value

            # Remove from current position
            node.prev.next = node.next
            node.next.prev = node.prev

            # Move to front
            node.next = None
            node.prev = None
            self.llist.appendleft(node)

            return

        # Evict if full
        if self.llist.size == self.capacity:
            lastNode = self.llist.tail.prev

            lastNode.prev.next = self.llist.tail
            self.llist.tail.prev = lastNode.prev

            lastNode.next = None
            lastNode.prev = None

            self.llist.size -= 1
            del self.map[lastNode.key]

        # Insert new node
        newNode = LLNode(key, value)
        self.llist.size += 1

        self.llist.appendleft(newNode)
        self.map[key] = newNode

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```