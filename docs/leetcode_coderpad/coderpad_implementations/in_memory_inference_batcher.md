---
title: In Memory Inference Batcher
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You're building an inference gateway that receives requests for multiple machine learning models
To improve GPU utilization, the gateway groups requests into batches before dispatching them to inference workers
However, the gateway must balance batching efficiency against request latency
Your task is to implement an in-memory `InferenceBatcher`


1. `submit()` adds an inference request to the pending queue
- Each request has a unique request_id, a model_id, and an arrival timestamp
- Requests targeting different models must never be combined into the same batch
2. Batch creation
- A batch becomes eligible for dispatch when either:
    - It contains `max_batch_size` requests
    - Its oldest pending request has waited at least `max_wait_ms`
- A batch cannot exceed `max_batch_size`.
- Requests for the same model must be processed in FIFO order
3. Polling
- `poll(now_ms)` returns all batches currently eligible for dispatch
- Each returned tuple contains `(model_id, [request_id_1, request_id_2, ...])`

Once dispatched, requests must be removed from the pending queues and never returned again. The order of batches across different models doesn't matter. The order of requests within a batch does

### Template
```python
class InferenceBatcher:
    def __init__(
        self,
        max_batch_size: int,
        max_wait_ms: int
    ):
        pass

    def submit(
        self,
        request_id: str,
        model_id: str,
        timestamp_ms: int
    ) -> None:
        pass

    def poll(
        self,
        now_ms: int
    ) -> list[tuple[str, list[str]]]:
        pass
```

### Example
```python
batcher = InferenceBatcher(
    max_batch_size=3,
    max_wait_ms=10
)
batcher.submit("r1", "fraud", 0)
batcher.submit("r2", "fraud", 2)
batcher.submit("r3", "risk", 3)
assert batcher.poll(5) == []
batcher.submit("r4", "fraud", 6)
assert batcher.poll(6) == [["fraud", ['r1', 'r2', 'r4']]]
assert batcher.poll(12) == []
assert batcher.poll(13) == [["risk", ['r3']]]
```

### Constraints
- Up to 100,000 requests
- Up to 1,000 distinct models
- poll() may be called frequently
- Timestamps are monotonically nondecreasing across calls to submit() and poll()
- Assume a single-threaded implementation initially
- No actual model inference, networking, or background workers are required

### Initial Thoughts, Questions
Need to quickly find which batches are ready to go, meaning which batches have a minimum timestamp older than current timestamp - max wait, or which batches have a total number of requests. If we track the current batch for every `model_id`, then on each submit we can check if the size is ready to go to `ready_batches`

For timing, on each poll we could iterate over every single `model_id` and get the current batch, and look at the first (earliest) entry. This would be $O(m)$, and we would end up looping over a large number of unnecessary models. If we track the earliest timestamp for each model in a sorted data structure we could iterate over it until we reach a timestamp that's no longer old enough to pop off. If we take this route, we may need to delete a batch in the middle of the sorted data structure if it becomes large enough. That is typically $O(n)$ in a heap, because we wouldn't know the exact index. We could track current batch versions so that we don't have to do this


### Implementation
```python
import heapq
from collections import defaultdict
class InferenceBatcher:
    def __init__(
        self,
        max_batch_size: int,
        max_wait_ms: int
    ):
        self.maxBatchSize = max_batch_size
        self.maxWaitMs = max_wait_ms
        self.batches = defaultdict(list)
        self.batchVersion = defaultdict(int)
        self.batchHeap = []
        self.readyBatches = []
    def submit(
        self,
        request_id: str,
        model_id: str,
        timestamp_ms: int
    ) -> None:
        self.batches[model_id].append(request_id)
        if len(self.batches[model_id]) == self.maxBatchSize:
            self.readyBatches.append([model_id, self.batches[model_id]])
            self.batches[model_id] = []
            self.batchVersion[model_id] += 1
        elif len(self.batches[model_id]) == 1:
            heapq.heappush(
                self.batchHeap,
                [timestamp_ms, self.batchVersion[model_id], model_id]
            )
    def poll(
        self,
        now_ms: int
    ) -> list[list[str, list[str]]]:
        # TODO: This can just be a queue since the ones coming in are 
        #   guaranteed monotonically increasing
        while self.batchHeap and (now_ms - self.batchHeap[0][0]) >= self.maxWaitMs:
            firstTs, thisBatchVersion, model_id = heapq.heappop(self.batchHeap)
            if thisBatchVersion == self.batchVersion[model_id]:
                self.readyBatches.append([model_id, self.batches[model_id]])
                self.batchVersion[model_id] += 1
                self.batches[model_id] = []
        resp = self.readyBatches
        self.readyBatches = []
        return(resp)

batcher = InferenceBatcher(
    max_batch_size = 5,
    max_wait_ms = 5
)
for i in range(10):
    batcher.submit(f"r{i}", "fraud", i)
batcher.poll(11)
batcher.submit("r12", "fraud", 12)
batcher.poll(18)
batcher.submit("r20", "fraud", 20)
batcher.submit("r21", "credit", 21)
batcher.submit("r22", "credit", 22)
batcher.poll(30)

>>> batcher = InferenceBatcher(
...     max_batch_size = 5,
...     max_wait_ms = 5
... )
>>> for i in range(10):
...     batcher.submit(f"r{i}", "fraud", i)
...
>>> batcher.poll(11)
[['fraud', ['r0', 'r1', 'r2', 'r3', 'r4']], ['fraud', ['r5', 'r6', 'r7', 'r8', 'r9']]]
>>> batcher.submit("r12", "fraud", 12)
>>> batcher.poll(18)
[['fraud', ['r12']]]
>>> batcher.submit("r20", "fraud", 20)
>>> batcher.submit("r21", "credit", 21)
>>> batcher.submit("r22", "credit", 22)
>>> batcher.poll(30)
[['fraud', ['r20']], ['credit', ['r21', 'r22']]]
>>>
>>>
```

## Systems Design
Design a system to handle inference serving with batching and max time

### Requirements
- Peak traffic: 10,000 RPS
- Latency target: p99 < 100 ms
- Models: 30+
- Availability: 99.95%


#### Model characteristics
- Mix of CPU-based tabular models and GPU-based neural networks
- Models are independently versioned and deployed
- Some models receive substantially more traffic than others
- Requests are synchronous and require a response
- Model serving should scale horizontally

To discuss
1. Serving stack: Ray Serve vs Triton vs custom FastAPI/ECS services
2. Request routing: Model identification, version selection, and replica discovery
3. Batching: Where batching happens, queue ownership, and per-model isolation
4. GPU execution: Device placement, memory utilization, and model concurrency
5. Reliability: Request deadlines, retries, backpressure, and degraded service
6. Performance: p50/p95/p99 latency, throughput, batching efficiency, and autoscaling
But I don't want to hand you the architecture. This should be your design