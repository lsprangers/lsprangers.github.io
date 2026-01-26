---
title: numberOfRecentCalls
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# numberOfRecentCalls

```python
# 933
class RecentCounter:

    def __init__(self):
        self.requests = deque()
        self.resp = 0

    def ping(self, t: int) -> int:
        # O(?) --> O(3000) worst case so O(1)
        while self.requests and self.requests[0] < (t - 3000):
            # O(1)
            self.requests.popleft()
            self.resp -= 1
        
        # O(1)
        self.requests.append(t)
        self.resp += 1
        return(self.resp)


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)
```