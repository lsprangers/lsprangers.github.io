---
title: In Memory Rate Limiter
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Rate Limiter
- This is a quick demonstration of doing a Rate Limiter
- The goal is to have some approach that sits in memory to rate limit incoming requests from a "client"




```python

from dataclasses import dataclass
from ipaddress import ip_address, IPv4Address
import time
from collections import defaultdict, deque

@dataclass
class POST_STRUCT:
    timestamp: int
    ip: IPv4Address
    data: dict

class RateLimiter:
    def __init__(self, time_window = 3, rate_limit = 2):
        self.time_window = time_window
        self.rate_limit = rate_limit
        self.failed_response = 429
        self.counter = defaultdict(deque)
    def post(self, req: POST_STRUCT) -> bool:
        q = self.counter[req.ip]
        
        # remove bad requests from left
        while q and q[0] <= req.timestamp - self.time_window:
            q.popleft()
        
        # add in any remaining requests that are within window
        if len(q) < self.rate_limit:
            q.append(req.timestamp)
            return(True)
        return(False)


class Client:
    def __init__(self, ip):
        self.ip = ip_address(ip)
    
    def setup_send(self, ts, data):
        req = POST_STRUCT(ts, self.ip, data)
        return(req)


if __name__ == "__main__":
    c1 = Client("1.0.0.1")
    c2 = Client("2.0.0.2")
    c3 = Client("3.0.0.3")

    for ts in range(20):
        rl = RateLimiter()
        
        c1_resp = rl.post(
            c1.setup_send(ts, {1: 1})
        )
        print("c1 Response: " + c1_resp + "\n\n")
        
        c2_resp = rl.post(
            c2.setup_send(ts, {2: 2})
        )
        print("c2 Response: " + c2_resp + "\n\n")
        
        c3_resp = rl.post(
            c3.setup_send(ts, {3: 3})
        )
        print("c3 Response: " + c3_resp + "\n\n")
```