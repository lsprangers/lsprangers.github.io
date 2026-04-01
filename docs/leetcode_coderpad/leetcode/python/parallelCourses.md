---
title: parallelCourses
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# parallelCourses

```python
class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        if not relations or n < 2:
            return(True)
        
        # Build a DAG via Topo Sort
        
        is_dependency_for = defaultdict(list)
        dependency_count = {idx + 1: 0 for idx in range(n)}
        for relation in relations:
            
            # relation[0] is an active dependency for relation[1]
            is_dependency_for[relation[0]].append(relation[1])
            
            # count for O(1) in future
            dependency_count[relation[1]] += 1
        
        # is_depepdency_for = {1: [3], 2: [3]}
        # dependency_count = {1: 0, 2: 0, 3: 2}
        zero_deps = deque([])
        for node_idx, node_idx_count in dependency_count.items():
            if node_idx_count == 0:
                zero_deps.append(node_idx)
        
        
        classes_covered = 0
        resp = 0
        # [1, 2]
        while zero_deps:
            curr_zero_deps = len(zero_deps)
            resp += 1
            for _ in range(curr_zero_deps):
                # 1
                curr_class = zero_deps.popleft()
                
                # 3
                for dependent_class in is_dependency_for[curr_class]:
                    # {2: 0, 3: 1}
                    dependency_count[dependent_class] -= 1
                    if dependency_count[dependent_class] == 0:
                        zero_deps.append(dependent_class)
                
                classes_covered += 1
        
        
        return(resp if classes_covered == n else -1)
```