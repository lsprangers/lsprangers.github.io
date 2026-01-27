import heapq
from typing import List, Dict, Tuple
from collections import deque, defaultdict

# Mixing up coding conventions between camelCase and my_underline_method
#   sorry - it's just how I think for now, I will change after review

# Assumptions:
#   - hold_id is unique
#   - timestamps passed accordingly (the withdraw function doesn't) and so we can't implement logic there
#   - all amounts in dollars only (no cents atm)

class Ledger:
    def __init__(self):
        self.posted_balances: Dict[int, int] = defaultdict(int)
        
        # A hold will have {acctID --> List} where List is tuple of:
        #   (expiresAt, holdId, amount) so that heapq can work off
        #   of the expiresAt for sorting
        # Since times are smallest to largest, we can store with positive
        #   expiresAt, so heapify([100, 200, 300, 150]) would sort to
        #   100, 150, 200, 300 as we popped off - if something expires at 200
        #   we know 100 and 150 will also be popped off, so this is the correct
        #   sorting approach / key
        self.holds_expiry: Dict[int, List[Tuple]] = defaultdict(list)
        self.holds: Dict[int, Dict[int, int]] = defaultdict(dict)
        self.holds_total: Dict[int, int] = defaultdict(int)
    
        
    def deposit(self, accountId: str, amount: int) -> None:
        # Just a very straightforward deposit
        self.posted_balances[accountId] += amount
        
    def withdraw(self, accountId: str, amount: int) -> bool:
        # How can I flush holds and check before withdraw without a timestamp?
        # self._flush_old_holds(accountId)
        if (self.posted_balances[accountId] < amount or 
                self.posted_balances[accountId] - self.holds_total[accountId] < amount):
            return(False)
        else:
            self.posted_balances[accountId] -= amount
            return(True)

    def _flush_old_holds(self, accountId: int, currTimestampMs: int) -> None:
        # self.holds_expiry[accountId][0] is "oldest" expiresAt
        # self.holds_expiry[accountId][0][0] is the actual time
        
        # Flush old and expired holds
        while self.holds_expiry[accountId] and self.holds_expiry[accountId][0][0] <= currTimestampMs:
            # oldest_hold: Tuple(expiresAt, holdId, amount)
            expires_at, hold_id, amount = heapq.heappop(self.holds_expiry[accountId])
            
            # it may have been removed during release_hold
            #   if this exists we can remove from 
            #   holds_total
            if hold_id in self.holds[accountId]:
                del self.holds[accountId][hold_id]
                self.holds_total[accountId] -= amount
            
        
    def place_hold(self, accountId: str, amount: int, holdId: str, timestampMs: int, ttlMs: int) -> bool:
        if ttlMs < 0:
            raise ValueError("Bad ttlMs - can't be negative")
        if timestampMs < 0:
            raise ValueError("Bad timestampMs - can't be negative")
        
        # Since we are affecting available_balance, need to expire old holds
        self._flush_old_holds(accountId, timestampMs)
        if self.posted_balances[accountId] - self.holds_total[accountId] < amount:
            return(False)
            
        # expires when current timestamp and ttlMs (time to live) are reached
        expires_at = timestampMs + ttlMs
        hold_info = (expires_at, holdId, amount)

        heapq.heappush(self.holds_expiry[accountId], hold_info)
        
        if holdId in self.holds[accountId]:
            raise ValueError(f"Hold already exists for {holdId} in {accountId}")
        
        self.holds[accountId][holdId] = amount
        self.holds_total[accountId] += amount
        return(True)
        
        
        
    def release_hold(self, accountId: str, holdId: str) -> bool:
        if holdId in self.holds[accountId]:
            self.holds_total[accountId] -= self.holds[accountId][holdId]
            del self.holds[accountId][holdId]
            return(True)
        
        return(False)
                        
    def capture_hold(self, accountId: str, holdId: str) -> bool:
        if holdId not in self.holds[accountId]:
            raise ValueError(f"No hold exists for {accountId}, {holdId}")
            
        hold_amount = self.holds[accountId][holdId]
        released = self.release_hold(accountId, holdId)
        if not released:
            raise ValueError(f"Something went wrong for {accountId}, {holdId}")
        
        # no longer being held
        self.posted_balances[accountId] -= hold_amount
        return(True)

    def posted_balance(self, accountId: str, timestampMs: int) -> int:
        self._flush_old_holds(accountId, timestampMs)
        return(
            self.posted_balances[accountId]
        )
        
    def available_balance(self, accountId: str, timestampMs: int) -> int:
        self._flush_old_holds(accountId, timestampMs)
        return(
            self.posted_balances[accountId] - self.holds_total[accountId]
        )

    # def begin(self) -> None
    # def commit(self) -> bool
    # def rollback(self) -> bool