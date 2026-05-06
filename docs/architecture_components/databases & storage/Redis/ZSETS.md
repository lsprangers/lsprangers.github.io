---
layout: technical
title: Redis ZSets
category: Architecture Components
difficulty: Advanced
description: Discussion around Redis
---

## Redis ZSets
Redis Sorted Sets, i.e. Redis ZSets, is a collection of unique strings (members) ordered by an association score. When ties occur, the strings are ordered lexicographically

The typical use cases for them are:
- **Rate Limiters**: You can use a sorted set to build a sliding window rate limiter
- **Min Heap**: You can do $O(\log n)$ insertion and deletion while evicting stale entries (similar to rate limiter)
- **Leaderboards**: Maintaining an ordered list of highest scores in massive online games

Sorted Sets are a mix between a sorted set and a hash, where it's composed of unique, non-repeating string elements, but alongside it each element is associated with a floating point value, ***the score***, which allows them to be ordered. Elements from the set are taken in order:
- Items are not natively stored in order in the underlying set
- Upon request, the items are taken based on ordering of score

The implementation is done via [skip list](/docs/dsa/4.%20linked%20lists/index.md#skip-lists) and hash tables:
- Skip lists aid in ordered access
- Hash tables for $O(1)$ lookup
- Adding is $O(\log n)$ via `ZADD`
    - Inserting into a skip list is $O(\log n)$
- Retrieving an element is $O(1)$
    - Checking hash table
- Retrieving ranges themselves are $O(\log n + k)$ via `ZRANGEBYSCORE` and `ZRANGE`
    - Traversing a skip list $O(\log n)$
    - Returning $k$ results $O(k)$
    - `ZREVRANGE` gives the highest scores first, `ZRANGE` default to ascending, not descending
- Popping / deletion is $O(\log n)$ via `ZREM`
- `ZRANK` gives the relative ranking of an item in the scorebaord, these operations are also $O(\log n)$
- Updates are $O(\log n)$ as it adjusts current value and repositions the member
    - Delete + add ( `ZREM` + `ZADD`)

### Postgres Vs Redis
Typically in interviews I'd utilize Postgres + indexes for as much as possible, but Redis is actually more performant for these specific range / rank based solutions like leaderboards

Keeping an ordered list of players by their score, updating them, and retrieving them, even with ranges, is comparative or better performance than Redis - mostly due to [BTree Indexes](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE/index.md) on postgres which fulfill the $O(\log n)$ time complexities, however the ranking operation of `ROW_NUMBER() OVER(ORDER BY score DESC) AS rank` operation is a full $O(N)$ window scan in postgres, which is much less performant than the Redis counterpart

Operation            | Redis Sorted Set | PostgreSQL (indexed)
---------------------|------------------|---------------------
ZADD / UPDATE        | O(log N)         | O(log N) index update
ZREVRANK             | O(log N)         | O(N) window scan*
Top-K query          | O(log N + K)     | O(K) with index
Score range query    | O(log N + M)     | O(log N + M)
Player count         | O(1) ZCARD       | O(1) with count cache

### Rate Limiter
Implementing a [rate limiter](/docs/leetcode_coderpad/coderpad_implementations/rate_limiter.md) can be done easily in memory with a sliding window, but becomes increasingly complex when ***we hit the scale of millions of requests per minute*** (millions of entries in a list will explode local memory) and have ***to start distributing requests and keeping some sort of (eventually) consistent counter***

The main trade-offs on strict consistency, memory limitations, and distribution lead to a wide range of solutions, and a fair amount of them are backed by Redis:
- Sliding window can be achieved with ZSets
    - Fixed window counters are more efficient on memory, but can lead to edge cases where more than allowed requests get through
        - `INCR` and `EXPIRE` calls used to track based on fixed windows, but if there's 10 requests at 1:59, and 10 more at 2:01, we effectively allow 20 calls in 2 seconds
    - Strict sliding windows can be implemented with ZSets, but expirey calls must be performed as an API call, so they can only occur on `GET` requests, or as a background process
        - If background process, need to ensure it also occurs during `GET` to ensure no concurrency issues
    - `ZRANGEBYSCORE` and deletions `ZREMRANGEBYSCORE` run efficiently in Redis
        - Expiry issues still matter, and periodic cleanup is needed. That being said, the range scores will ensure we check a strict range, and that old values aren't included in count
- Token bucket can be achieved with counters based on fixed windows, or using `INCR` and `EXPIRE` as a generic counter (bucket)
    - Incrementing can only be done on check calls, or by a background process, so some calculations are needed to refill based on last timestamp called
    - Lua scripting can be used to ensure consistency and concurrency issues are mitigated, but it's at the cost of latency and potential blocking

Background removal of old scores can be done via `ZREMRANGEBYSCORE`, and this can be done during `GET` or as a backhround process, but `ZRANGEBYSCORE` should still count only active values even if old ones exist. ***Cleanup is required for memory and performance, not correctness***

#### Sliding Window
Implementing a sliding window rate limiter utilizing Redis ultimately comes in 2 flavors:
- True sliding window with `INCR` and `EXPIRE` calls
    - Pros:
        - Accurate (no edge cases). Strict deny
        - Can be consistent with Lua scripting
        - Efficient retrieval, addition, and deletion
        - Can shard based on `userId` or some identifier to reduce strain
            - Con would lead to potential hot keys here
    - Cons:
        - Requires `EXPIRE` calls on `GET`, or as background process
        - Keeps all requests stored, so memory is proportional to $N$ requests
            - Redis can handle hundreds of thousands of RPS, but storing millions of events, i.e. linear space complexity, becomes extremely expensive at large scale
- Fixed Bucket Sliding Window
    - For each time bucket, like each minute, simply start a new counter
    - Pros:
        - Accurate to a certain degree, but has edge cases that allow for double overages
        - Efficient memory utilization - $O(1)$ because we are just storing integer counts across some fixed slice of time windows (not storing all historic time series info, just before window and curr window)
        - Can shard based on `userId` or some identifier to reduce strain
            - Con would lead to potential hot keys here
        - Time complexity at $O(1)$ instead of $O(\log n)$ as it's a simple fixed counter
    - Cons:
        - Edge cases allow for double rate limited set. Occurs if user makes $N-1$ requests at `t:59` and another $N-1$ requests at `t+1:01`, this means $\approx$ $2N$ calls can be made in 2 seconds
- Weighted Estimate Sliding Window
    - Based on `(prev_count * overlap_pct) + curr_window_count`
    - Pros:
        - Accurate to a certain degree, but has edge cases that allow for potential overages (not nearly as bad as fixed bucket)
        - Efficient memory utilization - $O(1)$ because we are just storing integer counts across some fixed slice of time windows (not storing all historic time series info, just before window and curr window)
        - Can shard based on `userId` or some identifier to reduce strain
            - Con would lead to potential hot keys here
        - Time complexity at $O(1)$ instead of $O(\log n)$ as it's a simple fixed counter
    - Cons:
        - We've removed the $2N$ possible calls by utilizing the `overlap_pct`, but there's still edge cases for $\gt N$ calls at the boundaries

### Min Heap
References [OneUpTime Article](https://oneuptime.com/blog/post/2026-01-21-redis-priority-queues-sorted-sets/view?utm_source=chatgpt.com)

Implementing [priority queue's / min heaps](/docs/dsa/5.%20heap%20&%20priority%20queue/index.md) in a local process is fairly straightforward, but setting these up in a distributed manner utilizing another API is typically difficult. There aren't many solutions for distributing a min heap, but there are solutions for sharding min heaps, and aggregating multiple min heaps

Redis ZSets allow for pushing out the min-heap storage from a local process to a single Redis cluster - ultimately, it's the same operations with the same time complexity, but not bounded to whatever our local RAM memory is

<!-- Collapsible Python snippet -->
<details>
  <summary>Show Python Script</summary>

```python
import redis
import time
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

class PriorityQueue:
    def __init__(self, name, redis_client):
        self.key = f"pq:{name}"
        self.redis = redis_client

    def push(self, item, priority):
        """
        Add item with priority (lower score = higher priority).
        Use negative priority if you want higher numbers = higher priority.
        """
        self.redis.zadd(self.key, {item: priority})

    def pop(self):
        """Remove and return highest priority item (lowest score)"""
        result = self.redis.zpopmin(self.key)
        if result:
            return result[0][0]  # Return item without score
        return None

    def peek(self):
        """View highest priority item without removing"""
        result = self.redis.zrange(self.key, 0, 0)
        if result:
            return result[0]
        return None

    def pop_with_priority(self):
        """Remove and return (item, priority) tuple"""
        result = self.redis.zpopmin(self.key)
        if result:
            return (result[0][0], result[0][1])
        return None

    def size(self):
        """Get queue size"""
        return self.redis.zcard(self.key)

    def is_empty(self):
        """Check if queue is empty"""
        return self.size() == 0

    def clear(self):
        """Remove all items"""
        self.redis.delete(self.key)

# Usage
pq = PriorityQueue('tasks', r)

# Add tasks with priorities (lower = more urgent)
pq.push('critical-alert', priority=1)
pq.push('normal-task', priority=5)
pq.push('low-priority-cleanup', priority=10)
pq.push('urgent-fix', priority=2)

# Process in priority order
while not pq.is_empty():
    task = pq.pop()
    print(f"Processing: {task}")
```

</details>

#### Distributed Heap
None of this covers sharding, which would still be bounded to a similar setup as the [K Sorted Streams](/docs/leetcode_coderpad/coderpad_implementations/merge_k_sorted_streams.md) where you have multiple "local" (or redis based) priority queue's which have $O(\log n)$ add and remove, and for each of those you aggregate them to a "global" (or yet another redis based) aggregator 

It's suboptimal to store all local results also in the global result, as that simply introduces unnecessary local aggregators at that point. If the global one is evicting stale information, and the local ones are strictly to handle sharded writes, and they're also evicting old information, then there's a useful setup there. That being said if the global aggregator is overwhelmed for a period of time, there's a chance it doesn't see a high score in a certain time frame, and so the global and local aggregators need to be based on the same window

Furthermore, consistent hashing of `userID` comes into play, where if our clusters scale up or down a portion of `userID` would need to get remapped, which means removing them from a priority queue and adding them to another
op