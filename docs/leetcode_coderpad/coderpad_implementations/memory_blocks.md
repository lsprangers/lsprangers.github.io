---
title: Template
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Regroup
For any target MEX = `m`, we must find an array such that:
- `0, ..., m-1` present, to ensure that `m` is still the smallest
- `m` must not be involved

## Initial Problem Statement
You are given an array `memoryBlocks` of length `n`, where each element represents the size of a memory block.

You may perform the following operation any number of times:
- Choose an index `i`
- Increase `memoryBlocks[i]` by 1
- You may only do this if `memoryBlocks[i] < n - 1`

After any sequence of operations, define the valid size of the array as its `MEX`:
- The `MEX` of an array is the smallest non-negative integer that does not appear in the array
- Your task is to return all distinct `MEX` values that can be achieved, sorted in increasing order

### Example
`memoryBlocks = [0, 3, 4]`

`n=3`, so we can only increase memory blocks if `memoryBlocks[i] < 2`
Possible outcomes:
- Start: `[0, 3, 4]` --> MEX = 1
- Increment index 0: `[1, 3, 4]` --> MEX = 0

### Constraints


### Initial Thoughts, Questions
- For an `m`, we need:
- `0, ... m-1` in an array
- `m` not in the array

Greedily, if we are looking at `m=5`, we'll need to check that we can get to `0,1,2,3,4` in the array somehow. If there's no 0, we are done it's impossible. If there's no 1, but we have two 0's, we can get there, etc

So we can reuse smaller values up to a certain extent - how to check those?
For `m=5` with `[0,0,1,1,4,5,5]`. We know we can go up to `n-1`. We can work backwards, starting at `m` and ensuring that we can increment those upwards

### Implementation
```python
def findValidSizes(memoryBlocks: list[int]) -> list[int]:
    freqs = collections.Counter(memoryBlocks)
    n = len(memoryBlocks) - 1
    # [0, 0, 0, 1, 4, 5, 6]
    memoryBlocks.sort()
    total_resp = 0
    for m in range(n):
        left = 0
        right = 0
        while right < len(memoryBlocks):
            
        
        

"""
[0, 3, 4] --> increase 0 up to 3

[0, 1, 1, 2, 2, 2, 3, ...] --> in this case if there's 800 entries,
    and we look at entry 0, we know we can get from 0-800 by simply incrementing the 0.
    More generically, we can get from any value, ideally the minimum value in the array,
    to all other values up to the size of the array, except for values present in the array.
    The range of possible MEX values are [min(array), len(array) - 1] - if we take this list and remove
    all values that exist in the array, that should solve the problem

[0, 0, 0] - [0, 2]
- If we increment [1, 0, 0] --> MEX is 2
- Do nothing, MEX is 1
- Increment all [1, 1, 1] --> MEX is 0

[0] --> [0, 0] --> MEX is 1

[0, 0, 0, 0, 0] 5 0's, so range is [0, 4]
- [1, ...] would give us MEX 2
- [1, 2, ... ] would give us MEX 3
- ...

So I feel like I'm approaching a pattern, but I can't quite rationalize it

[0, 1, 2, 3, 4] --> [0, 4]
- Increment first --> MEX 0
- Increment second --> MEX 1
- Can only get to MEX 3, which shows [0, 4] except 4 exists and we can't increment it

Pattern seems to be, go from the min up to the length, but exclude any values which are "stuck"

"""
```

## Systems Design


### High Level requirements


#### API Surface

#### Clarifying Questions
Questions around implementations, strict vs approximate, and anything that would kill any choices made in future

#### System Constraints
Summarize system constraints in your own words
- QPS 
- latency SLO    
- consistency requirements
- failure tolerance

#### Identify Core Challenges
What makes this problem hard in distributed manner (MOST IMPORTANT PART)
- Distributed correctness (no double allow)
- Routing / management
- Data structure
- Scale + latency
- Failure behavior
- single-writer vs linearizable store
- availability vs consistency
- data plane vs control plane

#### Starter Architecture
Distributed compatible, but high level components and algorithms, focus on partitioning and scaling, not frontend or anything. Some data structure information is OK, specifically ones that relate to the core problem.

Components + Flow + network, partition, and some data structures

#### Real Architecture
Now you make in depth choices on literally everything, and draw the entire thing out

#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture
