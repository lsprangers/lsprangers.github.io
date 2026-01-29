---
title: Versioned File Store
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building an in-memory file store with version history


### API
```python
class FileStore:
    def put(self, path: str, contents: str, timestamp: int) -> None
    def get(self, path: str, timestamp: int) -> str | None
    def delete(self, path: str, timestamp: int) -> None
```

### Semantics
- Multiple versions per file
- `get(path, t)` returns the contents at the latest `timestamp ≤ t`
- `delete` marks file deleted at that timestamp
- Timestamps for a given path are strictly increasing

### Example

```
put("/a", "hello", 1)
put("/a", "world", 3)

get("/a", 2) -> "hello"
get("/a", 3) -> "world"

delete("/a", 4)
get("/a", 5) -> None
```

### Constraints
- get must be $O(log n)$ per file
- Store only in memory


### Initial Thoughts, Questions


### Implementation
```python
```