---
title: LRU Cache
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Implement an LRU (Least Recently Used) cache
- If capacity is reached, evict the least recently used key
- `get` and `put` must be $O(1)$ average time

### Example
```python
class LRUCache:
    def __init__(self, capacity: int):
    def get(self, key: int) -> int
    def put(self, key: int, value: int) -> None
```

### Constraints
- capacity $\gte$ 0
- keys are integers
- values are integers

### Initial Thoughts, Questions
- Doubly linked list can host the `right` (latest) and `left` (oldest) values with `next` and `prev` for $O(1)$ popping, updated, etc
    - We cannot use a python deque, as random access via K:V reference to a node would not be $O(1)$ as it fully traverses the linked list to an index
- K:V store of key and reference to a node (pointer), so that access to middle of linked list is $O(1)$, and then can remove that element in $O(1)$ time with `elem.prev.next = elem.next` semantics

### Implementation
```python
class DoublyLinkedListNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.lookup: Dict[int, DoublyLinkedListNode] = {}
        self.right: DoublyLinkedListNode = DoublyLinkedListNode()
        self.left: DoubleLinkedListNode = DoubleLinkedListNode()

        # deque structure
        #   left (newest) --> --> ... right (oldest)
        self.right.prev = self.left
        self.left.next = self.right

    def append_left(self, node: DoublyLinkedListNode):
        # assumes node has no leaky references elsewhere
        curr_left = self.left.next
        self.left.next = node
        node.prev = self.left
        node.next = curr_left
        curr_left.prev = node

    def append_right(self, node: DoublyLinkedListNode):
        # assumes node has no leaky references elsewhere
        curr_right = self.right.prev
        self.right.prev = node
        node.next = self.right
        node.prev = curr_right
        curr_right.next = node
    
    def delete_node(self, node: DoublyLinkedListNode) -> DoublyLinkedListNode:
        # Will update self.right and self.left inline if they're being deleted
        node_prev = node.prev
        node_next = node.next
        if node == self.right:
            # node_next = None
            self.right = node_prev
            self.right.next = node_next
        elif node == self.left:
            # node_prev is None
            self.left = node_next
            self.left.prev = node_prev
        else:
            # Update both
            node_prev.next = node_next
            node_next.prev = node_prev
        
        # Wipe curr node
        node.prev = None
        node.next = None
        return(node)


    def get(self, key: int) -> int:
        # Get response and move node to newest, which means it was 
        #   the most recently used
        if key not in self.lookups.keys():
            return ValueError(f"Missing {key}")
        node = self.lookups[key]
        node = self.delete_node(node)
        self.append_left(node)
        return(node.val)

    def put(self, key: int, value: int) -> None:
        if len(self.lookups.keys()) >= capacity:
            curr = self.right
            self.delete_node(self.right)
            del self.lookups[curr]
        
        new_node = DoublyLinkedListNode(val)
        self.append_left(new_node)
        self.lookups[key] = new_node
        return

```

## Systems Design


### High Level requirements


#### API Surface

#### Clarifying Questions
Questions around implementations, strict vs approximate, and anything that would kill any choices made in future

#### System Constraints
Summarize system constraints in your own words
- QPS 
- latency SLO    
- consistency requirements
- failure tolerance

#### Identify Core Challenges
What makes this problem hard in distributed manner (MOST IMPORTANT PART)
- Distributed correctness (no double allow)
- Routing / management
- Data structure
- Scale + latency
- Failure behavior
- single-writer vs linearizable store
- availability vs consistency
- data plane vs control plane

#### Starter Architecture
Distributed compatible, but high level components and algorithms, focus on partitioning and scaling, not frontend or anything. Some data structure information is OK, specifically ones that relate to the core problem.

Components + Flow + network, partition, and some data structures

#### Real Architecture
Now you make in depth choices on literally everything, and draw the entire thing out

#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture
