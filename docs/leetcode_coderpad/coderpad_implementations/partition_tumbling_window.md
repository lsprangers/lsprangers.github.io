---
title: Partition Tumbling Window
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Initially set a window size for tumbling windows - `60`

Get a number of events streamed in with `(ts, data)` semantics

Watermarks distinguish when a specific partition will stop sending in data - it's guaranteed there's no further events coming in after that. Furthermore, there's a global watermark, which should be considered the minimum of all other partitions. No event can come in behind this timestamp

### Initial Thoughts, Questions
- Events can happen in any order, it's not guaranteed to be sorted so we want to keep a min heap of all events that have occurred, and we know there aren't any events older than a global watermark so we can emit these as that API is called
- Watermark setting is the majority of edge cases. Emitting events is just popping off of heaps as they're less than global watermark
- Events should be removed according to global watermark, and shouldn't be evicted based on partition based watermark. There's a potential for a specific partition to go far beyond the global standard, but we are supposed to emit based on global watermark
    - Is this really true? This seems a bit odd


### Implementation
```python

class EventIngestor:
    def __init__(self, partitions: List[str], window_size: int):
        self.event_to_partition = {partition: [] for partition in partitions}
        self.partition_to_watermark = {partition: 0 for partition in partitions}
        self.global_watermark = [0, 0]
        self.window_size = window_size
    
    def ingest(self, partition: str, ts: int, data: dict[str, int]) -> None:
        # pusb to heap
        heapq.heappush(self.event_to_partition[partition], (ts, data))


        return
    
    def advance_watermark(self, partition: str, ts: int):
        self.partition_to_watermark[partition] = watermark
        self.global_watermark = min(self.partition_to_watermark.values())
    
    def emit_events(self):
        # is this called somewhere? We should we running this during advance watermarks during [0, 121 ege cases]

        # no need to partition by events, just append by timestamp
        resp = []
        for partition_key, partition_heap in self.event_to_partition.items():
            while partition_heap and self.global_watermark[0][0] <= partition_heap[0][0] < self.global_watermark[0][0] + self.window_size:
                ts, data = partition_heap.pop()
                resp.append(data)
        
        # we don't want to update to self.global_watermark[1] - this is being called by a separate process so we just track last gloval watermark and can emit events per call. This call with [0, 121] would emit events for [0, 59), but it's definitely a large edge case
        self.global_watermark[0] = self.global_watermark[0] + self.window_size
```

## Systems Design


### High Level requirements


#### API Surface

#### Clarifying Questions
Questions around implementations, strict vs approximate, and anything that would kill any choices made in future

#### System Constraints
Summarize system constraints in your own words
- QPS 
- latency SLO    
- consistency requirements
- failure tolerance

#### Identify Core Challenges
What makes this problem hard in distributed manner (MOST IMPORTANT PART)
- Distributed correctness (no double allow)
- Routing / management
- Data structure
- Scale + latency
- Failure behavior
- single-writer vs linearizable store
- availability vs consistency
- data plane vs control plane

#### Starter Architecture
Distributed compatible, but high level components and algorithms, focus on partitioning and scaling, not frontend or anything. Some data structure information is OK, specifically ones that relate to the core problem.

Components + Flow + network, partition, and some data structures

#### Real Architecture
Now you make in depth choices on literally everything, and draw the entire thing out

#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture
