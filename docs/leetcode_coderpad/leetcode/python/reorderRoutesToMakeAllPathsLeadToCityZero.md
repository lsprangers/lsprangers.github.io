---
title: reorderRoutesToMakeAllPathsLeadToCityZero
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# reorderRoutesToMakeAllPathsLeadToCityZero

```python
class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        # define child node as something that has 0 neighbors outside of seen set
        self.adj_list = defaultdict(list)
        self.seen = set()
        self.roads = set()
        self.resp = 0

        for x, y in connections:
            self.adj_list[x].append(y)
            self.adj_list[y].append(x)
            self.roads.add((x, y))
        
        self.dfs(0, -1)
        return(self.resp)
        
    
    def dfs(self, curr_node, parent_node):
        for neighbor in self.adj_list[curr_node]:
            if neighbor not in self.seen:
                self.seen.add(neighbor)
                self.dfs(neighbor, curr_node)
        
        if curr_node != 0 and (curr_node, parent_node) not in self.roads:
            self.resp += 1
```

```python
class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        self.canReachZero = set([0])
        self.twoWayGraph = defaultdict(set)
        self.oneWayGraph = defaultdict(set)
        
        # O(E)
        for _from, _to in connections:
            if _to == 0 or _to in self.canReachZero:
                self.canReachZero.add(_from)
                
            self.oneWayGraph[_from].add(_to)            
            self.twoWayGraph[_from].add(_to)            
            self.twoWayGraph[_to].add(_from)
        
        stack = [0]
        seen = set()
        resp = 0
        while stack:
            currNode = stack.pop()
            if currNode in self.canReachZero:
                canReach = True
            else:
                canReach = False
            
            for neighbor in self.oneWayGraph[currNode]:
                if neighbor in self.canReachZero:
                    canReach = True

            for neighbor in self.twoWayGraph[currNode]:
                if neighbor not in seen:
                    stack.append(neighbor)
                    seen.add(neighbor)
            
            self.canReachZero.add(currNode)
            if not canReach:
                resp += 1
                
        
        return(resp)
```