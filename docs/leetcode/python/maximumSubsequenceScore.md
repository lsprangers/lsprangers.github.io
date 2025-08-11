---
title: maximumSubsequenceScore
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# maximumSubsequenceScore

The reason we can't use bactracking is that it'll find all ${n \choose k} = {{n!} \over {k!} \cdot {(n-k)!}}$

The one major restriction here is if we choose some index $k$ for our `nums2` minimum, all we have to do is find the 2 largest values in `[0, k-1]`, so we can instead use a min-heap for this

## TLE - Backtracking
```python
class Solution:
    def __init__(self):
        self.resp = -float("inf")
        self.seen = set()

    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        # Solutions:
        #   - Permutations, and checking for each permutation of size
        #       - TLE! We explore all (n choose k) which "explodes"
        #   - Maybe some weird DP problem, but state transition isn't clear
        #   - Some weird window problem, but lots of "ifs"
        #   - A greedy problem, but there are edge cases where it fails
        self.backtrack(nums1, nums2, [], k, 0)
        return(self.resp)

    def backtrack(self, nums1: List[int], nums2: List[int], curr: List[int], k: int, idx: int):
        if len(curr) == k and tuple(curr) not in self.seen:
            total_sum = sum([num for idx, num in enumerate(nums1) if idx in curr])
            multiplier = min([num for idx, num in enumerate(nums2) if idx in curr])
            self.seen.add(tuple(curr))
            
            self.resp = max(
                self.resp,
                total_sum * multiplier
            )
        
        for next_idx in range(idx, len(nums1)):
            curr += [next_idx]
            self.backtrack(nums1, nums2, curr, k, next_idx + 1)
            curr.pop()
        
        return
```

## Greedy
The intuition here is greedily choosing `n2`, and then choosing all other largest n1's to find the max score

```python
class Solution:
    def __init__(self):
        self.resp = -float("inf")
        self.seen = set()

    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        # Solutions:
        #   - Permutations, and checking for each permutation of size
        #       - TLE! We explore all (n choose k) which "explodes"
        #   - Maybe some weird DP problem, but state transition isn't clear
        #   - Some weird window problem, but lots of "ifs"
        #   - A greedy problem, but there are edge cases where it fails
        #       - Guess this is the one!
        pairs = sorted(zip(nums2, nums1), reverse=True)  # sort by nums2 desc
        heap = []
        curr_sum = 0
        max_score = 0
        
        for n2, n1 in pairs:
            heapq.heappush(heap, n1)
            curr_sum += n1

            # pop off smallest n1 we've seen so far
            if len(heap) > k:
                curr_sum -= heapq.heappop(heap)

            # get max
            if len(heap) == k:
                max_score = max(max_score, curr_sum * n2)

        return max_score     
```