---
title: Template
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You manage a company hierarchy

Employees form a tree

### API
```python
class OrgChart:
    def add_employee(self, manager: str, employee: str) -> None
    def get_reports(self, manager: str) -> List[str]
    def lowest_common_manager(self, a: str, b: str) -> str
```

### Semantics
- CEO has manager `None` boss
- Tree structure (no cycles)
- `get_reports` returns all direct + indirect reports
- lowest_common_manager is the first common manager in line to 2 employees
    - Same as lowest common ancestor


### Example


### Constraints


### Initial Thoughts, Questions


### Implementation
```python
```