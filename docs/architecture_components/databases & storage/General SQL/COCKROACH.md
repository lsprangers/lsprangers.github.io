---
layout: technical
title: Cockroach DB
category: Architecture Components
difficulty: Advanced
description: Discussion around Relational SQL Databases
---

## Cockroach DB
Most of this is from [CockroachDB Whitepaper](/arxiv_papers/CockroachDB%20marked%20up.pdf)

CockroachDB is a fully distribution, multi-regional, fault tolerant database that supports [serializable transactions](/docs/architecture_components/typical_reusable_resources/typical_distributed_kv_store/ISOLATION_LEVELS.md#isolation-level-spectrum). Turns out that's quite an involved process

CockroachDB seems to be highly focused on consistency and distributed transactions, and in terms of CAP theorem it's categorized as a CP system, prioritizing strong, serializable data consistency over immediate availability during severe network partitions. It guarantee's ***linearizable consistency*** via it's [RAFT and leaserholders](#raft-and-leases) structure

### Bells And Whistles
CockroachDB (CRDB) can be considered a full fledged production database with all of the bells and whistles needed for a transaction database used in todays age. I basically just copied and pasted their bullet list
- Fault tolerance done via 3 replicas of any partition stored in distinct geographic locations
- Maintains high availability through auto recovery machanism when a node fails
- Compliance and HA via geo distributed partitioning and replica replacement
    - Uses heuristics for data placement, but allows user based partitioning + location placement (GDPR)
- Transactions across multiple geographies, multiple partitions, and multi-node
    - Serializable isolation without any specialized hardware
    - Standard clock synchronization mechnism like NTP is sufficient for serializability
        - No phantom reads, ensures repeatable reads. etc
- Query optimizer + distributed SQL engine
- Schema updates / changes, backup and restore, fast imports, JSON support, integration to OLAP systems (CDC?)
- CRDB cluster can span an arbitrary number of public and private clouds
    - Cloud agnostic, bare metal, apache license after 3 years

## System Overview
CRDB uses shared nothing architecture so all nodes are used for storage and computation, and so a CRDB cluster contains an arbitrary number of nodes needed to fulfill storage, queries, replication, etc. Any cluster can handle client connections, becuase any node would have the following layers:
- **SQL Layer** is the interface for all user interactions with the underlying database (across cluster)
    - It includes parser, optimizer, and SQL execution engine itself which will convert declarative SQL statements to read/write requests on the underlying K:V store
    - Same thing as any other query parser, and these declarative items then create imperative calls to underlying **transaction layer**
    - SQL layer has no idea how data is partitioned or distributed, as distribution layer abstracts things away to represent a K:V store with `get`, `set`, etc
    - TODO: [SQL Query Architecture](#architecture)
- **Transaction Layer** handles requests from the SQL layer, and this layer ensures atomicity of changes spanning multiple K:V pairs
    - Largely responsible for isolation guarantees
    - Even this layer is abstracted away to believe it's engaging a monolithic K:V database
    - - TODO: [Transaction Architecture](#architecture)
- **Distribution Layer** presents the abstraction of a monolithic K:V database
    - All data addressable within this key space, whether it's system data or user data
    - Range partitioning is used on keys to divide the data into contiguous ordered chunks of ~64MiB stored across the cluster
        - Small enough to shuffle across nodes easily, but large enough to store contiguous data frequently accessed together
    - Each of these chunks is a **Range**
        - Ranges start empty, grow, split, merge, etc
        - These ranges can split if they become hotspots
    - Ordering between ranges is maintained in a two-level indexing structure inside a set of system ranges, which are cached for faster K:V lookups
    - Ultimately, this distribution layer is responsible for identifying which ranges should handle which subset of each query, and then routing to these subsets
        - This seems like a [Disk Based Structure Of Sorted Ranges](/docs/architecture_components/databases%20&%20storage/Disk%20Based/index.md)
- **Replication Layer** focused on replicating ranges across nodes
    - Uses [consensus based replication](/docs/architecture_components/typical_reusable_resources/typical_distributed_kv_store/REPLICATION.md#consensus) like RAFT or Paxos to ensure all replicas are in sync before returning success
- **Storage Layer** represents the physical disk-backed K:V store
    - Provides efficient writes and Range scans for typical SQL execution needs
    - Utilizes [RocksDB](/docs/architecture_components/databases%20&%20storage/Disk%20Based/index.md) which is an LSMTree based disk storage mechanism, that uses multiple components to durably store sorted data to disk with efficient indexes for querying

### SQL Layer
Generally just exposes a SQL API to developers to convert high level SQL statements to low level read and write requests to the transaction layers K:V store

- **SQL API**: Forms the user interface, and allows developers to submit declarative SQL statements
- **Parser**: Converts SQL text into an abstract syntax tree (AST) via `yacc` files
    - Not much to go over here, it's documented everywhere
- **Cost Based Optimizer**: Converts the AST into an optimized logical query plan
- **Phyiscal Planner**: Converts the logical query plan into a physical query plan for actual execution by one or more nodes in the clluster
- **SQL Execution Engine**: Executes the physical plan by making read and write requests to the underlying K:V store

#### SQL API
Forms the user interface, and allows developers to submit declarative SQL statements

Developers are able to connect to any node in a CRDB cluster, so SQL API requests can go to any node - therefore, CRDB works fairly seamlessly with load balancers who can route any request in any way to any node. Whichever node receives the request acts as the ***gateway node***, which processed the request and responds to the client

Data will get written to and read from the [storage layer](#storage-layer) way at the bottom, and inbetween there are a ton of resources to ensure data that's committed is actually committed, highly available, etc

#### Relational Structure
Users experience things as a relational structure comprised of *rows and columns*. Sets of rows and columns are organized into *tables*, and then collections of tables make up a *database*. A CRDB cluster can contain one or many databases spread out and replicated over many nodes

CRDB provides the typical SQL flavors and constraints like foreign keys and other validation constraints, and has typical ANSI SQL based semantics. ACID semantics also follow the typical transaction patterns with `BEGIN`, `COMMIT`, etc. Alongside that, each row must have a primary key which allows for access of that rows attributes (columns)

#### Logical Planner
The parser takes the string SQL query, converts it into an AST, and from that a logical query plan is required. The AST is transformed into this query plan in following steps:
- AST is transformed into a high-level logical query plan which includes ***semantic analysis*** which includes operations like:
    - Checking whether a query is valid
    - Resolving names, references, etc
    - Eliminating unneeded intermediate computations such as `1+1 = 2` that don't require data access
        - AKA constant folding
    - Finalizing data types to use for intermediate results, which includes checking if a query contains one or more subqueries
- Logical plan is simplified using a series of transformations that are always valid
    - `a BETWEEN b AND c` can get converted to `a >= b AND a <= c`
- The logical plan is optimized using a search algorithm that evaluates many possible ways to execute a query, and selects an execution plan with the least cost
    - This search algorithm is usually based on heuristics like node processing time, costs, data flows, and overall table cardinality and returned data
    - Ideally there's reduced total shuffle, for example combining data from 2 partitions, we'd desire choosing the larger one for most of the computations where it's local
    - Partition level metrics and aggregations also help to skip over some partitions overall, or to use partition level statistics as a quick cache via automatic stats collection parameters
    - etc...

All of these are taken into consideration to simply come up with one of many plans that can turn the AST into an actual logical plan of execution based on heuristics and costs

#### Phyiscal Planner
After receiving the logical query plan, the physical planner decides which nodes will participate in the execution of the query itself based on range locality information

This is where CRDB decides to distribute a query to perform some computation close to where the data resides. Distribution here refers to if the gateway handler node itself handles the computation, or if it decides to split computation out amongst many other nodes, not in terms of actual storage layer nodes. Distribution would result in something like multiple nodes handling *TableReader* operators, one for each node containing a range read by the scan, and the remaining logical operators like filters, joins, etc are then scheduled on the same node as *TableReader* - similar to Spark transformations on partitions

This results in a directed acyclic graph (DAG) of physical SQL operators. These SQL operators are able to be directly ran on the [distribution layer](#distribution-layer) as it presents an abstract K:V store - the SQL layer doesn't care about node placement or anything like that

#### SQL Execution Engine
The physical plan is sent out to one or many nodes for execution, and on each execution node CRDB spawns a *logical processor* to compute part of the query, these processors communicate with each other over a logical flow of data, and the combined results of the query are ultimately sent back to the gateway node after all operations are completed

All of this data is encoded and serialized, and so this must be decoded by gateway node before returning to the client

***Vectorization*** is possible to run SIMD instructions over data, and ultimately reads batches of data from disk in the storage layer. It'll convert data from row format to columnar format, and these batches of column data are stored in memory so the engine can access them quickly during execution. The SIMD level instructions are fairly specific to each physical operator, and are apart of CRDB protocols. After computing the result set, it's transformed back into row format for communication

#### Encoding
Almost every layer below the SQL layer operates on raw bytes (serialized, encoded data) so CRDB must encode and decode, to and from transaction layers, for everything

For indexed columns, the encoding needs to preserve the same sort order as the data type it represents, mostly because the underlying storage is stored as sorted K:V maps, which allows for drastically more efficient scans

#### Schema Changes
New columns, new indexes, etc are enabled by default, and replica nodes stay online during this transition. The underlying protcool allows different nodes in the cluster to asynchronously transition to a new table schema at different times and continue to accept reads / writes and catch up

The schema change protocol decomposes each specific schema change into a sequence of incremental changes that achieve the desired effect 

### Transaction Layer
The transaction layer implements support for ACID transactions by coordinating concurrent requests from the [SQL layer](#sql-layer) to run on the underlying [distribution layer](#distribution-layer)

As always, consistency is king for CRDB, and everything throughout is how to keep all of this a consistent experience for developers to create API's off of. The transaction layer is an incredibly important part of that as transaction semantics and [isolation levels](/docs/architecture_components/typical_reusable_resources/typical_distributed_kv_store/ISOLATION_LEVELS.md) affect how concurrent operations affect each other, and the latency end users experience

All statements are handled as transactions out of the box, which is known as ***autocommit mode***, and outside of that the typical transaction level commands are available. These transaction level commands are also how the [replication layer](#replication-layer) allows for read replicas of data up to a certain point
```SQL
BEGIN
COMMIT
ROLLBACK (to savepoint)
AS OF SYSTEM TIME -10s
```

#### Writing
Writing cannot be done directly to disk by the transaction layer, as there's a number of consensus, consistency, and durability items that are addressed by lower layers

Concurrency and parallelism issues are common in distributed systems, and CRDB utilizes ***Write intents*** for this purpose. Outside of that multiple locks, transaction tables, and per-node objects are used to help in [Multi Version Concurrency Control (MVCC)](/docs/architecture_components/databases & storage/General SQL/MVCC.md)
- Write intents are replicated via RAFT, which acts as a provisional value and an exclusive lock
- Unreplicated locks represent a provisional uncommitted state, these locks are stored in an in-memory per-node lock table 
- A transaction record storedin the range where the final write will occur, which includes transactions current state 
    - `PENDING, STAGING, COMMITTED, ABORTED`

#### Concurrency Control
The *concurrency manager*, via it's [MVCC](/docs/architecture_components/databases & storage/General SQL/MVCC.md), keeps multiple timestamped versions of data objects, allowing each values transaction to read a consistent snapshot of the data as it existed at the start of their operation
- The **latch manager** sequences the incoming requests and provides isolation between those requests
- The **lock table** provides both a locking mechanism and sequencing of requests (in unison with latch manager). This lock table is the per-node in-memory data structure that holds a collection of locks acquired by in-progress transactions

Ultimately, this entire transaction layer's focus is on the concurrency manager, which looks to engage with some in-memory data structures to ensure transactions have tolerable isolation levels. Each request in a transaction should be isolated from other requests, and once a transcation is committed it should be able to resolve without any worry of affecting other transactions

There's a number of locks used throughout this process, and essentially as new transactions come online and try to access data that's under a lock, it will wait in a queue for that lock to be released

#### Isolation Levels
CRDB offers both **serializable** and **read committed** [isolation levels](/docs/architecture_components/typical_reusable_resources/typical_distributed_kv_store/ISOLATION_LEVELS.md). By default all transactions are executed at the strongest level of serializable which permits no concurrency anomalies

Serializable guarantees that even though the transactions may execute in parallel, the result is the same as if they had executed one at a time without any concurrency. This ensures data correctness by preventing all anomalies allowed by weaker isolation levels such as phantom reads and non-repeatable reads

##### Serializable Example
- Hostpital has an application for doctors to manage their on-call shifts
- The hospital has a rule that at lesat one doctor must be on call at any one point in time
- Two doctors are on-call for a particular shift, and both of them try and request leave for the shift at approximately the same time
- In PostgreSQL, with the default `READ COMMITTED` isolation level, the ***write skew*** anomaly results in both doctors successfully booking leave, and the hospital having no doctors on call for a shift

***Write skew*** occurs when a transaction reads something, makes a decision based on the value it saw, and writes the decision to the database. However, by the time the write is made the premise of the decision is no longer true. The only isolation levels that guarantee this won't occur are `REPEATABLE READ` and higher, which ensures that any transaction that reads data will essentially lock that data somewhere so nothing else can update it.

### Distribution Layer

### Replication Layer
The replication layer receives requests from the [Distribution Layer](#distribution-layer), if the node that has received the request is the leaseholder, it moves forward, and if not it returns an error with a pointer to the leaseholder. The replication layer commits commands to disk via RAFT consensus, and serves actual content from the [Storage Layer](#storage-layer)

Fault tolerance and high availability is therefore guaranteed through consensus replication, disk based storage, automatic recovery, and multi-replica partitions of data ranges

Most of the below content sits in the ***replication layer***. All of it is defined explicitly for ***Ranges*** - all replication, duplication, leadership, leaseholders, etc are strictly for Ranges

The whole entirety of consistency basically depdends on RAFT, leases, and membership changes which can all change if Ranges split, merge, or change in any way. CRDB implements ***multi-active*** availability by having the RAFT quorum completely agree before returning commit success (3 is the least number of nodes to ensure this, so that's default)

The number of failures that can be tolerated is `(n_replicas - 1) / 2`, so with 3 nodes, 1 failure can be tolerated, etc... and this will directly affect the availability SLA when paired with node failures of major cloud providers

#### RAFT
[RAFT](/docs/architecture_components/typical_reusable_resources/typical_distributed_kv_store/REPLICATION.md#consensus) is used for consensus based replication, which ultimately ensures that a majority of replicas agree on a specific value, and that once that value is determined to be committed we can return success. Once a commitment is returned, that value can never be broken while RAFT continues operating. ***Every replica of a Range form a raft group***, so inside of the raft grouping it's only the replicas of a Range talking to each other. Each replica is either a long-lived leader coordinating all writes to the rest of the RAFT group (follower replicas), or a follower. There can be many partitions on a single VM, and so a VM may be running multiple separate raft group nodes (leader / follower) based on the number of Ranges it is hosting. The ***unit of replication is a command***, which represents a sequence of low-level edits to be made to the storage, which are the actual imperative commands from the transaction layer. RAFT will keep a consistent, ordered log of updtes across a Range's replicas, and each replica individually applies commands to the storage engine as RAFT declares them to be committed

#### Leases
CRDB uses ***Range-level leases*** where a single replica in the RAFT group (usually the leader) acts as the ***leaseholder***. This is the only node that's allowed to serve authoritative up-to-date reads or propose writes to the RAFT group leader

There's a mention that "because all writes go through leaseholder, reads can bypass networking round trips required by RAFT without sacrificing consistency" - I didn't know what this meant before, but, I think, it ultimately means if RAFT leader and leaseholder are on the same node then there doesn't have to be as much network round trip as leaseholder can directly ensure it has latest value by engaging with RAFT leader. CRDB actually ensures the leaseholder is also the RAFT leader via ***leader leases***, which ultimately optimizes the speed of reads and writes, while lowering overall networking. On any new write request, a majority of replica nodes must be able to communicate with each other to coordinate the write, which ensures the most recent write is always available to subsequent reads. If there's no leaseholder, any node receiving a request will attempt to become the leaseholder, and for a leaseholder to extend it's lease it must also remain the RAFT leader

Leases of user Ranges are tied to the liveliness of the node the leaseholder is on, and so nodes need to signal liveliness via heartbeats every 4.5 seconds. These ranges must be renewed within that timeframe, and if replicas detect a leaseholder isn't live it will try to acquire the lease. ***Lease acquisitions piggyback off RAFT***; replicas attempting to acquire a lease do so by committing a special lease acquisition log entry. Leaseholder liveliness is very similar to RAFT leader liveliness, and ultimately both lead to an overall consensus of "who is leading this" - one is for authoritative node actions (reads / writes in control plane), and the other is for value level consensus (K:V pairs on data plane)

#### RAFT and Leases
As mentioned below, leaseholders are the authorized nodes responsible for accepting reads and writes from users, they will take actual queries from transaction / distribution layers and then send those same commands to the RAFT leader. Typically these are on the same machine, but regardless the RAFT leader then takes those commands and establishes quorum with the set of replica followers, and then responds to the leaseholder who can then respond to client

Client --> leaseholder --> RAFT leader --> replica nodes / followers --> aggeregate quorum to RAFT leader --> leaseholder --> client

The serializability on CRDB is ensured by enforcing strict protocols between these 2 essential services, and any of the arrows above can break causing RAFT leader elections, new leaseholders, etc all the while quorum commands and lease proposals are flying around the Range replica set

It's truly one of the most critical aspects of CRDB, and I don't have the ability to explain every part of it here becuase it's much better suited explain by other folks

The stateful and durable RAFT log, along with commit timestamps and caching, essentially allow new leaseholders, new RAFT leaders, new replica nodes, etc all to come into a cluster / reboot and "catch up" while guaranteeing all commits on the RAFT cluster have a quorum. ***This RAFT log + protocol underpins almost every part of recovery and high availability***

- Question: So what's the point of both leaseholders and RAFT? They seem duplicative
    - In ***strongly consistent*** reads, leaseholders do completely bypass RAFT, because the leaseholders writes must have been committed in the first place to achieve consensus, so a second consensus is unnecessary
    - The two items do actually solve 2 separate problems:
        - ***Leases*** solve read performance and location control
        - ***RAFT*** ensures data consistency and quorum
    - Relying on RAFT only has horrible read performance
        - Every read would require a round-trip to quorum to ensure the leader is still the leader
        - Leaseholders can serve strongly consistent reads directly from it's local storage without checking followers
    - If the leaseholder gets partitioned, then the leaseholder itself cannot guarantee consistency. If the leader becomes partitioned and replicas cannot access it, they may think themselves as the new leaseholder, which causes two nodes to believe they're the leaseholder (***split-brain***)
    - When the leaseholder proposes the write to the RAFT group it can wait for quorum and then respond, and in the future it can immediately respond to read requests, and no other node would be out of sync or cause split-brain


```
A - B - C - D (RAFT leader)
----partition----
E (leaseholder)
```
Take the example below where `E` is the leaseholder, but has become partitioned, and now `D` is the RAFT leader - this is a *leader-leaseholder* split
- In older versions of CRDB with ***epoch-based leases*** (time based) a partitioned leader, `E`, could continue to serve consistent reads for a short time. No other node can become leaseholder in the top partition (`A - D`), and so E will serve data and no new writes will be able to occur. `E` cannot get data level quorum with RAFT, and so it won't be able to get data level consensus
    - Once the epoch is up, `E` can't renew it's lease because renewal requies a RAFT write (to ensure data consistency availability) which it cannot achieve in minority partition, and so at this point it stops serving as leaseholder
    - `D` as the RAFT leader cannot serve reads either, it's not the leaseholder! None of them can! If any request came to `A-D`, they would try and forward it to the leaseholder that they know of `E`
    - Eventually, `A-D` will realize the leaseholder `E` is unreachable, and so once the lease expires a node on majority side will be granted a new lease via a RAFT command
    - ***This still avoids split-brain***, the leaseholder ensures that, but at this point no new writes can occur
    - Time based leases look to ensure that specific intervals of MVCC timestamps never overlap, and so two replicas can never hold overlapping lease intervals for the same range. Even if `E` is partitioned, it only serves reads for the remainder of it's current valid time slice, and never afterwards
        - ***This is why the paper mentions "consistent even with commodity hardware"***
- In modern day (25.1+) the ***leader-lease guarantee*** helps to avoid the above
    - RAFT leader and leaseholder are now the same role, so if `E` is that, then it will not be able to serve writes in the same way because the RAFT leader can't reach consensus
    - Once it stops receiving heartbeats from the quorum, it automatically loses leadership **AND** leaseholder status
    - In this scenario, `E` would immediately stop, and so the `A-D` realize this eventually and look to elect an entirely new leader + leaseholder replica
        - This leads to faster recovery time, and still completely avoids split-brain scenarios

So what if a new node tries and becomes leaseholder? In newer versions of cockroachDB `E` needs to have ***leader-leaseholder*** guarantees, and so it will stop serving as the authoritative node and `D` will try and become RAFT leader. In older versions, without leader-leaseholder guarantee, both `D` and `E` would serve, and `E` would serve stale data

#### Follower Reads
After reviewing the above, it was tough to read "we also allow follower reads from any node"! Follower based replicas:
- Do not participate in RAFT quorum voting
- Constantly receive updates from RAFT leader cluster
- Cannot serve "live" data - ***they only serve stale data***
    - Queries literally include `AS OF SYSTEM TIME -10s` and similar patterns
- Follower can only serve the read if it's a **closed timestamp**, which means a heartbeat from the leaseholder is ahead of the request time
    - In this way, followers know of data being consistent at that timestamp, and that no more writes will occur before that specific timestamp
- Therefore:
    - Still have RAFT majority quorum
    - Allows for read replica semantics, but strictly mentions that ***they are up to a given timestamp***
    - User must accept this tradeoff
- Benefits:
    - Reduced strain on leaseholder
    - Geo-location latency - a user in Australia can have a much faster read even if the main replica set + leaseholder is in UK
    

#### Circuit Breakers
When an indiviual Range becomes unavailable, requests to those ranges are refused by a per-replica circuit breaker mechanism instead of hanging indefinitely. This results in a transient `ReplicaUnavailableError` bubbling up to SQL Layer, but after a certain amount of time the Range will either be removed and marked dead or come back online

#### Snapshots
Snapshots help in ***Range rebalancing*** - snapshots copy all of a replicas data as of a specific timestamp, and sends it to other nodes during a rebalance event to expedite replication

A node would then replay all of the actions from the RAFT groups log that have occurred since then, and would ultimately be a new replica

Therefore, snapshots are guaranteed state at some point, easily serialized and transferred over the network in bulk to avoid having to send commands acorss the network, and then from that timestamp RAFT logs replay the rest

### Storage Layer
