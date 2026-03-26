---
title: Streaming Longest Subarray Sum K
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Implement this:
```python
class LongestSubarraySumK:
    def __init__(self, k: int):
        ...
    def add(self, x: int) -> int:
        """
        Add next value from the stream
        Return the maximum length of any contiguous subarray seen so far
        whose sum is exactly k
        """
```


### Constraints
- numbers may be positive, zero, or negative
- stream is append-only
- `add(x)` should update internal state and return the best answer seen so far
- optimize for incremental updates, not recomputing from scratch


### Initial Thoughts, Questions
- In an array `arr = [1, 3, 5, -8, 10]`, the sum between any two numbers can be given by prefix sum
- `pfxSum = [1, 4, 9, 1, 11]`, so the total between indexes i and j is `pfxSum[j] - pfxSum[i - 1]`
- Keeping this in streaming fashion, we just need to append the new value of the prefix sum to the end, which is an $O(1)$ operation since it's just `pfxSum.append(pfxSum[-1] + new_val)`
- We also need to keep indexes of values of prefix sums in a K:V store so that we can lookup the corresponding "other value" to get to $K$
    - If $K = 10$, and our prefix sum is currently at `pfxSum[-1] = 4`, we need to find `k - pfxSum[-1]` or 6 in the prefix sum list, which is $O(1)$ if we utilize a KV store. We store all the indexes of 6 and every other value, and for any index less than the newest one we just pick the index that corresponds to the longest subarray, which would be the first one seen
        - Therefore, we only need to keep the index of the first value seen, not an actual list
- To make the lookup clean, we can initialize prefix sum to be `pfx_sum = [0]`, and `idx_lookup[0] = -1`
    - Then finding `curr_prefix - earlier_prefix = k` is easier and doesn't involve `x - 1` indexing

### Implementation
```python
class LongestSubarraySumK:
    def __init__(self, k: int):
        self.idx_lookup = {}
        self.curr_prefix = 0
        self.curr_prefix_idx = 0
        self.k = k
        self.best = 0

    def add(self, x: int) -> int:
        """
        Add next value from the stream
        Return the maximum length of any contiguous subarray seen so far
        whose sum is exactly k
        """
        self.curr_prefix += x
        self.curr_prefix_idx += 1

        # Given there's an initial 0, [0, 1st, 2nd, etc...] the first value has idx = 1
        #   so our lookups need to be careful of size with this
        if self.curr_prefix not in self.idx_lookup:
            self.idx_lookup[self.curr_prefix] = self.curr_prefix_idx - 1
        
        # need to find abs(curr_prefix - k)
        # curr_prefix - earlier_prefix = k
        lookup = self.curr_prefix - self.k
        if self.curr_prefix == self.k:
            self.best = max(self.best, self.curr_prefix_idx)

        elif lookup in self.idx_lookup:
            self.best = max(self.best, self.curr_prefix_idx - self.idx_lookup[lookup] + 1)

        return(self.best)

if __name__ == "__main__":
"""
kv = {
    1: 0
    0: 1
    5: 2
    3: 3
    6: 4
}
pfx = [1,  0, 5,  3, 6]
arr = [1, -1, 5, -2, 3]
curr_pfx_sum = 6
cpffxidx = 5
"""

    t = LongestSubarraySumK(3)
    t.add(1) # find 1 - 3 = -2 --> 0
    t.add(-1) # find 0 - 3 = -3 --> 0
    t.add(5) # find 5 - 3 = 2 --> 0
    t.add(-2) # find 3 - 3 = 0 --> 4
    t.add(3) # find 6 - 3 = 3 --> 5 - 3 + 1 = 3
"""
kv = {
    3: 0
    2: 1
    6: 3
    9: 4
}
pfx = [3,  2, 2, 6, 9,  6]
arr = [3, -1, 0, 4, 3, -3]
"""
    test = LongestSubarraySumK(6)
    test.add(3)     # find 3 - 6 = -3
    test.add(-1)    # find 2 - 6 = -4
    test.add(0)     # find 2 - 6 = -4
    test.add(4)     # find 6 - 6 = 0 --> 4
    test.add(3)     # find 9 - 6 = 3 --> 5 - 0 - 1 = 4
    test.add(-3)

"""
kv = {
    1: 0
    3: 1
    6: 2
}
pfx = [1, 3, 6]
arr = [1, 2, 3]
"""
    test2 = LongestSubarraySumK(5) 
    test2.add(1) # find 1 - 5 = -4 --> 0
    test2.add(2) # find 3 - 5 = -2 --> 0
    test2.add(3) # find 6 - 5 = 1 --> 3 - 0 - 1 = 2. [2, 3] is the correct subarray, it is the correct length

"""
kv = {
    -1: 0
    2: 2
    10: 3
    5: 4
    0: 5
}
pfx = [-1, -2, 2, 10, 5,  0, 5]
arr = [-1, -1, 4, 8, -5, -5, 5]
"""
    test3 = LongestSubarraySumK(5)
    test3.add(-1) # find -1 - 5 = -6 --> 0
    test3.add(-1) # find -2 - 5 = -7 --> 0
    test3.add(4) # find 2 - 5 = -3 --> 0
    test3.add(8) # find 10 - 5 = 5 --> 0
    test3.add(-5) # find 5 - 5 = 0 --> 5
    test3.add(-5)
    test3.add(5) # find 5 - 5 = 0 --> 7, which is correct. This is the longest subarray
```