---
title: numProvinces
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numProvinces

I didn't remember how to do [unionFind](/docs/dsa/implementations/unionfind.md) here - but that'd be the best way to do it

```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        seen = set()
        num_provinces = 0
        nodes = range(len(isConnected))

        def dfs(node: int, isConnected: List[List[int]]):
            seen.add(node)
            # O(n) since we loop the entire thing
            for neighbor, flg_neighbor_is_connected in enumerate(isConnected[node]):
                if flg_neighbor_is_connected and neighbor not in seen:
                    seen.add(neighbor)
                    dfs(neighbor, isConnected)
        
        # O(n)
        for node in nodes:
            if node not in seen:
                num_provinces += 1
                dfs(node, isConnected)
        
        return(num_provinces)


```