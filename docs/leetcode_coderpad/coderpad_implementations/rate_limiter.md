---
title: Rate Limiter
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
- Design a class:
- `RateLimiter(int maxRequests, long windowMillis)`
    - With a method:
        - `boolean allow(String userId, long timestampMillis)`
- Behavior:
    - Each user is allowed at most `maxRequests` within any rolling time window of size `windowMillis`
    - `allow` returns true if the request is allowed
    - `allow` returns false if the user has exceeded their limit
    - If a request is rejected, it does not count toward future allowed requests

### Example
```ruby
RateLimiter limiter = new RateLimiter(3, 10000);

limiter.allow("A", 0);     // true
limiter.allow("A", 1000);  // true
limiter.allow("A", 2000);  // true
limiter.allow("A", 3000);  // false (3 requests already in last 10s)
limiter.allow("A", 11000); // true (window has slid)
```

### Constraints
- Assume timestamps are monotonically non-decreasing per user
- Requests may interleave across different users
- Aim for efficient per-request performance
- Single-threaded for now (no concurrency required)

### Initial Thoughts, Questions
"Efficient per request performance" means it needs to run quickly and return to user, ideally $O(1)$ or something similar - no crazy memory lookups or anything like that
"Single-threaded" means don't overdo anything

- What to do if a timestamp is equivalent for users? Do we deduplicate or just add it in?
    - Treat each call to allow as an independent request, even if timestamps are equal. No deduplication. If a user sends multiple requests at the same timestamp, they all count
- Is the interval closed? Meaning if we have `[1_000, 2_000, 11_000]` does that count as 3? `11_000 - 1_000 = 10_000`
    - The window is inclusive of the lower bound and exclusive of anything strictly older
    - In practice: a request at time t should consider previous requests with timestamps $\gt$ t - windowMillis
        - Therefore, `11_000` should only consider requests with `timestamp > 11_000 - 10_000 = 1_000`
            - `timestamp > 1_000`, not inclusive
- "requests may interleave across users" - we don't have a `user_id` portion of rate limiter class, is one instance of rate limiter assigned to one single user?
    - One RateLimiter instance handles all users
    - So you need to track per-user request history internally


The general approach I would take is:
- Initialize
    - User dict of `user_id : deque([])` referencing a users transactions
        - The `deque` itself will hold timestamps of all the calls that have been made by that user
- For each call to `allow()`
    - Some initial checks on the K:V user dictionary on if key exists, something simple and quick
    - The deque holds items from left to right, oldest to shortest respectively - i.e. `[1000, 2000, 11_000]`
        - Given the timestamp that's come in, we just run `while` over deque to remove older timestamps based on threshold or until empty
    - `len(user_dict[user_id])` can give us the number of calls the user has made, and this is $O(1)$ in python, but if it wasn't we'd also hold a K:V counter that we update along the way

### Implementation

```python
from collections import deque, defaultdict

class RateLimiter:
    def __init__(self, maxRequests: int, windowMillis: float):
        self.maxRequests = maxRequests
        self.windowMillis = windowMillis
        self.userDict = defaultdict(deque)
    
    def allow(self, userId: int, timestampMillis: float) -> bool:
        # For now I'm just going to bring this in, alter it, and re-equate at end
        user_history = self.userDict[userId]
        
        # [1_000, 6_000] if next request is 11_000, we want to get rid of everything
        #   older than 11_000 - 10_000 = 1_000, i.e. 
        # timestamp_millis = 11_000, windowMillis = 10_000
        # "Therefore, `11_000` should only consider requests with `timestamp > 11_000 - 10_000 = 1_000`"
        # we want to get rid of everything <= 1_000
        while user_history and user_history[0] <= (timestampMillis - self.windowMillis):
            user_history.popleft()
        
        if len(user_history) >= self.maxRequests:
            return(False)
        else:
            user_history.append(timestampMillis)
            return(True)

rl = RateLimiter(3, 10000)
rl.allow("A", 0)
True
rl.allow("A", 1000)
True
rl.allow("A", 2000)
True
rl.allow("A", 3000)
False
rl.allow("A", 11000)
True
rl.userDict
defaultdict(<class 'collections.deque'>, {'A': deque([2000, 11000])})
```

## Systems Design
Design a distributed rate-limiting service that enforces:

- Limit: 100 requests per user per minute
- Across multiple API servers  
- Global consistency required
- p99 latency $\lt$ 10ms for allow() check
- System must scale to 50M requests/sec total


### High Level requirements
- Must work across many stateless API servers
- Must enforce the limit globally, not per node
- Users may hit different servers for sequential requests
- Failover and partial network partitions are expected
- The service must not dramatically degrade during Redis/DB failures
- Cost efficiency matters

#### API Surface
```
allow(userId, timestamp) → true/false
```

#### Clarifying Questions
- Is this rate limiter for one specific backend service, or are we checking multiple users across multiple services?
    - One centralized rate limiting service used by many backend API's
    - Rate limiter must enforce limits per user globally, regardless of downstream service
- How strict / consistent does this need to be? In terms of timing, counts, etc is it absolutely required that 100 cannot be stopped over any minute period?
    - Strict. A user must never successfully exceed 100 true responses in any sliding 60 second window
        - Occasional false negatives (deny when should allow) are acceptable
        - False positive (allow when $\gt$100) should never happen
    - Strong enforcement
- "User may hit different servers for sequential requests", can you explain this requirement more? It seems like a strange requirement
    - There are many API GW / Edge servers that are routing requests to this rate limiter service
    - Users traffic isn't sticky to any of these API GW services
    - Rate limit must still be correct
- How are clients identified?
    - `userId` is reliable, and each incoming request to rate limiter receives `(userId, timetamp)`

#### System Constraints
The rate limiting service needs to track a users total request count over a sliding window of 60 seconds, and the requests are coming in from many different API GW and edge servers at 50M req / second, we must respond with $\lt$ 10ms p99 latency, even in the face of network failures or partition failures. The system must continue even if backend redis / database failures occur, and the system has strict allow rules meaning a user should never be allowed $\gt$ 100 requests per minute, with the occasional false positive being acceptable

#### Identify Core Challenges
The challenges here are going to be
- Accepting this many requests coming in (50M / second), and updating a data structure that also allows for fault tolerance, while replying within 10ms 99% of the time
- Achieving horizontal scaling, consistency (hard deny), and failover across partitions means we can't have a single point of failure for any user / group of users
- Keeping a time based data structure in memory that allows for $\lt$10ms response is difficult, especially given we will be receiving requests, updating a data structure, and then using that data structure to respond. This data structure must be ordered for time, or bucketed in some way that allows for time based queries in an efficient manner
    - Sliding windows are usually used in these scenario's
- The hard deny also means that any node that returns a response must have all available information, because if a new request comes in while the current one is being processed (at the edge case of 100), we may return `allow` when it should be `deny` - that is if at time `t` the current counter is at 99, and we receive a check so we're at 100, and we reply at time `t + s`, then if another check call occurs at time `t* < t + s`, we would return `allow` when that should be deny
    - This concurrency discussion is of key importance on how we handle users and partitions
- Single node per user is required for strictly consistent correctness, which creates a challenge for high availability, and for split-brain scenario's during re-booting or re-partitioning
    - Given potential network partitions, downtimes, reboots, etc our system, if it doesn't receive a response from the API GW, should respond `deny`

#### Starter Architecture
To achieve the above we should focus on:
- Scalable routing - getting requests efficiently to authoritative nodes requires consistent hashing, even in the face of rebalances, node outages, etc
    - Rebalances could potentially affect which underlying VM is actually accepting the request for a specific `userId`
    - Node outages mean the router needs to have some sort of timeout period for responses
    - This router needs to scale to 50M requests per second, and also handle sending the response back (in most scenario's)
    - Partitioning should be done based on `userId` as it was stated in spec that's a stable parameter
    - Routing should be done by a distributed load balancer, and would have to be at L7 layer given the `userId` comes in as a header. There's ways to switch to network load balancing, but it would require is to make assumptions around IP addresses and ports, so we'll stick to L7 ALB with hashing based on `userId`
        - The routing service needs to implement ring based consistent hashing so that rebalances don't enforce full shuffle of data across nodes
        - The routing service should handle hashing of `userId`, passing to consistent hashing component / service, and that should then route the request to a specific node
        - Consistent hashing depends on binary search, so it will be $O(\log n_nodes)$
        - This can be avoided with caching, but cache invalidation would need to happen if any rebalance occurs. The routing service can handle that as well
            - Caching should make request routing ultimately $O(1)$
- User state data structure - this data structure needs to handle time bounded request information to ensure we can always deny over-using users. There can be no edge cases where a user gets 101 requests in a time window. This data structure needs to be optimized to add on new requests, to identify stale requests, and to get the number of current requests
    - In memory sliding window structures can handle these scenario's efficiently, they can be stored per-user generically across all API's
        - This sliding window is an event deque, where items on the left are new, and items on the right are oldest. We pop from the right and append to the left, each of these operations are $O(1)$ via linked list operations, and length is also $O(1)$
            - Storing this in memory is expensive - we should follow up on average number of users, average number of user requests per minute, etc for an idea on if this storage is even possible
- Fault tolerance, consistency, and high availability
    - There's a large tradeoff between these items, and the spec is clear that consistency and strict deny is the most important, so each node must have all information about the user if it is ever to respond `allow`
    - Availability, consistency, and latency:
        - If we have highly available replicas, that means the leader node must replicate it's data structure on each followers, which could be an issue for the strict $\lt$10 ms latency. These replicas would need to be in consensus if they are to serve future reads if a leader goes down
        - If we choose latency over availability, and a node goes down, we would need to assume the worst on node start (user at saturation), and start collecting checks during that period and counting, while responding `deny` until we have a full minutes worth of information
        - Immediate recommendation would be to choose latency over availability, and if a node shuts down we would `deny` while a new node comes up
            - If this is incorrect, and we need to have immediate restore, then we will need an active replica and the leader will need to route each request to a linearizable backend database. This means transactions, acknowledgements, etc - when we respond `allow` to a request we need to guarantee that makes it to the backend database, so our response cycle now includes a round trip to a database and commit level transaction semantics
    - Fault tolerance
        - Each piece of this architecture has the same tradeoffs of latency, availability, and consistency
            - The router needs to be highly available with failover, and must record some state around `userId --> VM` mapping
            - The authoritative user nodes were described above

Flow:
Typical:
    request --> Routing service (ALB + cache) O(1) --> VM accepts --> Drains deque, checks length --> responds

Failure:
    request --> Routing service (ALB + cache) O(1) --> VM internal 5XX error --> routing service invalidates cache --> respond deny

Node reboot on failure
    Spin up --> identify to routing service --> restart cache




#### Real Architecture
Specifics on partition keys, algorithms for completing the functionality, and actual solid opinionated choices

Draw diagram while explaining

#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture

#### Background
The generic response is to use Lua Scripting with a Redis cluster, but this incurs a network hop, serialization, and general dependencies on Redis that mean there's a hard-deny or hard-accept if Redis ends up going down. Furthermore we need an entire Redis cluster that's sharded by `userId`, which comes with extra issues around user routing, rebalancing, and downtimes. Redis does cover the "Fault Tolerance" portion where things are written to disk, but probably doesn't cover the `5p99 <10ms` latency part, which is an extremely fast SLA + turnaround time. Utilizing Redis also means concurrency limitations and semantics, which is what we are asking for given the hard deny (absolutely nothing $\gt$ 100 requests), and again that kills the p99 latency discussion

“If we require zero false positives under partitions, then the system must fail closed and sacrifice availability or throughput. If we require 50M rps with $\lt$10ms latency, then we must accept either approximate limits or false negatives.”

- Option A — Central Redis-based:
    - Centralized state
    - Atomic Lua scripts
    - Scales to millions rps
    - Fails closed or open
    - Simpler ops
- Option B — Shard-by-user, local memory (strict correctness)
    - Single writer per user
    - No false positives
    - Fail closed on uncertainty
    - Availability loss under failures
    - Harder ops
- Option C — Approximate / token bucket
    - Local counters
    - Gossip / eventual sync
    - High throughput
    - Occasional false positives
    - Best UX

The whole point is to gauge the spec, talk through architecture and what's desired, and start going abck and forth on what can be done, what's harder to implement, and the trade-offs involved

#### Other References
Implementing a rate limiter can be done easily in memory with a sliding window, but becomes increasingly complex when ***we hit the scale of millions of requests per minute*** (millions of entries in a list will explode local memory) and have ***to start distributing requests and keeping some sort of (eventually) consistent counter***

There's another document talking about [Redis ZSets that includes rate limiting](/docs/architecture_components/databases%20&%20storage/Redis/ZSETS.md#rate-limiter)

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

Background removal of old scores can be done via `ZREMRANGEBYSCORE`, and this can be done during `GET` or as a backhround process, but `ZRANGEBYSCORE` should still count only active values even if old ones exist