
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
