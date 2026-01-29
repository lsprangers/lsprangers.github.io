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
    - In practice: a request at time t should consider previous requests with timestamps > t - windowMillis
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