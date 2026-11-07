---
title: Task Execution Engine
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You're implementing a task execution engine for ML workflows

Each task may depend on other tasks, and a task cannot execute until all its dependencies have completed

### Requirements
```python
class TaskExecutor:
    def __init__(self, tasks: dict[str, list[str]]):
        pass

    def get_ready_tasks(self) -> list[str]:
        pass

    def complete(self, task_id: str) -> None:
        pass

    def is_finished(self) -> bool:
        pass
```

1. `tasks` maps each task ID to a list of dependencies.
```
tasks = {
    "ingest": [],
    "validate": ["ingest"],
    "train": ["validate"],
    "evaluate": ["train"],
    "publish": ["evaluate"],
    "metrics": ["validate"]
}
```

2. `get_ready_tasks()`
Returns all tasks that:
- Have all their dependencies completed.
- Have not already been returned by a previous get_ready_tasks() call.
- Have not been completed.
Once returned, a task is considered in progress.

The result can be in any order.

3. `complete(task_id)`

Marks a previously returned task as completed.
- A task cannot be completed twice.
- A task that hasn't been returned by get_ready_tasks() cannot be completed.
- Invalid completion requests should raise ValueError.
4. is_finished()

Returns True only when all tasks have completed.
Example
```
executor = TaskExecutor({
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B", "C"]
})

assert executor.get_ready_tasks() == ["A"]
assert executor.get_ready_tasks() == []

executor.complete("A")

assert set(executor.get_ready_tasks()) == {"B", "C"}

executor.complete("B")
assert executor.get_ready_tasks() == []

executor.complete("C")
assert executor.get_ready_tasks() == ["D"]

executor.complete("D")
assert executor.is_finished() is True
```

Another example

```python
executor = TaskExecutor({
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B", "C"]
})

# Scheduler asks for available work
ready = executor.get_ready_tasks()  # ["A"]

# Scheduler dispatches A to an external worker
# ... some time passes ...

# Worker reports that A finished
executor.complete("A")

# Scheduler asks for more work
ready = executor.get_ready_tasks()  # ["B", "C"]

# Both B and C are dispatched
# C finishes before B
executor.complete("C")

ready = executor.get_ready_tasks()  # []

# B eventually finishes
executor.complete("B")

ready = executor.get_ready_tasks()  # ["D"]
```

#### Constraints
- Up to 100,000 tasks.
- Up to 500,000 dependency relationships.
- Assume all dependencies reference existing tasks.
- Assume the dependency graph is acyclic.
- Single-threaded execution for now.
- Optimize for efficient repeated calls to get_ready_tasks().


### Initial Thoughts
So this is a DAG problem mixed in with state controls. We essentially need to keep track of nodes in the DAG that are TODO, running, and completed

In a typical topological sort setup there's no time component involved, so in here we would need to essentially figure out what that future time component would be. For now if it's a big loop that's fine

Implement the three logical states you identified:
- TODO: Task hasn't been dispatched
- RUNNING: Task was returned by `get_ready_tasks()` but hasn't been completed
- COMPLETED: Task was explicitly completed

```python
from enum import Enum
class Status(Enum):
    TODO = 1
    RUNNING = 2
    COMPLETED = 3
class TaskExecutor:
    def __init__(self, tasks: dict[str, list[str]]):
        self.nodeToDeps = {}
        self.depToNodes = {}
        self.state = {}
        self.ready = []
        for task, deps in tasks.items():    
            if task not in self.nodeToDeps:
                self.nodeToDeps[task] = set()
            for dep in deps:
                if dep not in self.depToNodes:
                    self.depToNodes[dep] = set()
                self.depToNodes[dep].add(task)
                self.nodeToDeps[task].add(dep)
            self.state[task] = Status.TODO
            if len(deps) == 0:
                self.ready.append(task)
                del self.nodeToDeps[task]
    def get_ready_tasks(self) -> list[str]:
        for readyTask in self.ready:
            self.state[readyTask] = Status.RUNNING
        resp = self.ready.copy()
        self.ready = []
        return(resp)
    def complete(self, task_id: str) -> None:
        if task_id not in self.state or self.state[task_id] != Status.RUNNING:
            raise ValueError(f"{task_id} is bad")
            return(None)
        del self.state[task_id]
        if task_id in self.depToNodes:
            for upstreamTask in self.depToNodes[task_id]:
                self.nodeToDeps[upstreamTask].remove(task_id)
                if len(self.nodeToDeps[upstreamTask]) == 0:
                    self.ready.append(upstreamTask)
                    del self.nodeToDeps[upstreamTask]
            del self.depToNodes[task_id]
    def is_finished(self) -> bool:
        return(
            len(self.state) == 0
        )

executor = TaskExecutor({
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B", "C"]
})
```