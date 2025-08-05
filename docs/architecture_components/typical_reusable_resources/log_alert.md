---
title: In Memory Log Alerting System
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Log Alerting System
Problem

Design a system that ingests log messages with a timestamp, and alerts if more than K "ERROR" messages occur in the past W seconds (sliding window).

Expose:

    log(timestamp: int, level: str) — level can be "INFO" or "ERROR"

    should_alert(timestamp: int) -> bool — return True if more than K errors seen in last W seconds

Constraints

    You may assume timestamps are increasing

    Use a sliding window with a deque

Parameters

    K = 3, W = 10

Test Case 1
system.log(1, "ERROR")
system.log(2, "INFO")
system.log(3, "ERROR")
system.log(4, "ERROR")
print(system.should_alert(5))  # True (3 errors in 10s)
system.log(15, "ERROR")
print(system.should_alert(15))  # False (window 5–15 has only 1 error)