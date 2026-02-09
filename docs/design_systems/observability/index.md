---
title: Distributed Metrics Aggregation System
category: Design Systems
difficulty: Advanced
show_back_link: true
---

## Systems Design



### High Level requirements
- Clients send:
    - counters
    - gauges
    - timers / histograms
- Ingest up to 20M events/sec
- Queries:
    - aggregates over last N minutes
    - percentiles (p50 / p95 / p99)
- Horizontal scale
- Eventual consistency acceptable
- Retention: 7 days
- Cardinality: millions of metric series

Restating:
Clients will aggregate defined metrics locally, and we need to keep track of these client defined metrics. These metrics can be counts, gauges (what are gauges?), or time based (not a one size fits all data structure). Ingesting 20M events / second so heavy write throughput on our system. Clients will query specific aggregations and other statistics like percentiles. We should handle counts, percentiles, and time based visualizations (antything else specifically?). Eventual consistency is acceptable, no hard requirements on timing and consistency from our ingest and aggregate to our query layer. Millions of metric series means we need to somehow serve these millions of metrics in an efficient manner
- What's the QPS of each user, and how many typical users?
- What are the metric types we will handle? i.e. what aggregations, and should these aggregations be specified in the design, or are we focusing only on ingest layer and query layers for now?
- How can we identify clients? Are there many users per a firm like client, are clients singular entities that only focus on their metrics, etc?
- Do all retained metrics need to have the same efficiency and query time as new metrics, or are there layers to our query layer SLA's?
- What tolerance do we have for fault tolerance, partitioning, and consistency? Which are we most concerned on high availability, consistency, accuracy under node failure?

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
