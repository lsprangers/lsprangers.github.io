---
title: Template
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement


### Example


### Constraints


### Initial Thoughts, Questions


### Implementation
```python
# You are given a list of task names and a cooldown n

# Each task takes 1 unit of time. Same task types must be separated by at least n units of time

# Return the minimum total time needed to execute all tasks

tasks = ["A", "A", "A", "B", "B", "B"]
n = 2

# order of array doesn't matter - A B idle A in example
# therefore, we could use a deque f 
# [A, A, A, A, B, C, C, C]
# I was going to say a deque [(4, A), (1, B), (3, C)]
# [(4, A), (1, B), (3, C)]
# [(1, B), (3, C), (3, A)]
# [(3, C), (3, A)]
# [(3, A), (2, C)]
# [(2, C), (2, A)]
# ..
# [(2, A), (1, C)]

# where we just pop off left and move it to the right. The edge case where this fails is 
# [A, A, A, B, C, D] where we'd want to "intertwine" A's inbetween B, C, D
# (3, A), (1, B), (1, C), (1, D)

# When we pop A and reduce we have (2, A), (1, B), (1, C), (1, D) - we can't do A, so we move to next item 

# The invariant here is that we want to continuously reduce the largest items as fast as possible as to
#   not get stuck in idle time. If we use lazy deque approach, which is greedy, there may be times we are
#   idle when we don't have to be

from collections import Counter
import heapq

def leastInterval(tasks: list[str]) -> int:
    counts = Counter(tasks)

    # available: max heap using negative counts
    available = [(-count, task) for task, count in counts.items()]
    heapq.heapify(available)
    # can use deque b/c same cooldown for each task
    cooldown = deque([])
    
    time = 0
    
    while available or cooldown:
        # (nextTime, count, task)
        while cooldown and cooldown[0][0] <= time:
            nextTime, negCount, task  = cooldown.popleft()
            
            heapq.heappush(available, (negCount, task))
        
        if available:
            negCount, task = heapq.heappop(available)
            
            # move to 0
            negCount += 1
            time += 1
            nextTime = time + n
            # if still items
            if negCount < 0:
                cooldown.append((nextTime, negCount, task))
        
        else:
            # no item, idle (just siimulate skip)
            time = cooldown[0][0]
    
    return(time)



def leastIntervalVariableCooldown(tasks: list[str], cooldowns: dict[str, int]) -> int:
    counts = Counter(tasks)

    # available: max heap using negative counts
    available = [(-count, task) for task, count in counts.items()]
    heapq.heapify(available)
    # needs to be a minHeap on next available items on cooldown
    cooldown = []
    
    time = 0
    
    while available or cooldown:
        # (nextTime, count, task)
        while cooldown and cooldown[0][0] <= time:
            nextTime, negCount, task  = heapq.heappop(cooldown)
            
            heapq.heappush(available, (negCount, task))
        
        if available:
            negCount, task = heapq.heappop(available)
            
            # move to 0
            negCount += 1
            time += 1
            nextTime = time + cooldowns.get(task, 0) # now we need to heappush based on cooldown
            # if still items
            if negCount < 0:
                heapq.heappush(cooldown, (nextTime, negCount, task))
        
        else:
            # no item, idle (just siimulate skip)
            time = cooldown[0][0]
    
    return(time)

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
