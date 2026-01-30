---
title: Versioned File Store
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building an in-memory file store that supports writing versions and querying historical state


### API
```python
class FileStore:
    def put(self, path: str, contents: str, timestamp: int) -> None
    def get(self, path: str, timestamp: int) -> str | None
    def delete(self, path: str, timestamp: int) -> None
```

### Semantics
- `put(path, contents, t)` writes a new version at time `t`
    - If content exists should it be overwritten?
    - 
- `delete(path, t)` marks the file deleted at time `t`
- `get(path, t)` returns the file contents at the latest version with timestamp $\lt$ `t`, unless the latest such version is a deletion, in which case return `None`
- Timestamps for the same path are strictly increasing (you can assume no out-of-order writes for a given path)
- If the path has never been written before time `t`, return `None`

#### Complexity Requirements
- `get` should be $O(log n)$ per path
- `put` / `delete` should be amortized $O(1)$

### Example

```
put("/a", "hello", 1)
put("/a", "world", 3)

get("/a", 2) -> "hello"
get("/a", 3) -> "world"
get("/a", 0) -> None

delete("/a", 4)
get("/a", 5) -> None
```

### Constraints
- get must be $O(log n)$ per file
- Store only in memory


### Initial Thoughts, Questions
- Should put fail if a version already exists?
- If `put` and `delete` are amortized $O(1)$ then they should be stored in dict of some sort 
    - If size grows too large it expands, i.e. amortized
- Thought process would be dictionary of keys, `put` and `get` are direct inserts
    - Amortized as underlying list has to grow larger if more data comes in
- Ordered dicts don't keep keys sorted, just order of insertion
    - The bsearch part would be over the search space of time
    - Need to keep min and max timestamps 
    - For a `get`, if it's within min and max then bsearch over that and look for last index that is relevant (bisect_left)
        - Bisect right returns `i` such that all `a[:i]` are less than or equal to it
        - `a = [1, 1, 3]`, `bisect_right(a, 2)` returns 2, and `bisect_right(a, 1)` also returns 2 as that's the index where everything left of it is less than equal
        - `bisect_right(a, target) - 1` gives us the last index such that lte

### Implementation
- Storage will be, for each `path`:
    - Store `store = defaultdict(list)`
    - Where the list inside of it will be `(timestamp, value)` as `bisect_right` works off first tuple entry
    - Since all entries strictly increasing, just appending works fine
- `get` will utilize `bisect_right - 1` to get latest index
- `put` will just append new `(timestamp, value)`
- `delete` just needs to be a tombstone record - it doesn't delete a specific version, it just deletes the entire file
    - Using tombstone allows for restores in future

```python
from collections import defaultdict
import bisect

class FileStore:
    def __init__(self):
        # {path --> [(timestamp, value), ..., (timestamp, None)]}
        #   deletes will be None for easy checking
        # path -> { "ts": [...], "vals": [...] }
        self.store = defaultdict(lambda: {"ts": [], "vals": []})

    def put(self, path: str, contents: str, timestamp: int) -> None:
        self.store[path]["ts"].append(timestamp)
        self.store[path]["vals"].append(contents)

    def get(self, path: str, timestamp: int) -> str | None:
        # avoids defaultdict creating an entry
        versions = self.store.get(path)
        if not versions:
            return None
        
        # Failed interview because of this shit - tuple comparison
        #   had to take out and create lambda in defaultdict b/c None < "" not true and throws 
        #   TypeError
        # last_valid_timestamp = bisect.bisect_right(self.store[path], (timestamp, "")) - 1
        
        ts_list = entry["ts"]
        last_valid_timestamp = bisect.bisect_right(ts_list, timestamp) - 1

        # earlier than any entry - just a safecheck
        if last_valid_timestamp < 0:
            return(None)
        
        return(versions["vals"][last_valid_timestamp])

    def delete(self, path: str, timestamp: int) -> None:
        # Just tombstone it
        self.store[path]["ts"].append(timestamp)
        self.store[path]["vals"].append(None)
```