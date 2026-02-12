---
title: Topic Trends
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building a system that tracks trending topics. Each topic has a name and a numeric score. You must design a structure that supports these operations:
- `add(topic: str, score: int)`
    - If topic doesn't exist, insert it with the given score
    - If it already exists, increase it's score by the given amount
- `top(k: int)` 
    - Return top k topics with the highest score, in descending order
    - If scores tie, return topics in lexicographical order
- `reset(topic: str)`
    - Reset topics score to 0
    - Topic exists, but shouldn't rank above any topics with positive score

You may assume:
- There can be up to $10^5$ operations
- Topic names are strings
- `top(k)` may be called frequently
- `add` and `reset` may interleave arbitrarily with top


### Example


### Constraints


### Initial Thoughts, Questions
- If we use priority queue, then
    - `add` is $O(\log n)$ for insert, and worst case $O(n \times log n)$ for update
        - If the score we need to update is at the "bottom", i.e. 0, we need to pop off everything before it into `helper_queue`, $O(n)$, update the score, and then add all of that back into base priority queue `base_queue`
        - After popping off each insertion into `helper_queue`, which is $O(n \ times 1)$ work at worst, inserting each of the $n$ back into `base_queue` takes $O(\log n)$ effort
    - `top` would be $O(k \times \log n)$
        - We pop off $k$ terms into `helper_queue`, inserting them back in is $k$ push of $O(\log n)$ effort
    - `reset` would be similar to updating add as we need to go find the topic, update it's score, and then push everything back to `base_queue`
- We can use a combination of priority queue and hash table here
    - For each entry, we keep track of it's current score in hash table `curr_score: Dict[str, int]`
    - Adding a net new topic means adding it to `curr_score` and pushing onto `base_queue` which would be $O(1) + O(\log n)$ time
    - Updating a topic would become 
        - $O(1)$ updating `curr_score`
        - $O(\log n)$ pushing the updated topic into `base_queue`
        - Means we need to push in `(score, topic_name)` tuple into `base_queue`
            - We may need to also hold onto some sort of version for each score `(score, topic_name, version)`
            - Hold onto curr version in `curr_score: Dict[str, (int, int)]` so that for each new update via add, we increment this version as well - this is all needed to move past items in `top k`, i.e. drain queue and invalidate, for top k calls
    - For each `top` call, we then need to continuously pop off of `base_queue` and check each item against `curr_score` dict to check if it's the latest score or not
        - Time complexity here is $O(K)$ where $K$ is number of items we pop off including invalid data points, checking against `curr_score` is $O(1)$
        - After draining, we do need to hold onto valid entries in `helper_queue` and push them back on for $O(k \times \log n)$ similar to previous time
    - `reset` is then just a specific type of update where we increment version and update score to 0
- Given that `top` may be called frequently, there's really no difference between pure priority queue and priority queue + hash map, but storing all of the operations and current state would certainly have some space effect
    - Worst case we'd store all operations in `base_queue` until it's drained, but `top` is called frequently so it'd drain frequently
    - `add` and `reset` are intermingled with `top` so it'd be ideal to not have those block nearly as much
 
Walked through [Redis ZSets for Priority Queue's](/docs/architecture_components/databases & storage/Redis/ZSETS.md)

### Implementation
```python
from collections import defaultdict
from typing import Dict, Tuple
import heapq

# We can DRY some things out with add and update, but I didn't want to go down that
#   rabbit hole during this imlpementation - there's definitely a good case for that though

class trendingTopics:
    def __init__(self):
        # intentionally don't use defaultdict, check everywhere
        #   topic --> (score, curr_version)
        self.curr_records: Dict[str, (int, int)] = {}
        self.prio_q = []
    
            
    def add(self, topic: str, score: int) -> None:
        if topic not in self.curr_records.keys():
            self.curr_records[topic] = (score, 0)
            heapq.heappush(self.prio_q, (-score, topic, 0))
            return
        
        curr_score = self.curr_records[topic][0]
        curr_version = self.curr_records[topic][1]
        new_score = curr_score + score
        new_version = curr_version + 1
        
        self.curr_records[topic] = (new_score, new_version)
        
        # in future, we can check curr_version + 1 against curr_records to
        #   ensure it's latest value
        # if we only use (new_score, topic), and the scores are the same, then 
        #   it may be a bad edge case
        # max queue so negative ONLY FOR PRIO Q
        heapq.heappush(self.prio_q, (-new_score, topic, new_version))
        return
    
    def top(self, k: int) -> None:
        if len(self.curr_records) < k:
            raise ValueError(f"We don't have {k} topics")

        resp = []
        helper_q = []
        while self.prio_q and len(resp) < k:
            curr = heapq.heappop(self.prio_q)
            # check versions
            curr_neg_score = curr[0]
            curr_topic = curr[1]
            curr_version = curr[2]
            # if is valid latest, drain
            if curr_version == self.curr_records[curr_topic][1]:
                resp.append(curr_topic)
                helper_q.append((curr_neg_score, curr_topic, curr_version))

        # regardless of errors or not, push valid ones back
        while helper_q:
            heapq.heappush(self.prio_q, helper_q.pop())
            
        if len(resp) < k:
            raise ValueError(f"We don't have {k} current topics")
        
        return(resp)
    
    def reset(self, topic: str) -> None:
        if topic not in self.curr_records.keys():
            raise ValueError(f"{topic} not in current records can't reset")
        
        curr_score = self.curr_records[topic][0]
        curr_version = self.curr_records[topic][1]
        new_score = 0
        new_version = curr_version + 1
        
        self.curr_records[topic] = (new_score, new_version)
        
        # in future, we can check curr_version + 1 against curr_records to
        #   ensure it's latest value
        # if we only use (new_score, topic), and the scores are the same, then 
        #   it may be a bad edge case
        heapq.heappush(self.prio_q, (-new_score, topic, new_version))    
        return
```

## Systems Design
Design a real-time Trending Topics service similar to what you just implemented in memory, but this time for production at scale.

### High Level requirements
- Millions of incoming updates per second (topic, delta_score)
- Should return top-k trending topics globally with low latency
- Must support:
    - rapid score updates
    - resets
    - topic creation
    - frequent `top(k)` queries
- System must be fault-tolerant, horizontally scalable, and able to survive node failures
- No single machine can hold all state
- Consistency model is up to you, but justify it

### API Surface
- `POST /add`
- `POST /reset`
- `GET /top?k=N`

### Initial Thoughts, Questions (SD)
#### Clarifying Questions
- Do multiple clients in parallel, and or concurrently, update topics? Would different clients depend on the actual timestamp of their updates to be consistent? If client 1 updates topic 1 at time 1, and client 2 updates topic 1 at time 1.1, is it strictly required we have that ordering in place?
- As for consistency, do we require strict consistency after a write by a client? i.e. should the resulting read somehow be blocked until writes are finalized for certain topics? This would prove quite difficult in a system of this throughput, and would drastically change choices
    - What are latency requirements? They'll be highly affeceted by our choices of ordering and consistency

- Yes, multiple clients update topics concurrently
- No, you do not need to preserve client-issued ordering
- Eventual consistency is acceptable
- No strict read-after-write consistency is required for top(k)
- Writes do not block reads
- top(k) must return in < 100 ms p99
- Update propagation may lag slightly behind; sub-second convergence is acceptable

#### System Constraints
The system will receive a heavy amount of write traffic, millions of input POST per second, and the system needs to handle each of these as independent updates to a central system. Each write also affects some global ordering of topic events that need to be handled in a distributed manner so that we can return results within 100ms for 99% of the API calls to `top-k`. The system must be fault tolerant and horizontally scalable, so partitions are needed, which will affect how we do global ordering, and will ultimately turn this into local and global ordering problem

#### Identify Core Challenges
The core challenges here are going to be: 
- Handling millions of writes per second in an efficient way 
- Doing global ordering after millions of updates 
- Serving the top-k in an efficient way given millions of updates 
- Keeping things reliable / fault tolerant without sacrificing speed or consistency

#### Starter Architecture
At a high level: 
- To horizontally scale we'll need to partition out the write update processing 
- Each of these different partitions should store it's local top-k view to ensure it doesn't have to read from across the system. These do not need to worry about serving reads 
- There can be a global aggregation process that runs global ordering across all partitions as is required, and this can also help serve the top-k reads 

In this way we can horizontally scale out new update requests to handle millions of write updates, and they will flow to an end aggregator that ultimately has to do more work and handle read requests from clients - the two parts are separate and have different scale and SLA needs

#### Real Architecture



#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture
