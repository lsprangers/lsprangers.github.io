---
title: Template
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building an in-memory ledger for account balances with support for:
- deposits / withdrawals
- transactional semantics (begin/commit/rollback)
- “holds” (pending debits) that expire
- and `available_balance` vs `posted_balance`

Design a class:
```python
class Ledger:
    def deposit(self, accountId: str, amount: int) -> None
    def withdraw(self, accountId: str, amount: int) -> bool

    def place_hold(self, accountId: str, amount: int, holdId: str, timestampMs: int, ttlMs: int) -> bool
    def release_hold(self, accountId: str, holdId: str) -> bool
    def capture_hold(self, accountId: str, holdId: str) -> bool

    def posted_balance(self, accountId: str, timestampMs: int) -> int
    def available_balance(self, accountId: str, timestampMs: int) -> int

    def begin(self) -> None
    def commit(self) -> bool
    def rollback(self) -> bool
```

### Semantics

#### Balances
- **posted_balance**: sum of completed deposits/withdrawals
- **available_balance**: posted_balance minus any active holds (pending debits)

#### Deposits / withdrawals
- **deposit**: always succeeds; increases posted
- **withdraw**: succeeds only if available_balance >= amount at time of call; decreases posted

#### Holds
A hold represents a pending debit (like a card authorization):
- `place_hold` succeeds only if available_balance >= amount at that time
- A hold has `(holdId, amount, expiresAt)` where expiresAt = timestampMs + ttlMs
- `release_hold` removes an active hold (no posted change)
- `capture_hold` converts an active hold into a posted withdrawal:
    - removes the hold
    - subtracts hold amount from posted

#### Expiration
When calling `posted_balance` or `available_balance` (and also when placing/capturing holds), the system should treat expired holds as inactive

You may assume timestamps for a given account are **non-decreasing** across calls

#### Transactions
`begin/commit/rollback` apply to all operations above
- `begin()` starts a transaction (can be nested)
- During a transaction, all operations should be “tentative”
- `commit()` persists the latest transaction layer into the next outer layer
- rollback() discards changes in the latest layer

If `commit()` or `rollback()` is called with no open transaction, return false

#### Complexity requirements
Aim for near $O(1)$ amortized per operation
Holds expiration should not require scanning all holds every time

### Example
```rust
L.deposit("A", 100)
L.place_hold("A", 30, "h1", t=0, ttl=10000)   # true
L.available_balance("A", 0)  -> 70
L.posted_balance("A", 0)     -> 100

L.capture_hold("A", "h1")    # true
L.posted_balance("A", 0)     -> 70
L.available_balance("A", 0)  -> 70
```


### Constraints


### Initial Thoughts, Questions
- Explain `expiresAt = timestampMs + ttlMs`
    - `timestampMs` = the time when the hold is created, in milliseconds since some reference (epoch or monotonic clock; doesn’t matter for the problem)
    - `ttlMs` = time-to-live, in milliseconds — how long the hold should remain active
    - `expiresAt` = the exact timestamp (ms) when the hold becomes inactive
    - So if you place a hold at time `1000` with `ttlMs=5000`, then e`xpiresAt=6000`
    - At `timestamps >= 6000`, that hold is expired and should no longer reduce available balance
- Are any API calls outside of a transaction immediately committed? If there was an API call without a transaction and a rollback() is called, do we remove the last API call? A better question is API + transaction1 + direct API call...if a rollback() is called do we remove direct API call or transaction1?
    - Operations outside any transaction are immediately committed
        - `rollback()` only affects the most recent open transaction layer
        - If there is no open transaction, `rollback()` returns false and does nothing
        - A direct API call after a committed block is not undone by rollback unless it was executed inside an open transaction
```scss
deposit(100)          # committed
begin()
withdraw(10)          # tentative
deposit(5)            # tentative
commit()              # now both tentative ops become committed
deposit(20)           # committed
rollback()            # false (no open tx), does not undo deposit(20)
```
- Are transactions considered strictly ordered, or are there ID's associated with them?
    - Transactions are strictly ordered by call sequence
    - There are no transaction IDs



### Implementation
- Storing monetary amounts via tuples - Dollars would be `BIG_INT` outside of python, cents just `INT`
- Transactions can be held on a stack where a new transaction gets `push` onto stack, and a commit `pop` one off
- Holds themselves should be stored in a priority queue based on `expiresAt`
    - This priority queue will get drained during any action that checks `available_balance`, as holds directly affect only this part
    - Holds should also be stored in a dictionary by their `holdId` for $O(1)$ access
    - Any `capture_hold` call will focus on `expiresAt` and time management
- Always handle time based on parameters passed into API

```python

```