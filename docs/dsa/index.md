---
title: Data Structures & Algorithms
layout: default
---

## DSA
This is a dump of all the DSA notes I had from school, coursework, and interviews

## Cheat Sheet
- Use prefix sum + hashmap for ***exact subarray sum*** questions: 
    - count, existence, longest length, divisible/mod variants, especially when negatives may exist
- Use sliding window for ***monotonic*** window problems based on ***at-most, or exact subarray*** questions:
    - at-most constraints, character frequency windows, and sum constraints on nonnegative arrays
    - count valid subarrays with `right - left + 1`
- Prefix-sum init: 
    - `freq = {0: 1}` for counting 
    - `first = {0: -1}` for longest length
    - usually keep only a running sum, not a full prefix array
- If negatives exist, standard sum-based sliding window is usually wrong; prefix sums still work

The number of subarrays between `left, right` is `right - left + 1`

- Use binary search on answer when the output is a min/max value and you can write a monotonic `check(mid)`
- If `check(x)` is true, then all smaller values are also true, or all larger values are also true
- Search the answer space, not the array: 
    - capacity, speed, sweetness, threshold, minimum/maximum feasible value
- Main job is not coding binary search; it is proving the monotonicity and writing `check(mid)` correctly
- Use half-open interval: search space is `[left, right)`
- For most problems, half open will work
    - `mid = left + (right - left) // 2`
    - Initialize with `left = 0`, `right = len(arr)`
    - Loop with `while left < right`
    - If mid is good, do `right = mid`; otherwise do `left = mid + 1`
    - return `left` as first valid position or insertion point
- For last valid X, need to switch to:
    - `mid = left + right + 1 // 2`
    - `left = mid`
    - `right = mid - 1`