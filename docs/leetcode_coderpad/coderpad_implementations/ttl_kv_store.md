---
title: TTL KV Store
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



## Second Attempt
Implement this:
```python
class TTLKVStore:
    def set(self, key: str, value: str, ttl_ms: int, now_ms: int) -> None:
        ...
    
    def get(self, key: str, now_ms: int) -> str | None:
        ...
    
    def delete(self, key: str) -> None:
        ...
```

### Requirements
- `set(key, value, ttl_ms, now_ms)` stores the value with expiration at `now_ms + ttl_ms`
- `get(key, now_ms)` returns `None` if the key does not exist or is expired
- `delete(key)` removes the key if present
- assume:
    - many keys
    - many expired entries
    - get should be efficient
    - expired keys do not need to be removed exactly at expiration time, but must never be returned after expiration
- discuss:
    - data structures
    - time complexity
    - how you avoid stale expiration entries causing bugs
    - what changes if this becomes thread-safe
    - what changes if this must work across multiple machines

### Implement
- Can the expiration be lazily evaluated, or should there be some background process removing things?
    - On lazy evaluation we would just need to "clear" the old data during `get` requests before actually looking into the keys
- Storing this data would need to be done utilizing a priority queue for timestamps and keys so that clearing out up to a specific timestamp means we just need to pop off of the priority queue up to `now_ms`
    - Inserting into the priority queue is $O(log k)$ where $k$ is the number of keys
    - Deleting / popping off is also $O(log k)$ as we need to rebalance the priority queue underlying tree
    - Given there might be multiple live values for a key, we also need to store versions of each K:V pair so that we don't delete an older K:V that's still in the PQ
    - The actual key stored in our K:V store would be `key: [value, expiry_ts, version]`, and we would also need to place `[(expiry_ts, key, version)]` into the priority queue
        - Use expiration time `(now_ms + ttl_ms, key, version)`
- Clearing the data on get should ensure we have no expired keys in the K:V store, which means we can return `None` during `get`, and then `set` just needs to increment the version and add the entry to the priority queue
    - `set` is $O(log k)$
    - `get` is $O(log k)$ for each pop less than `now_ms`
    - `delete` can be $O(1)$ if we just directly remove it from the K:V store, then during the clearing out in `get` we can ignore the key if it doesn't exist

```python
import heapq
class TTLKVStore:
    def __init__(self):
        self.kv_store = {}
        self.pq = []
        self.last_seen_version = {}

    def _evict_expired(self, now_ms) -> None:
        # storing [expiry_ts, key, version]
        while self.pq and self.pq[0][0] <= now_ms:
            old_entry_expiry_ts, old_entry_key, old_entry_version = heapq.heappop(self.pq)
            # storing [value, expiry_ts, version] in KV
            # Delete entry only if it's the key exists and it's the version specified in the heapq expired entry
            if old_entry_key in self.kv_store and self.kv_store[old_entry_key][2] == old_entry_version:
                del self.kv_store[old_entry_key]
        
        return


    def set(self, key: str, value: str, ttl_ms: int, now_ms: int) -> None:
        # should check if later version exists, but assumption stated it's monotonically increasing
        # there may be an edge case where we store a version in the KV store that's deleted, and get would need to get a lower
        #   version
        # This should still mean we get a latest version based on last, and to avoid any edge cases we'll store another dict for now
        if key in self.last_seen_version:
            new_version = self.last_seen_version[key] + 1
            self.last_seen_version[key] = new_version
        else:
            self.last_seen_version[key] = 0
            new_version = 0

        expiry_ts = now_ms + ttl_ms

        # Just return and don't set anything at all
        if expiry_ts <= now_ms:
            return
        
        # need to sort on expiry_ts, [expiry_ts, key, version]
        pq_entry = [expiry_ts, key, new_version]
        heapq.heappush(self.pq, pq_entry)

        self.kv_store[key] = [value, expiry_ts, new_version]
        return
    
    def get(self, key: str, now_ms: int) -> str | None:
        self._evict_expired(now_ms)
        
        if key in self.kv_store:
            # [value, expiry_ts, version]
            return(self.kv_store[key][0])
        else:
            return(None)

    def delete(self, key: str) -> None:
        if key in self.kv_store:
            del self.kv_store[key]


if __name__ == "__main__":
    test_class = TTLKVStore()
    test_class.set('a', '1', 10, 0)
    test_class.set('b', '2', 5, 1)
    # simple
    assert test_class.get('b', 2) == '2'
    test_class.delete('a')
    assert test_class.get('a', 3) == None

    # simulate an odd case of ttl
    test_class.set('c', '3', 10, 5) # expire at 15
    test_class.set('c', '4', 1, 7) # expire at 8

    assert test_class.get('c', 8) == None
    test_class.set('d', '5', 5, 9) #expire at 14
    test_class.set('d', '6', 5, 10) #expire at 15
    assert test_class.get('d', 12) == '6'
    assert test_class.get('d', 14) == '6'

"""
Time:
- set is O(log k) from heapq push
- get is O(log m) where m is the number of expired heap entries removed in that call
    - _evict_expired is amortized O(log k), it only touches each key at most once, and that operation is O(log k)
    - Each actual entry is pushed once and popped once
- delete is O(1)

Space:
- Storing each key in KV and PQ - O(n)

Thread safety:
- This is currently thread safe in one process in Python. If we create multiple threads it's still thread safe due to GIL lock in Python
    - In another language we would need some mutexes on pq and kv_store during the actual entry updates, deletes, and heapq push / pop

Distributed Machine:
- Pull out both the priority queue and KV store into separate distributed stores, and the set/get/delete logic would need to get a distributed mutex to make the
    state change in those distributed databases to ensure consistency
"""
```


#### Follow Up
`def count_unexpired(self, now_ms: int) -> int:`
It should return the number of currently unexpired keys

Constraints:
- many expired entries may still be sitting in the heap
- do not scan all keys on every call unless you choose that deliberately and justify it