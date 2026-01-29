from typing import List
from collections import defaultdict, deque

"""
A -> B
A -> C
B -> D
C -> D
```
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
        deployment_order = self.deployment_order(service)
        return(
            not deployment_order[1]
        )
    
    def deployment_order(self, service: str) -> tuple[list[str], list[str]]:
        """
        Returns (order, cycle).

        - If deployable: (valid_deployment_order, [])
        - If not deployable: ([], cycle_path)

        cycle_path should be a list of services that shows a directed cycle
        Example: ["B", "D", "B"] or ["A", "C", "A"].
        """
        has_cycle = False
        state = defaultdict(int)
        order = []
        cycle = []
        stack = []

        # Push on entry, pop on exit

        # On back-edge to a visiting node v, find the index of v in stack and slice stack[idx:] + [v]        
        
        # service_to_dependent_on = {
        #     'a': [b, c],
        #     'b': [d, f],
        #     'c': [d],
        #     'd': [e, a]
        #     'e': []
        #     'f': []
        # }
        # Then `deployment_order(A)` could be `[D, B, C, A]` or `[D, C, B, A]`
        # If we add a cycle reachable from A:

        # D -> A
        
        def dfs(service: str):
            nonlocal has_cycle
            nonlocal state
            nonlocal order
            nonlocal cycle
            nonlocal stack

            if has_cycle:
                return
            
            if state[service] == 1:
                idx = stack.index(service)
                cycle = stack[idx:] + [service]
                has_cycle = True
                return
            elif state[service] == 2:
                return
                            
            # [a, b, d, a]
            stack.append(service)
        
            state[service] = 1
            for depends_on in self.deps[service]:
                dfs(depends_on)

            state[service] = 2
            if has_cycle:
                return
                
            stack.pop()
            order.append(service)
        
        dfs(service)
        if has_cycle:
            return([], cycle)
        return(order, [])
    
from dependencyGraph import DependencyGraph
dg = DependencyGraph()
dg.add_dependency("a", "b")
dg.add_dependency("a", "c")
dg.add_dependency("b", "d")
dg.add_dependency("d", "b")
print(dg.deployment_order('a'))

from dependencyGraph import DependencyGraph
dg = DependencyGraph()
dg.add_dependency("a", "b")
dg.add_dependency("a", "c")
dg.add_dependency("b", "d")
dg.add_dependency("b", "f")
dg.add_dependency("c", "d")
dg.add_dependency("d", "e")
dg.add_dependency("d", "a")

