---
title: Dependency Graph Service
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building an in-memory dependency graph between services. A dependency means:
- `service` requires `depends_on` to be deployed first

So if A depends on B, then B must come before A in deployment order

### API
```python
class DependencyGraph:
    def add_dependency(self, service: str, depends_on: str) -> None
    def can_deploy(self, service: str) -> bool
    def deployment_order(self, service: str) -> List[str]
```

### Semantics
- `add_dependency(service, depends_on)`
    - Adds a directed edge: service -> depends_on.
    - You may assume inputs are valid strings. Duplicate edges may occur; handle gracefully.
- `can_deploy(service)`
    - Returns `False` if there is a cycle reachable from `service` (including via transitive dependencies). Otherwise returns `True`
    - If a dependency graph contains a cycle elsewhere, but it is not reachable from `service`, it does not matter for this query.
- `deployment_order(service)`
    - Returns a valid deployment order for service and all transitive dependencies
- Rules:
    - If `can_deploy(service)` is false, return an empty list
    - Order must place dependencies before dependents
    - Each service should appear at most once in the list
    - Include the `service` itself in the output

### Example
If we add:

```
A -> B
A -> C
B -> D
C -> D
```

Then `deployment_order(A)` could be `[D, B, C, A]` or `[D, C, B, A]`

If we add a cycle reachable from A:
```
D -> B (now B -> D -> B)
```

Then `can_deploy(A)` is false and `deployment_order(A)` returns `[]`

### Constraints
- Aim for efficient traversal
- Single-threaded
- You can assume graph fits in memory

### Initial Thoughts, Questions
- Initially this is a fairly straightforward topological sorting algorithm, and the constraints allow us to reply with any list that works, without the need for levels or groupings of anything
- The main item to focus on is implementing `can_deploy(service)`, which should be generic enough to cover any of the services provided
    - For each new call to it need to hold a `resp: List` variable for responses
    - Adjacency matrix `adj = defaultdict(list)` will store the `depends_on` for every node
        - This could be reused over calls to `can_deploy`, so `adj` can be initialized at the start if problem setup needs that
    - At the end if not all the nodes are included (cycle) we return `[]`
- This should run in time complexity $O(V + E)$ as it:
    - Needs to build out the adjacency matrix ($O(V + E)$)
    - Find all nodes with `in_degree = 0` ($O(V + E)$)
    - For each node with `in_degree = 0`, add it to the list and decrement it's neighbors $O(V + E)$
- Space complexity is also $O(V +  E)$ due to the adjacency matrix 


Meh - missed a few things:
- Reachability from service matters, no need to topo sort the entire graph, only the subgraph reachable from the queried `service` - this makes the overall implementation faster, and ***correctly matches the spec provided***
    - In a graph need to traverse to from `service` to find all reachable nodes, and then that's the result set you should run topo sort over
        - Can be done via DFS + color masking 
            - `0` univisited
            - `1` visiting (in stack)
            - `2` visited (done)
            - If you reach `1` you have a cycle, if you reach `2` stop that call
- Edge direction is `service -> depends_on`, topological sort wants dependencies first
### Implementation
```python
from typing import List
from collections import defaultdict

"""
A -> B
A -> C
B -> D
C -> D
dg = DependencyGraph()
dg.add_dependency(a, b)
dg.add_dependency(a, c)
dg.add_dependency(b, d)
dg.add_dependency(c, d)


service_to_dependent_on = {
    'a': [b, c],
    'b': [d],
    'c': [d],
    'd': []
}
service_to_what_requires_it = {
    'a': [],
    'b': [a],
    'c': [a],
    'd': [b, c]
}

in_degree is same as len(service_to_what_requires_it[service])
in_degree = {
    'a': 0
    'b': 1
    'c': 1
    'd': 2
}

Then `deployment_order(A)` could be `[D, B, C, A]` or `[D, C, B, A]`
If we add a cycle reachable from A:

D -> B (now B -> D -> B)
"""
class DependencyGraph:
    def __init__(self):
        self.deps = defaultdict(set)
        
    def add_dependency(self, service: str, depends_on: str) -> None:
        self.deps[service].add(depends_on)
        
        
    def can_deploy(self, service: str) -> bool:
        if self.deployment_order(service) == []:
            return(False)
        return(True)
    
    def deployment_order(self, service: str) -> List[str]:
        # 0 is default unvisited
        state = defaultdict(int)
        order = []
        has_cycle = False
        
        def dfs(service: str) -> None:
            nonlocal has_cycle
            if has_cycle:
                return
            
            if state[service] == 1:
                has_cycle = True
                return
            if state[service] == 2:
                return
            
            # {d: 2, b: 2, a: 2, c: 2}
            state[service] = 1

            # service_to_dependent_on = {
            #     'a': [b, c],
            #     'b': [d],
            #     'c': [d],
            #     'd': []
            # }            
            for service_curr_depends_on in self.deps[service]:
                dfs(service_curr_depends_on)
            
            state[service] = 2
            # [d, b, c, a]
            order.append(service)
            

        dfs(service)
        return(
            [] if has_cycle else order
        )
```

## Follow Up 1
Right now, `deployment_order(service)` returns an empty list if there’s a cycle

If the service is not deployable due to a cycle reachable from service, return one example cycle path so the caller can debug it

- Cycle must be reachable from the input service
- Returning any one cycle is fine
- Keep time complexity near O(V + E) for the reachable subgraph

```python
def deployment_order(self, service: str) -> tuple[list[str], list[str]]:
    """
    Returns (order, cycle).

    - If deployable: (valid_deployment_order, [])
    - If not deployable: ([], cycle_path)

    cycle_path should be a list of services that shows a directed cycle.
    Example: ["B", "D", "B"] or ["A", "C", "A"].
    """
```