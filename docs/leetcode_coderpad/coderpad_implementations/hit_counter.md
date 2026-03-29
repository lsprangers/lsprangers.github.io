---
title: Hit Counter
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Implement:
```python
class HitCounter:
    def hit(self, timestamp: int) -> None:
        ...
    def get_hits(self, timestamp: int) -> int:
        ...
```

### Constraints
Requirements
- `timestamp` is in seconds
- record a hit at `timestamp`
- return the number of hits in the past 300 seconds, inclusive of the current second
- assume `timestamps` passed to both methods are monotonically non-decreasing
- optimize for many calls
- discuss tradeoffs if the monotonicity assumption is removed

### Initial Thoughts, Questions
- Rate limiting problem
- Space
    - Sliding window ensures absolute correctness, but requires $O(n)$ space (full priority queue)
    - Fixed buckets are much cheaper space wise, but allow for overages at edges
    - Fixed counter is cheapest time wise, but can't do "last 300 seconds" very well, it's just total over time
    - Covering the spec I'd assume sliding window in this in-memory solution so that it's absolute correctness
- Monotonicity
    - Right now we can use a simple storage structure with append and pop pointers (deque) which gives us $O(1)$ append and pop. We can do this becuase we know timestamps are monotonically increasing, and so appending them keeps the sorted structure
    - If this assumption wasn't true, we'd need a priority queue for inserts which would be $O(log n)$ insert and pop to keep the sorted structure
    - Both allow for draining the total hits and appending in an efficient time, which means returning total hits can be an efficient return. We do have to drain the sorted structure in `get_hits`, and so it's never $O(1)$


### Implementation
```python
# import heapq
from collections import deque
class HitCounter:
    def __init__(self):
        # [oldest, ...., newest]
        self.dq = deque([])

    def hit(self, timestamp: int) -> None:
        # appends to right
        self.dq.append(timestamp)
        return

    def get_hits(self, timestamp: int) -> int:
        # [0, 10, 70, 100, 150, 200, 300, 350, 450, 480, 500]
        # get_hits(400)
        # 400 - 300 = 100, so pop everything off before and including 100
        # [150, 200, 300, 350, 450, 480, 500]
        while self.dq and self.dq[0] <= (timestamp - 300):
            self.dq.popleft()
        
        return(len(self.dq))
```

### Follow Up
Many hits at the same timestamp - can memory be reduced by compressing repeated timestamps
```python
# import heapq
from collections import deque
class HitCounter:
    def __init__(self):
        # [oldest, ...., newest]
        self.dq = deque([])
        self.curr_len = 0

    def hit(self, timestamp: int) -> None:
        # appends to right
        if self.dq and self.dq[-1][0] == timestamp:
            self.dq[-1][1] += 1
        else:
            self.dq.append([timestamp, 1])
        
        self.curr_len += 1
        return

    def get_hits(self, timestamp: int) -> int:
        # [0, 10, 70, 100, 150, 200, 300, 350, 450, 480, 500]
        # get_hits(400)
        # 400 - 300 = 100, so pop everything off before and including 100
        # [150, 200, 300, 350, 450, 480, 500]
        while self.dq and self.dq[0][0] <= (timestamp - 300):
            expired_ts, expired_ts_count = self.dq.popleft()
            self.curr_len -= expired_ts_count
        
        return(self.curr_len)
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
