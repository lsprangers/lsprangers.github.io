---
title: In Memory Feature Store
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You're building an online feature store for an ML inference service at Upstart. Multiple upstream pipelines publish feature updates, and inference services need to retrieve the latest valid features for a given entity

Your task is to implement a small in-memory feature store with following constraints
- Up to 1 million total operations
- Potentially thousands of versions per feature
- Reads are substantially more frequent than writes
- Optimize for efficient get() operations

### Requirements
Implement the below interfaces
1. `put()`
Stores a feature value with an associated timestamp
- Updates may arrive out of order
- Multiple versions of the same feature must be retained
- If the same (entity_id, feature_name, timestamp) is written multiple times, the most recent write wins
2. `get()`
Returns the feature value with the greatest timestamp less than or equal to as_of
- If no such version exists, return None
- Future versions must never be returned

```python
class FeatureStore:
    def put(
        self,
        entity_id: str,
        feature_name: str,
        value: float,
        timestamp: int
    ) -> None:
        pass

    def get(
        self,
        entity_id: str,
        feature_name: str,
        as_of: int
    ) -> float | None:
        pass
```

Example:
```python
store = FeatureStore()
store.put("user1", "income", 80000, 100)
store.put("user1", "income", 95000, 300)
store.put("user1", "income", 87000, 200)
assert store.get("user1", "income", 250) == 87000
assert store.get("user1", "income", 300) == 95000
assert store.get("user1", "income", 50) is None
store.put("user1", "income", 90000, 200)
assert store.get("user1", "income", 250) == 90000
```

### Initial Thoughts
"greatest timestamp less than or equal to as_of", "Reads are substantially more frequent than writes", "Optimize for efficient get() operations" - because lookups aren't necessarily $O(1)$ via a specific timestamp, we need to store sorted versions of the feature values + timestamp so that we can find the greatest next version in $O(\log n)$. We can still key a dictionary by feature name, but the actual storage structure after that would need to be a sorted object

What is entity ID? "It uniquely identifies the entity whose feature we're storing" - i.e. it needs to be apart of the key

For this I'd propose an in memory dictionary keyed by `(entity_id, feature_name)` whose actual underlying data structure is a Sorted Dictionary, which implements an ordered version with dictionary semantics:
- add is $O(\log n)$
- get, which is bisect left / right, is also $O(\log n)$
- discard / delete is $O(\log n)$ as well
- A new update to a specific timestamp with the same value would just overwrite it

### Implementation
```python
import sortedcollections
import collections
class FeatureStore:
    def __init__(self):
        self.kv = collections.defaultdict(sortedcollections.SortedDict)

    def put(
        self,
        entity_id: str,
        feature_name: str,
        value: float,
        timestamp: int
    ) -> None:
        self.kv[(entity_id, feature_name)][timestamp] = value

    def get(
        self,
        entity_id: str,
        feature_name: str,
        as_of: int
    ) -> float | None:
        key = (entity_id, feature_name)
        if key not in self.kv:
            return None

        versions = self.kv[key]
        idx = versions.bisect_right(as_of) - 1

        if idx < 0:
            return None

        timestamp, val = versions.peekitem(idx)
        return versions.peekitem(idx)[1]
```


## Follow Up - Productionization
Your feature store is now being integrated into a production inference service.

New requirement:

Multiple threads within the same Python process may call `put()` and `get()` concurrently.
The system must guarantee that:
1. Readers never observe an inconsistent intermediate state
2. Concurrent writes to the same (entity_id, feature_name, timestamp) don't corrupt the data structure
3. Reads should remain efficient, since inference traffic is read-heavy
4. You're still working with an in-memory implementation, not Redis or an external database

### Multithread Implementation
The high level approach would be to use threading locks that are picked up at the start of both put and get, this lock is the same across both because we want to ensure some level of isolation. Our get method has a few checks in it and so we can't rely on GIL level semantics to ensure everything is locked

This implementation almost succeeds without the need for threads:
- Although `put` is a single line, there are still multiple method calls involved. Specifically `SortedDict` maintains a dictionary and a sorted set of keys, so GIL ownership could change at any point in here
- A `get` starts with checking if a key exists
  - If that key does exist, it continues. At this point a put thread could take over and change the values, but that shouldn't matter as the existence check is atomic and we don't ever delete
    - If we did delete, then there's a chance this returns True, a def delete() command runs, and then our checks later fail
  - The real reason we need threads is for the versioning, specifically `idx = versions.bisect_right(as_of) - 1`, because if anything is put after this runs it can alter our index

The reason I mention wrapping around the start of both functions and releasing after is it makes the code much more maintainable and easier to reason through without actually impacting performance as the operations are all done in RAM and extremely fast

### Challenge
Each individual operation may be fast, but consider:
- 100 inference threads simultaneously calling `get()`
- One background thread periodically calling `put()`
- Each `get()` performing a binary search over thousands of versions
A global `threading.Lock` would serialize every read, even when those reads access completely unrelated entities
Suppose our workload is:
- 99% reads, 1% writes.
- 100 concurrent inference threads.
- 1 million distinct (entity_id, feature_name) pairs.
- Strict correctness requirements.
How would you modify your locking strategy to improve read throughput while maintaining correctness?
Readers must never observe partially updated or inconsistent data.
Readers accessing unrelated features should not unnecessarily block one another.

Interpretation:
This just means that each read would be "serialized" and have to wait for the output of one to start the next

To ensure we have the most minimal locking strategy that ensures partially updated or inconsistent data isn't seen, we need to use locks. It's plain and simple. However, we most likely need to change our underlying data structure / KV store based on the new requirement "Readers accessing unrelated features should not unnecessarily block one another."

The unit of isolation / thing we need to reason through is just the different features, and so one thread reading `(user1, income)` shouldn't block another thread reading `(user1, age)`. To do that we need to break out our KV store into a further nest of `{user: feature: versions: SortedDict}`, and then we can apply locks at the feature level

In our above code we would need a lock around the following portion, which currently does this on the entirety of the dictionary. This doesn't work with our current setup as the `versions = self.kv[key]` returns a link to an underlying portion, and even if we have a threading lock around `self.kv[key]` something could still write to it 
```
        versions = self.kv[key]
        idx = versions.bisect_right(as_of) - 1

        if idx < 0:
            return None

        timestamp, val = versions.peekitem(idx)
```


### Multithreading Implementation
```python
import sortedcollections
import collections
import threading
class ThreadSafeDict:
    def __init__(self):
        self.kv = {}
        self.lock = threading.Lock()

    def get_or_create(self, k):
        with self.lock:
            if k not in self.kv:
                self.kv[k] = threading.Lock()
            return self.kv[k]

class FeatureStore:
    def __init__(self):
        self.kv = collections.defaultdict(sortedcollections.SortedDict)
        self.locks = ThreadSafeDict()

    def put(
        self,
        entity_id: str,
        feature_name: str,
        value: float,
        timestamp: int
    ) -> None:
        key = (entity_id, feature_name)
        lock = self.locks.get_or_create(key)
        with lock:
            self.kv[key][timestamp] = value

    def get(
        self,
        entity_id: str,
        feature_name: str,
        as_of: int
    ) -> float | None:
        key = (entity_id, feature_name)

        if key not in self.kv:
            return None

        lock = self.locks.get_or_create(key)

        with lock:
            versions = self.kv[key]
            idx = versions.bisect_right(as_of) - 1
            if idx < 0:
                return None
            timestamp, val = versions.peekitem(idx)
            return val

store = FeatureStore()
store.put("user1", "income", 80000, 100)
store.put("user1", "income", 95000, 300)
store.put("user1", "income", 87000, 200)
assert store.get("user1", "income", 250) == 87000
assert store.get("user1", "income", 300) == 95000
assert store.get("user1", "income", 50) is None
store.put("user1", "income", 90000, 200)
assert store.get("user1", "income", 250) == 90000
```

### Yet Another Followup
I want a deterministic number of locks, not one per feature

### Multithreading Implementation
```python
import sortedcollections
import collections
import threading

class FeatureStore:
    def __init__(self, nLocks = 1024):
        self.kv = collections.defaultdict(sortedcollections.SortedDict)
        self.nLocks = nLocks
        self.lockPool = [threading.Lock() for _ in range(self.nLocks)]

    def getLock(
        self, 
        key: str,
    ) -> threading.Lock:
        # no need for thread safety, there are no updates this is just
        #   getting
        idx = hash(key) % self.nLocks
        return(self.lockPool[idx])

    def put(
        self,
        entity_id: str,
        feature_name: str,
        value: float,
        timestamp: int
    ) -> None:
        key = (entity_id, feature_name)
        lock = self.getLock(key)
        with lock:
            self.kv[key][timestamp] = value

    def get(
        self,
        entity_id: str,
        feature_name: str,
        as_of: int
    ) -> float | None:
        key = (entity_id, feature_name)

        lock = self.getLock(key)

        with lock:
            if key not in self.kv:
                return None            
            versions = self.kv[key]
            idx = versions.bisect_right(as_of) - 1
            if idx < 0:
                return None
            timestamp, val = versions.peekitem(idx)
            return val

store = FeatureStore()
store.put("user1", "income", 80000, 100)
store.put("user1", "income", 95000, 300)
store.put("user1", "income", 87000, 200)
assert store.get("user1", "income", 250) == 87000
assert store.get("user1", "income", 300) == 95000
assert store.get("user1", "income", 50) is None
store.put("user1", "income", 90000, 200)
assert store.get("user1", "income", 250) == 90000
```
