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