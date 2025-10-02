---
title: countElementsWithMaxFrequency
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countElementsWithMaxFrequency

```python
class Solution:
    def maxFrequencyElements(self, nums: List[int]) -> int:
        freqs = collections.Counter(nums)
        inv_freqs = defaultdict(list)

        curr_max = 0
        for k,v in freqs.items():
            curr_max = curr_max if curr_max > v else v
            inv_freqs[v].append(k)
        
        resp = 0
        for num in inv_freqs[curr_max]:
            resp += freqs[num]
        
        return(resp)
```