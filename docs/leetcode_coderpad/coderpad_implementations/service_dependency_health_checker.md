---
title: Service Dependency Health Checker
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You are given a collection of microservices and their dependencies

When a service depends on another, it cannot operate unless all of its dependencies are currently healthy

### API
Must build a class for following API:

```python
class ServiceHealth()

    def add_service(service: str) -> None
    def add_dependency(service: str, depends_on: str) -> None
    def set_unhealthy(service: str) -> None
    def set_healthy(service: str) -> None
    def is_operational(service: str) -> bool
```

- `add_service(service: str) -> None` registers a new service with no dependencies initially
- `add_dependency(service: str, depends_on: str) -> None` declares that service requires `depends_on`
    - Dependencies may form arbitrary directed graphs
    - ***Cycles are allowed in the input***, but cycles mean no service in that cycle can ever be healthy
- `set_unhealthy(service: str) -> None` sets a services `health` flag 
    - A service is considered healthy only if:
        - It's own `health_flg = 1`
        - All services it depends on are operational
- `set_healthy(service: str) -> None` sets a services `health` flag
    - A service is considered healthy only if:
        - It's own `health_flg = 1`
        - All services it depends on are operational
- `is_operational(service: str) -> bool` returns whether the service is operational or not

### Example
```
A depends on B
B depends on C

set_healthy(A), set_healthy(B), set_healthy(C)
is_operational(A) → True

set_unhealthy(C)
is_operational(A) → False
is_operational(B) → False

Cycle: X → Y → Z → X
Even if all are set healthy:
is_operational(X) → False
is_operational(Y) → False
is_operational(Z) → False
```

### Constraints
- Up to ~10,000 services
- Dependency graph may contain cycles
- `is_operational(service)` must run efficiently
- Health changes (`set_healthy`/`set_unhealthy`) will be frequent
- No external libraries beyond standard Python

### Initial Thoughts, Questions

### Data Structures
- Each `service` is a data structure with certain attributes itself
    - No need to go over the top here, just need a dictionary of `service_dict: service --> Dict[str, X]` with attributes around health and other items
    - Any call to `add_service` sets this up
- Service list can be stored as edges at first
    - Any single call to `add_dependency` would re-calculate ALL of the health attributes around health
        - In a future update, caching and only traversing the affected percentage could be done with color masking and topological sort at the same time
        - Should I implement this in initial try, or keep it simple?
    - There should be a direct service health flag `in_cycle` stored in `service_dict` that is updates to `1` if there's a cycle, and then this can be directly referenced in call to `is_operational` - if it's 1 then it's in a cycle and can just return
        - Same thing store `is_unhealthy` flag that's also checked at this API call
        - `set_healthy` and `set_unhealthy` would update the `service_dict[service][is_unhealthy]` flag

Caching and traversal of "only affected parts" is difficult, if there are 2 disconnected components that are then joined by an `add_dependency` call, we'd potentially miss out on them unless we stored some sort of component ID. This is usually done via `UnionFind` data structure, but I've only implemented that on undirected graphs. There's a way to do it I can try and walk through, but before implementing going to check in

### Initial Implementation
```python
from typing import Dict
from collections import defaultdict

class ServiceHealth():
    def __init__(self):
        self.service_dict: Dict[str, Dict] = {}
        # The services that each key needs to function
        self.service_to_depends_on = defaultdict(list)
        
        # Each service that's needed by key to function
        self.service_to_depended_by = defaultdict(list)
    
    def add_service(self, service: str) -> None:
        if service in self.service_dict.keys():
            raise ValueError(f"{service} already in dictionary")
                
        self.service_dict[service] = {
            "is_operational": False,
            "is_healthy": True,
        }
        return
    
    def add_dependency(self, service: str, depends_on: str) -> None:
        self.service_to_depends_on[service].append(depends_on)
        self.service_to_depended_by[depends_on].append(service)
        return None
    
    def set_unhealthy(self, service: str) -> None:
        # Sets the flg per service, doesn't compute the flag for all other dependent services

        if service not in self.service_dict.keys():
            raise ValueError(f"{service} not currently in dictionary")
        
        self.service_dict[service]["is_healthy"] = False
        return None

    def set_healthy(self, service: str) -> None:
        # Sets the flg per service, doesn't compute the flag for all other dependent services

        if service not in self.service_dict.keys():
            raise ValueError(f"{service} not currently in dictionary")
        
        self.service_dict[service]["is_healthy"] = True
        return None

    def is_operational(self, service: str) -> bool:
        if service not in self.service_dict.keys():
            raise ValueError(f"{service} not currently in dictionary")
        if self.service_dict[service]["is_healthy"] == False:
            return(False)
        
        has_cycle = False
        state = defaultdict(int)
        
        
        def dfs(service: str):
            nonlocal has_cycle
            nonlocal state
            count = 0
            
            if has_cycle:
                return(0)
            
            # If this doesn't exist, raise a ValueError
            if service not in self.service_dict.keys(): # or self.service_dict[service]["is_healthy"] == False:
                raise ValueError(f"{service} not currently in dictionary")
            
            # We will set cycle here
            if state[service] == 1:
                has_cycle = True
                return(0)
            # if this service has already been seen, we should still cover it
            # elif state[service] == 2:
            #     return(0)
            else:
                state[service] = 1
            
            
            # service_to_depends_on = {
            #     'a': [b, c],
            #     'b': [d, f],
            #     'c': [d],
            #     'd': [e]
            #     'e': []
            #     'f': []
            # }

            # D -> A
            
            # Because we're using `service_to_depends_on`, we're only touching the relevant
            #   subgraph, and has_cycle wouldn't be set on a cycle in a separate component
            for upstream_service in self.service_to_depends_on[service]:
                count += dfs(upstream_service)
            
            state[service] = 2
            # if all our dependent services are covered, then we're also covered
            return(
                1 if count == len(self.service_to_depends_on[service]) else 0
            )
            
            
        return(
            dfs(service) and not has_cycle
        )
```

### Follow Up Implementations
- In the scenario of an already seen service `state[service] == 2`, is there a way to memoize / cache this information for future?
    - Also, are there any other areas of storing memoized results / cached results?

Tweak `dfs()`

```python
        has_cycle = False
        state = defaultdict(int)
        cache = defaultdict(int)
        
        
        def dfs(service: str):
            nonlocal has_cycle
            nonlocal state
            nonlocal cache

            count = 0
            
            if has_cycle:
                return(0)
            
            # If this doesn't exist, raise a ValueError
            if service not in self.service_dict.keys(): # or self.service_dict[service]["is_healthy"] == False:
                raise ValueError(f"{service} not currently in dictionary")
            
            # We will set cycle here
            if state[service] == 1:
                has_cycle = True
                return(0)
            # if this service has already been seen, we should still cover it
            elif state[service] == 2:
                return(cache[service])
            else:
                state[service] = 1
            
            
            # service_to_depends_on = {
            #     'a': [b, c],
            #     'b': [d, f],
            #     'c': [d],
            #     'd': [e]
            #     'e': []
            #     'f': []
            # }

            # D -> A
            
            # Because we're using `service_to_depends_on`, we're only touching the relevant
            #   subgraph, and has_cycle wouldn't be set on a cycle in a separate component
            for upstream_service in self.service_to_depends_on[service]:
                count += dfs(upstream_service)
            
            state[service] = 2
            cache[service] = (1 if count == len(self.service_to_depends_on[service]) else 0)
            # if all our dependent services are covered, then we're also covered
            return(
                1 if count == len(self.service_to_depends_on[service]) else 0
            )
```


Further good follow ups:
- Talk about cache invalidation in `set_healthy` and `set_unhealthy`
- Talk about edge cases that don't fail now, but would later 
    - i.e returning `len(children) == count` may not always be ideal
- Mention system level insights
    - Health mutations are more frequent than dependency mutations, so caching operational results and invalidating on health checks is effective for system load
    - Multi-query batching
    - SCC caching (this one is a bit out there), talking about cycles with strongly connected components and utilizing Tarjan algorithm to identify strongly connected components and their supernodes, which can help on caching
        - similar to UnionFind but works on directed graphs

### What To Focus On
- Invariant returns using booleans instead of len count semantics
- Showing how data structures (black/white/gray) correspond to spec details + requirements
- Over optimize in initial pass. Focus on solving exactly as spec asks, and you can mention for future but leave out of initial implementation
    - UnionFind + premature caching implementation discussion