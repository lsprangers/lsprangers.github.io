---
title: Trie
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Trie

```python
class TrieNode:
    def __init__(self):
        self.links = [None] * 26
        self.is_end = False
        
    def contains_next(self, char: str) -> bool:
        return(
            self.links[ord(char) - ord('a')] is not None
        )
        
    def put_link(self, char: str, node: 'TrieNode') -> None:
        self.links[ord(char) - ord('a')] = node
        
    def get_char(self, char: str) -> 'TrieNode':
        return(self.links[ord(char) - ord('a')])
    
    def set_end(self) -> None:
        self.is_end = True
        
    def is_end(self) -> bool:
        return self.is_end
    
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if not node.contains_next(char):
                node.put_link(char, TrieNode())
            node = node.get_char(char)
        node.set_end()
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if not node.contains_next(char):
                return(False)
            node = node.get_char(char)
        return(True)
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if not node.contains_next(char):
                return(False)
            node = node.get_char(char)
        return(node.is_end)
    
    def top_k_with_prefix(self, prefix: str, k: int) -> list:
        def dfs(node, path, results):
            if node.is_end and len(results) < k:
                results.append(''.join(path))
            for i in range(26):
                next_node = node.links[i]
                if next_node:
                    path.append(chr(i + ord('a')))
                    dfs(next_node, path, results)
                    path.pop()
        
        node = self.root
        for char in prefix:
            if not node.contains_next(char):
                return []
            node = node.get_char(char)
        results = []
        dfs(node, list(prefix), results)
        return results
```