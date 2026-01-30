---
title: Consistent Hashing Service
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Implement a class that assigns keys to nodes using a consistent-hashing scheme

### API
```python
class ConsistentHashing:
    def add_node(self, node_id: str) -> None: ...
    def remove_node(self, node_id: str) -> None: ...
    def get_node(self, key: str) -> str | None: ...
```

### Requirements
- Keys and node identifiers must be mapped onto a hash space
- Each physical node must be represented by multiple virtual nodes (use 100 replicas)
- The system must track all virtual nodes and the node they belong to
- Adding a node inserts all of its replicas into the hash space
- Removing a node removes all of its replicas
- `get_node(key)` returns the node responsible for that key based on its hashed position on the ring
- If no nodes exist, return `None`


### Example
None atm

### Constraints
None atm

### Initial Thoughts, Questions
- For `n` nodes on the ring, it's split up into `n` sections
    - 1 node gets everything
    - 2 nodes splits it in half
    - 3 splits it into a peace sign kinda symbol
    - ...
- Each key is mapped to the last node on it's section
    - So if we use 1-100 as the circle identifiers, and there are 5 nodes 
        - 0:19
        - 20:39
        - 40:59
        - 60:79
        - 80:99
        - 100 == 0
    - Getting the closest node can be placing it onto ring can be done via:
        - `hash // (number_line // n_nodes) = index`
        - `index * (number_line // n_nodes) = ring start`
        - `(65 // (20)) * (20) = ring_start`
- Adding a new node in means splitting up one of the sections
    - Should this enforce all sections to become uniform again? Or just split up one of the sections?
    - Same question for removal, should we just bring all above instances down to the new node, or rebalance to be uniform?
- 32 bit space `[-2_147_483_648, 2_147_483_647]`
    - So ring is ~4M instead of 1-100, but the same rules apply
    - I can't wrap my head around how to assign a node given the negative space here, I can always just project onto `[0, 4M]` and subtract `2.1M`
    - Going to add `2^31` to each number, and sit in positive space
    - `hash_value = hash(x) & 0xffffffff`

Turns out everything I asked above is completely wrong about consistent hashing, it's not uniform, rebalances are horrible on system, etc...oops

### Implementation
- Storing node hashes in list
    - New node addition will be inserted
    - $O(n)$ insertion as all things have to shift up or down
    - `v_nodes = []`
- Each node is 100 nodes
    - So `add_node(node)` means there's actually 100 things to insert
    - `for i in range(99)`
        - `vhas_pos = hash(f"node_{i}") & 0xffffffff` 
        - `bisect_right(nodes, vhas_pos)` + insert there
            - Want to have all items less than or equal to `vhas_pos`
            - Can node hashes collide?
                - Yes, insert anyways
- Keep a dictionary of which virtual hashes apply to which overall node
    - `v_to_node[vhash] = node_id`
        - Could do `v_to_node[(vhash, unique_counter)] = node_id` to be absolutely sure no collisions, but collisions are rare
    - `node_to_v[node_id].append(vhash)`
- The above allows us to interact with both sorted virtual nodes, and then find their leader node `node_id`
- `remove_node(node_id)` means we need to loop over `node_to_v` and delete everything in there from `v_nodes` and clear our `node_to_v` and `v_to_node`
    - $O(n \times 100)$
    - Each `del v_node` from `v_nodes` is $O(n)$ movement
    - No reason to keep these in a priority queue or anything, we're not constantly looking for min or max, it's just we need a sorted structure that we can insert into random positions - list is still best case here as we don't want a linked list traversal $O(n)$
- `get_node(key)` would run `k_idx = hash(key) & 0xffffffff`
    - Need to find which `vhash` is greater than it
    - `bisect_left(v_nodes, k_idx)` will give us that index
        - All elements to the left are strictly less than
        - Therefore index returned is either equal to, or greater than
    - If that returned index is equal to `len(v_nodes)` we wrap around to 0 (that index wouldn't exist)
        - Equal to "None" return
        - Return `v_to_node` to get the actual `node_id` that corresponds to it

```python
class ConsistentHashing:
    def __init__(self):
        self.v_nodes = []
        self.v_to_node = defaultdict(str)
        self.node_to_v = defaultdict(list)
        self.replica_factor = 100

    def add_node(self, node_id: str) -> None:
        for i in range(self.replica_factor):
            vhas_pos = hash(f"{node_id}_{i}") & 0xffffffff
            vhas_item = (vhas_pos, node_id, i)

            # want to get the index where everything left of it is less than or equal to
            # i.e., everything to right is strictly larger
            #   [1, 2, 4, 5] 
            #       bisect_right(3) returns 2 - we want to insert there
            #       bisect_right(2) returns 2 - all ltequal to
            vhas_idx = bisect_right(self.v_nodes, vhas_item)
            self.v_nodes.insert(vhas_idx, vhas_item)
            
            # map a position hash back to node, if vhas found in v_nodes, we wwant to know
            #   which node_id it's for
            # could do v_to_node[(vhash, unique_counter)] = node_id later on to avoid coll's
            self.v_to_node[vhas_item] = node_id
            # doesn't need ordering, just need reference
            self.node_to_v[node_id].append(vhas_item)


    def remove_node(self, node_id: str) -> None:
        if node_id not in self.node_to_v.keys():
            return(None)


        vhas_pos_list = self.node_to_v[node_id]
        del self.node_to_v[node_id]
        for v_node_item in vhas_pos_list:
            # if there are duplicates, bisect_left will return first one
            #   we are assuming no hash coll's...
            self.v_nodes.pop(bisect_left(self.v_nodes, v_node_item))
            del self.v_to_node[v_node_item]


    def get_node(self, key: str) -> str | None:
        if not self.v_nodes:
            return(None)
        
        k_idx = hash(key) & 0xffffffff
        # bisect_left means all elements to left are strictly less than
        #   so this index is greater than or equal to
        next_greatest_vhas = bisect_left(self.v_nodes, (k_idx, -1))

        # loop to 0 if at the end
        next_greatest_vhas = next_greatest_vhas % len(self.v_nodes)
        
        return(
            self.v_to_node[self.v_nodes[next_greatest_vhas]]
        )
```