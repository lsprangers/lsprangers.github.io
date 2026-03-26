---
title: Merge K Sorted Streams
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You are given K sorted iterators, each producing integers in ascending order.
Each iterator may be very large or infinite, so you cannot materialize them fully.Implement a function that returns a single iterator that yields all values in sorted order

### Example
```python
#Input:
def merge_k_sorted(iterators: List[Iterator]) -> Iterator:
    return iterators

# Implement:
class Iterator:
    def has_next(self) -> bool:
        return(0)
    def next(self) -> int:
        return(0)
```

### Constraints
$K$ is number of iterators

- $K$ can be up to 10,000
- Total elements across all iterators can be very large
- Each individual iterator is sorted
- You may only call `next()` if `has_next()` is true
- Memory should be $O(K)$, not proportional to total elements

### Requirements
- Time complexity should be optimal
- Output must be lazily evaluated (iterator-based)
- No preloading entire iterators

### Initial Thoughts, Questions
- Are the inputs are sorted in the same way the output should be?
- `merge_k_sorted()` returns an iterator, and that iterator will most likely have some sort of async `yield` statement, so that as it's called we're expected to merge in results from the sorted iterators input
- Are the sorted inputs updated constantly too? Meaning is this a long running process, or are the inputs pre-defined and not updated?
- Upon each `next()` call to `merge_k_sorted` I need to somehow pick the smallest current element from each of the iterators and return that
    - I can pre-load those elements if the iterators are never updated
- I need to somehow keep track of the ordering of the elements in the iterator
    - I need to quickly access the smallest element (assuming ordering is smallest here, can be max too)
    - I need to return that smallest element
    - Then I need to ingest the next element from the iterator that had the previous smallest element, and insert that into my ordered object
- This mostly seems like holding a min-heap (if smallest), where the min-heap itself will be sorted based on the value, and have some reference back to the iterator that it was apart of `[1-k]`
    - When I pop off the smallest element, I need to push the element from that iterator onto the min-heap
- My implementation would have
    - $O(k)$ storage, with a single entry in the min-heap for each iterator $k$
    - $O(2 \times \log k)$ time complexity as removing smallest and inserting next item are both $O(\log k)$
    - Lazily evaluated, no pre-loading **entire** iterators
- Edge cases and gotchas
    - Need to check each iterator has a next, if it doesn't just ignore it then. No need to check further (unless it's continuously updated)
    - If there are duplicate values, how do I separate them or know which one to return? Merging them I would assume I just pick whichever one, which means based on min-heap it will be the one with the smallest iterator index
    - The values have some sort of comparison logic that's implemented on them?

### Implementation
General thought is to implement a new class, treat `Iterators` as a black box, and ensure new class implements something like:
```
merged = merge_k_sorted(iterators)
merged.has_next()
merged.next()
```

```python
# This is given, assume it's "good" - "Each input iterator already implements has_next() / next() and is treated as a black box"
class Iterator:
    def has_next(self) -> bool
    def next(self) -> int

class MergedIterator():
    # Once MergedIterator is instantiated, calling next and has_next can
    #   be done without returning something here. THis is strictly for 
    #   passing inputs in  
    def __init__(self, iterators: List[Iterator]):
        # use heapq operations EVERYWHERE
        # (val, iterator_reference)
        self.min_heap = []
        self.iterators = iterators
        # fill up initially
        for idx, iterator in enumerate(self.iterators):
            if iterator.has_next():
                heapq.heappush(self.min_heap, (iterator.next(), idx))

    def has_next(self) -> bool:
        return(len(self.min_heap) > 0)
    
    def next(self) -> int:
        # Just a guardrail
        if not self.has_next():
            raise ValueError("Iterators Empty")

        val, iter_idx = heapq.heappop(self.min_heap)
        # If it doesn't have next and is empty, just ignore it
        if self.iterators[iter_idx].has_next():
            heapq.heappush(self.min_heap, (self.iterators[iter_idx].next(), iter_idx))
        
        return(val)
    
merged_iterator = MergedIterator(iterators)
if merged_iterator.has_next():
    yield merged_iterator.next()

```

## Systems Design
Streaming + ML Design Question
- You now have K sorted streams of model outputs (e.g., per-shard inference results), and you need to:
    - Merge them in order (as above)
    - Compute rolling top-K results over the last $N$ seconds
    - Serve this in near real time to downstream consumers

### High Level requirements

#### Constraints
- Streams are high volume
- Eventual consistency is acceptable
- Memory must be bounded
- Queries ask for “top-K in last N seconds”

#### API Surface

#### Clarifying Questions
- What is the typical volume of model outputs? What is the typical volume over $N$ seconds?
    - Volume: `~5–10 million` events per minute total across all streams
- Can $N$ change over queries, or is $N$ a fixed parameter?
    - $N$ fixed at 60 seconds
- How many queries per second are coming in from clients asking about top $N$?
    - ~1,000 QPS querying “top-K over last 60s”.
- How large is $K$, is $K$ fixed, or is it changing for each query?
    - Small and fixed — assume K $\lte$ 100

#### System Constraints
In total, we need to keep a sorted data structure receiving up to 10 million events per minute, we are going to end up receiving about 1,000 queries per second querying for these `top-k` results, and $k$ is going to be a fixed number less than 100. Accepting hundreds of thousands requests every 10 seconds in a continuous fashion means that keeping our internal data structure will require extremely fast update speeds, and then the query layer needs to work off this data structure to continuously serve queries. Eventual consistency is OK and so accepting a new event and inserting into the data structure isn't strictly required while also serving queries. Most modern day servers can handle 1,000 queries per second alone, but handling millions of ingestion events each minute while handling query events will be a marked challenge.

- Is fault tolerance a large issue here? If the system goes down can we boot things back up and wait for $N$ seconds, or do we need to have this data stored somewhere to continue serving in face of server outage?
    - If a node goes down, it is acceptable to rebuild state by replaying events for up to N seconds
    - We do not require zero-loss recovery, but we do want the system to converge quickly
    - Storing raw events durably (e.g., in a log) is acceptable; storing full in-memory aggregates synchronously is not required

#### Starter Architecture
- Handling ingestion + ordering is the hardest part:
    - Redis ZSETS will help with a highly scalable component with ordering, but the model inferences may have duplicates. We can handle this by storing the model shard index alongside the score, and potentially a timestamp
        - This method should be OK to scale to millions of ingestion operations per minute, and can also handle thousands of queries per minute. Especially with fixed parameters of $K$ and $N$ this is a pretty straightforward solution, and if Redis goes down we can simply boot it back up and continue ingesting for $N$ seconds
        - Redis ZSETS with read replica would help the high availability in case a node goes down
        - This architecture means we are dependent on a centralized redis node / cluster, which may be suboptimal. At this point I'd stop to ask if the architecture should continue with this, or if we want to look at implementing something with less dependencies.
    - ZSET schema:
        - (score, timestamp, shard_index)
        - This allows us to differentiate any possible score from any other one, including if a shard sends out multiple similar. Timestamps are easy to sort by too, but this means we would return the most recent value before a longer value in our top-k return set
    - Top-K semantics:
        - To actually ensure we only return the top-k, I don't remember the exact commands but with Redis ZSETS there are ways to add in new data given the schema above, and to drain older results
        - The removal of results would need to be done by timestamp > `curr - 60` or some sort
            - This is a potential bottleneck as this is called during active commands to redis, and doesn't run as a background process on the cluster. Therefore we may be returning somewhat stale data inbetewen add calls
        - Adding in new data will place anything with higher score on top, and then for queries we would just retrieve the actual data with a certain `score[0:60]` type of query which redis can handle
    - Most of these choices have time complexities similar to local based min-heaps
- The query layer would be served by a set of stateless, horizontally scalable API's that simply all query redis and return results
- The ingest layer is also a set of horizontally scalable API's. There should be a queue or broker in the middle the inference outputs push to, and that will act as a durable log of sorts to handle data as it's ingested and then inserted into redis
    - Once a message is committed into Redis, we can mark it as read from a queue or increment offset for broker
- In this way we have a scalable ingestion layer + query layer backed by Redis utilizing ZSETS to handle data ordering, pruning, and adding in a eventually consistent way

Walked through [Redis ZSets for Priority Queue's](/docs/architecture_components/databases & storage/Redis/ZSETS.md)

#### Real Architecture
Now you make in depth choices on literally everything, and draw the entire thing out

#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture


## Second Attempt
Implement
```python
class MergedIterator:
    def __init__(self, iterators):
        ...
    def has_next(self) -> bool:
        ...
    def next(self) -> int:
        ...
```

Each underlying iterator supports:
```python
has_next() -> bool
next() -> int
```

Your `MergedIterator` should return all values across all iterators in globally sorted order.

Interview expectations:
- clarify assumptions
- give approach
- complexity
- code
- edge cases

### Implementation
```python
from typing import List

class SortedIterator:
    def __init__(self):
        self.iterator = ...
    
    def has_next(self) -> bool:
        ...
    
    def next(self) -> int:
        ...
    

# Assumptions:
#   - Once a sorted iterator `has_next()` returns `False`, it's permanently exhausted
import heapq

class MergedIterator:
    def __init__(self, iterators: List[SortedIterator]):
        # reference it, make available
        self.iterators = iterators
        self.next_vals = []
        for _iter in self.iterators:
            if _iter.has_next():
                heapq.heappush(self.next_vals, (_iter.next(), _iter))

    def has_next(self) -> bool:
        return(len(self.next_vals) > 0)

    def next(self) -> int:
        if not self.has_next():
            raise StopIteration("Nothing left to exhaust")

        min_iter, min_iter_val = heapq.heappop(self.next_vals)
        if min_iter.has_next():
            heapq.heappush(self.next_vals, (_iter.next(), _iter))
        
        return(min_iter_val)
```