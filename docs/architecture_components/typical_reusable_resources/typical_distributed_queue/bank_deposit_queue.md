---
title: In Memory Bank Deposit Priority Queue
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Bank Deposit Priority Queue
- This is an implementation of multiple requests being sent using timestamps that have withdraws, deposits, and cashback examples
- This is useful to showcase how priority queue's can be used in certain situations, such as using timestamps to balance accounts

## Setup
- balances: list of ints, 1-indexed
- requests: list of tuples (action, timestamp, account_id, amount)
- For a withdraw request, you need to process a cashback amount of 2% exactly 24 hours from the withdraw
- Timestamps are integer timestamps, may overlap


```python
import time

def now():
    return int(time.time())

def process_requests(balances, requests):
    # implement

def run_scenario(scenario_num, balances, requests, expected_balances, expected_results):
    try:
        final_balances, results = process_requests(list(balances), requests)
        balances_ok = final_balances == expected_balances
        results_ok = results == expected_results
        print(f"Scenario {scenario_num}: {'PASS' if balances_ok and results_ok else 'FAIL'}")
        if not balances_ok:
            print(f"  Expected balances: {expected_balances}, got: {final_balances}")
        if not results_ok:
            print(f"  Expected results: {expected_results}, got: {results}")
    except Exception as e:
        print(f"Scenario {scenario_num}: ERROR - {e}")

if __name__ == "__main__":
    t0 = now()

    # 4 Easy/Normal Scenarios
    scenarios = [
        # 1. Simple deposit and withdraw
        (
            [100, 200],
            [("deposit", t0, 1, 50), ("withdraw", t0+1, 1, 100)],
            [50, 200],
            ["OK", "OK"]
        ),
        # 2. Overdraw attempt
        (
            [100],
            [("withdraw", t0, 1, 150)],
            [100],
            ["Overdraw"]
        ),
        # 3. Invalid account
        (
            [100],
            [("deposit", t0, 2, 50)],
            [100],
            ["Invalid account"]
        ),
        # 4. Cashback processed after 24h
        (
            [100],
            [("cashback", t0, 1, 10)],
            [110],
            ["OK"]
        ),

        # 6 Edge Cases
        # 5. Withdraw after cashback arrives
        (
            [100],
            [("cashback", t0, 1, 50), ("withdraw", t0+24*60*60, 1, 150)],
            [0],
            ["OK", "OK"]
        ),
        # 6. Multiple cashbacks, overlapping timestamps
        (
            [100],
            [("cashback", t0, 1, 10), ("cashback", t0+1, 1, 20), ("withdraw", t0+24*60*60+1, 1, 130)],
            [0],
            ["OK", "OK", "OK"]
        ),
        # 7. Withdraw before cashback arrives (should fail)
        (
            [100],
            [("cashback", t0, 1, 50), ("withdraw", t0+1, 1, 150)],
            [100],
            ["OK", "Overdraw"]
        ),
        # 8. Deposit, withdraw, cashback, withdraw after cashback
        (
            [100],
            [("deposit", t0, 1, 50), ("withdraw", t0+1, 1, 100), ("cashback", t0+2, 1, 20), ("withdraw", t0+2+24*60*60, 1, 70)],
            [0],
            ["OK", "OK", "OK", "OK"]
        ),
        # 9. Invalid action
        (
            [100],
            [("invalid", t0, 1, 10)],
            [100],
            ["Invalid action"]
        ),
        # 10. Withdraw, cashback scheduled after all requests (should be ignored)
        (
            [100],
            [("withdraw", t0, 1, 50), ("cashback", t0+1000000, 1, 999)],
            [50],
            ["OK", "OK"]
        ),
    ]

    for i, (balances, requests, expected_balances, expected_results) in enumerate(scenarios, 1):
        run_scenario(i, balances, requests, expected_balances, expected_results)
```