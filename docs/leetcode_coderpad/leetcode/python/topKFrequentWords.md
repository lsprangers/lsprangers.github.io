---
title: topKFrequentWords
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# topKFrequentWords

```python
class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        # Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.
        freqs = collections.Counter(words)
        
        maxHeap = []
        for word, freq in freqs.items():
            # freq, then lexico order
            heapq.heappush(maxHeap, (-freq, word))
        
        resp = []
        for _ in range(k):
            _, word = heapq.heappop(maxHeap)
            resp.append(word)
        
        return(resp)
        
        
```