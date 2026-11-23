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

## Real World Problem
Going to try and setup a real world implementation of a lightweight version of this based on a typical data engineering teams problem. A typical problem seen is that there are many upstream jobs that run before a global job, however those upstream jobs aren't always triggered in one single batch. This happens a lot when multiple upstream jobs write to a global parquet table in different partitions, and after the initial write there is some global ranking / process that needs to run over the entire table. If you blatantly run the G process for each of them there's a few issues:
- We recompute G many times, mostly unnecessarily
- There are concurrency issues 
    - t=0 U1 starts
    - t=2 U1 finishes
    - t=3 G starts
    - t=4 U2 starts
    - t=5 U2 finishes
    - t=6 G tries to finish, but it's delta version is older than the last committed one (from U2), so it fails with `ConcurrentException`

```
U1 -- 
     |
U2 --  --> G
     |
U3 --
```

In the above example U1 may get triggered once a day, U2 may get triggered once a week, and U3 on an ad-hoc fashion. The typical way to handle this would be put all of them in an airflow DAG, and start the DAG when any number of these needs to be started. The issue there is on the 7th day when both U1 and U2 are started, if they come at different times, like 8 and 8:01, then the global job runs twice

### Problem Statement
There needs to be a way to efficiently handle upstream and global job execution based on dependencies:
- All upstream jobs will need a global job to run after them
- A global job has 1:M upstream jobs
- ***If multiple upstream jobs overlap, they should only run their shared global job once all have finished***
- During a global job run, upstream jobs should wait

These jobs need to be queue'd up, dispatched, and sent for execution by a service or open source tooling configuration such as Airflow / Prefect

#### Airflow Try
Airflow initially looks promising, there are branches, some `if-then` logic we could apply as a node, and concurrency controls such as `max_active_runs`

In a perfect world we could setup all of the upstream items as nodes in a DAG and invoke them on some event, and we could continually call upstream nodes to run and they'd get scheduled if others are running

However, Airflow doesn't have a notion of updating a current runs configuration, and will simply just run a job based on whatever configurations it was sent in the initial API call. There's no native way to say "oh you're already running U2, run U1 as well before starting G"

A potential workaround would be having each of the U jobs as independent DAGs, and having them call a separate G DAG upon completion. In that way we can independently start each of the U jobs themselves, and each of them will call G. We can even set `max_active_runs=1` on the G DAG so that at any given time only 1 can be scheduled to run. This won't solve the requirement of having G execute only once based on the upstream jobs, it will simply queue up the G runs serially one after another and we'll be back to running G more times than necessary. Also it doesn't stop upstream jobs from running if G is currently running. Airflow removed `max_queued_runs_per_dag`, so there's no way to setup this architecture, you must either run G many times, or choose to run it just at a specific cadence

#### Postgres + API
This just turns into a job scheduler / event scheduler at the end of the day with specific requirements. Most of this just needs to be done with postgres tables / indexes that can efficiently determine if a job can run, along with handling transactions on updating state

Trade U1, U2, and U3 for A, B, and C

![Task Scheduler Setup](/img/task_scheduler_setup.png)

| Situation |Decision |
|------------|---------|
| Request A, nothing running	| Start A |
| Request B, A running	| Start B |
| A finishes, B running	| Queue G |
| B finishes	| G becomes eligible |
| Request C, G running	| Keep C queued |
| G finishes	| Start C |
---------------------------

There should be 4 tables:
- jobs described metadata about jobs
- job_dependencies just has upstream and downstream jobs for an ID
- job_executions has the actual execution metadata about a specific job, along with status
- outbox is the queue of jobs that need to be ran

```sql
jobs
----
job_id
name
execution_config       -- Databricks job ID, parameters, etc.

job_dependencies
----------------
job_id
upstream_job_id
downstream_job_id

job_executions
--------------
run_id
job_id
status                 -- QUEUED, RUNNING, COMPLETED, FAILED
lease_expires_at
requested_at
completed_at

outbox
------
run_id
execution_id
event_type
processed_at
```


Along with a few components:
- API handler, which just handles new job creation requests, and handles events like job run request
- Dispatcher polls the outbox and decides if a job is ready to run
- Postgres holds state
- Cleanup API / script / etc to go and check expired leases from potentially partitioned jobs that may just be dead / failed

##### Handler

##### Dispatcher
A job can run as long as none of its upstream or downstream jobs are running. A job can be queue'd in either scenario as long as an existing instance of itself isn't already queued

Pseudocode:
```python
def dispatch(execution):
    with postgres_transaction():
        job = get_job(execution.job_id)

        # Serialize decisions affecting the same
        # dependency graph.
        lock_dependency_group(job.id)

        if has_conflicting_active_execution(job.id):
            return  # Leave queued.

        claim_execution(execution.id)

    launch_job(execution)
```

##### Questions
- What handles a finish job request? Handler? It needs to update downstream jobs want to execute

```python
def complete(execution_id):
    with postgres_transaction():
        execution = mark_completed_once(execution_id)

        if execution.was_already_completed:
            return

        for downstream in get_downstream_jobs(execution.job_id):
            enqueue_or_coalesce(downstream)
```

- "The worker renews its execution lease while running." A spark job can't and shouldn't do this. I guess we should just use Databricks somehow to tell the current status of a job. How would we do this with native spark cluster?

- What are the indexes on the table so each of these decisions happens efficiently?