---
title: In Memory Task Scheduler
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Task Scheduler
Problem

Design a task scheduler that allows adding tasks with:

    A timestamp at which the task should execute

    A priority, where lower numbers indicate higher priority

The system should support:

    schedule(timestamp: int, task_id: str, priority: int)

    run(current_time: int) -> List[str]: runs all due tasks up to current_time in correct order (by timestamp, then priority)

Constraints

    timestamp is in seconds

    No two tasks have the same (timestamp, task_id)

    You should return task IDs in order of execution

Test Case 1

scheduler.schedule(10, "task1", 2)
scheduler.schedule(5, "task2", 1)
scheduler.schedule(10, "task3", 1)
print(scheduler.run(5))   # ["task2"]
print(scheduler.run(10))  # ["task3", "task1"]
print(scheduler.run(20))  # []