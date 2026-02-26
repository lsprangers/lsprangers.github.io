---
title: Time Map
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Semantics:
- Store multiple values for same key at different timestamps
- `get(key, t)` returns value with largest timestamp $\lte$ t
- Timestamps are strictly increasing per key
- Target: $O(log n)$ per get

```python
class TimeMap:
    def set(self, key: str, value: str, timestamp: int) -> None
    def get(self, key: str, timestamp: int) -> str
```

### Initial Thoughts, Questions
- Store everything in K:V dict as `key --> ordered data structure` where the ordering is based on timestamp
    - Allows for $O(\log n)$ binary search over the ordered data structure to find largest timestamp $\lte$ t
- Timestamps strictly increasing, so each `set` can simply append at the end

### Implementation
```python
class TimeMap:
    def __init__(self):
        self.lookups: Dict[str, list] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        # should allow for bisect_right in future
        self.lookups_ts[key].append(timestamp, val))

    def get(self, key: str, timestamp: int) -> str:
        # (100, 1), (101, 3), (104, 2), (108, 6), (120, 5)
        # t = 106 means we need 104. Need to find index st all elements to right
        #   are strictly greater than
        # bisect_right(106) returns 2
        # (100, 1), (101, 3), (104, 2), (106, 6), (108, 6), (120, 5)
        # bisect_right(106) returns 3
        # bisect_right(99) returns 0
        # bisect_right(200) returns 6 (arr index out of bounds if we return)
        resp_idx = bisect_right(self.lookups[key], timestamp, key=lambda elem: elem[0])
        if resp_idx >= len(self.lookups[key]):
            resp_idx = len(self.lookups[key]) - 1
        return(self.lookups[key][resp_idx])
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
