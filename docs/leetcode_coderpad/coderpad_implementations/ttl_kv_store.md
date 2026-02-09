---
title: Template
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Implement an in-memory TTL key–value store

You need to support setting keys with optional expiration, retrieving keys, and deleting keys

### Example
- `set`
    - Stores value under key
    - If ttl_ms is provided, the key should expire ttl_ms milliseconds after the set call time
    - If ttl_ms is None, the key never expires
    - Setting an existing key overwrites both value and TTL

- `get`
    - Returns the value if the key exists and is not expired at `now_ms`
    - Returns None if the key does not exist or is expired
    - Expired keys should behave as if they do not exist

- `delete`
    - Removes the key if present

No-op if missing.
```python
set(key: str, value: str, ttl_ms: Optional[int]) -> None
get(key: str, now_ms: int) -> Optional[str]
delete(key: str) -> None
```

### Constraints
- Assume:
    - Up to millions of keys
    - Up to millions of operations
- now_ms is monotonically non-decreasing across calls
- You are not allowed to scan all keys on every get
- Expired keys must not accumulate unboundedly in memory

Aim for:
- `get` in amortized O(1)
- `set` in amortized O(1)
- You must actively clean up expired keys (not just lazily on access)
- Single-threaded (no concurrency concerns)

### Initial Thoughts, Questions
- What do you mean by keys must not accumulate? Are you asking me to continuously run some loop to check keys expiration and handle time?
    - If so, how should I handle time ticks? Is built in `time.time` OK?
- “Expired keys must not accumulate unboundedly” means:
    - You cannot rely purely on lazy deletion during get
    - If many keys expire but are never accessed again, your structure must still reclaim them
    - leanup should be driven by normal operations (set / get), not by an external timer
- You decide when cleanup happens (e.g., during get, during set, or both), but:
- You may not scan all keys
- You must use `now_ms` as the current time reference

Idea:
- Storing these as a K:V store would be trivial - you use a `Dict[str, str]`
- Storing these with TTL with a lazy drain that runs during `set / get`
    - You store a priority queue of `(time_to_expire = inserted_ms + ttl_ms, key)`, and you pop off all keys that have `now_ms > time_to_expire`
    - At that point you check if key exists, and it's a typical `set / get`
    - This would be $O(\log n)$ during `set / get` in worst case
    - If there's nothing to drain, it's $O(1)$
- ***Resetting TTL for existing key means we need to store a current version***
    - This stops need to pop off until we find it if so
    - Deletes would simply delete

### Implementation
Notes:
- `get` is still amortized $O(\log n)$, because popping off min-heap
- `set` is $O(\log n)$ as we need to push onto min-heap

```python
from collections import defaultdict
import heapq

class ttlKV:
    def __init__(self):
        # min-heap (ttl, key, curr_version)
        #   order by ttl, if 2 keys the same then order by curr_version
        self.pq = []
        # key --> (val, curr_version)
        self.records: Dict[str, (str, int)] = {}
        self.last_now = 0
    
    def drain_expired(self, now_ms: int) -> None:
        # cannot drain from set or delete
        while self.pq and self.pq[0][0] < now_ms:
            ttl, key, curr_version = heapq.heappop(self.pq)
            # If key exists, and is the current version, delete else ignore
            # key may not exist from a delete, or there may be a newly updated version
            if key in self.records.keys():
                if self.records[key][1] == curr_version:
                    del self.records[key]
        
        return
            
    
    def set(self, key: str, value: str, ttl_ms: Optional[int]) -> None:
        # Just need to update versions, curr_val unnecessary, left in for brevity

        if key in self.records.keys():
            curr_val, curr_version = self.records[key]
        else:
           curr_version = 0 

        self.records[key] = (value, curr_version + 1)
        heapq.heappush(self.pq, (self.last_now + ttl_ms, key, curr_version + 1))

        return None
    
    def get(self, key: str, now_ms: int) -> Optional[str]:
        # now_ms is non-decreasing
        self.drain_expired(now_ms)
        self.last_now = now_ms
        if key in self.records.keys():
            return(self.records[key][0])
        
        
        return None
    
    def delete(self, key: str) -> None:
        if key in self.records.keys():
            del self.records[key]
        return None

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
