---
layout: technical
title: Stream Processing
category: Architecture Components
difficulty: Advanced
description: Discussion around Kafka Brokers
---

## Stream Processing Thoughts
Kafka itself will help with reliable, fault tolerant, ordered storage of streaming messages, it's ecosystem will also help setup clusters, manage clusters, optimize streams, and enable stream processing

Stream processing engines are everywhere, with some of the most popular being Flink, Spark Streaming, Delta Live Tables (sub-component built on Spark Streaming), Kafka Streams, and other open source engines and frameworks

***Stream processing is an extremely complex architecture to manage, and comes with many pitfalls and decisions compared to batch processing - I, in all of my time, have still never seen a use case in the world that needs full stream processing for an entire analytical stack***

I personally think the decisions made between batch, stream, real time, etc are all important to consider given streaming is a "race car" you need to take care of and use in very specific circumstances, whereas batch processing (even mini-batch every minute) is more of a mini-van with reliable setups that have been proven over time in industry - don't Kafka yourself into tech debt when your SLA is daily

Below there's some introductions to stream processing, topics, streams, and tables along with discussing **declarative ways of doing this (kSQL)** versus **imperative (scala stream definitions)**

## Stream Processing
Most of this is covering the [Michael Noll Kafka Blog](https://www.michael-noll.com/blog/2018/04/05/of-stream-and-tables-in-kafka-and-stream-processing-part1/)
Now to cover stream processing - everything in stream processing is usually setup over **unbounded** key value streams of event data. This means it's continuously coming into the stream processing engine, and so there are new architecture components compared to typical RDBMS / batch processing

A majority of the time what needs to be covered are **continuous analytical metrics** such as top-k, last seen, rolling window, etc which cover past up to present, alongside **stateful analytical metrics** which cover present such as sum, count, max, etc. If we are looking at the top-k most listened to songs over the last 5 minutes, days, weeks, and months we will ideally want to keep a rolling count of that data coming in from the past (**stream**), and this will result in a stateful result set (**table**) we could query at any time. However, if we wanted to change it to every 10 minutes, weeks, months, etc then our table would no longer be useful and we'd have to recompute everything from our stream

- **Topics** are unbounded sequence of K:V pairs of raw bytes
    - Kafka has topics which are partitioned and replicated, where each node in a cluster is a leader of some partitions, and a follower with replicas for others
    - A topic has $1:M$ partitions, and each partition has a partition leader that handles read and write requests
    - Order is guaranteed within partitions, so if we have a User topic and we split it up between 4 partitions, the ordering in partition 1 may "intertwine" with partition 2 and there are no guarantees between those two partitions
        - A majority of times groups will try to partition and then enforce ordering inside of their consumer application logic which is an ***absolute anti-pattern and means you're using a tool unfit for your use case***
    - Scala analogy: `val topic: Seq[(Array[Byte], Array[Byte])] = Seq((Array(...)))`
- **Streams** are the unbounded, type casted (schema enforced), K:V pair messages across partitions that we process over time. Streams are the ***full history of the world events from the beginning of time until today***, they represent the past and present, and new events are constantly being added to the world's history
    - Topics simply have `array(byte[], byte[])` K:V messages, and so streams are a layer above that are supposed to define schemas and extra serialization protocols on top of them
    - Streams enforce schema's on read, and on write, meaning as they read in messages they will take in an avro schema and use it to decode the raw bytes into an actual typed message
        - This is similar to the API Layer 7 protocols that take in raw socket bytes and create HTTP headers and messages from them! Something somewhere needs to define the format of the bytes, and in Kafka it's Streams
    - We can enforce contracts for these on-read and on-write layers, so that a message is never written to Kafka with a bad format, and a message that is read with a bad format is discarded / quarantined properly
        - This is typically what we refer to with Avro Schema's
    - Scala analogy: `val stream = topic.map { case (k: Array[Byte], v: Array[Byte]) => new String(k) -> new String(v) }`
        - We literally just map over the corresponding schema to each portion of the message from the Topic, and the result is still an unbounded stream of messages
- **Tables** help us with stateful processing such as joins of real time data enrichment to dimension tables, aggregations of data into some dimension table, or other operations. A Table is a ***representation of the world today***
    - Even the WordCount hello world example actually results in a Table, and not a Stream only setup
    - Since topics are partitioned, both Streams and Tables will also be partitioned
        - Therefore, if we had something like User topic partitioned by `user_id`, and we wanted a Table with count of records over `user_country` we would first need to do this aggregation per partition, and then aggregate it globally
        - If we did something like `count(distinct X)` it's much harder because there may be repeated values across partitions you lose visibility on
            - For example if we wanted to count distinct countries across all users, and a user in partition 1 has US and a user in partition 2 has US, both of the counts would be included in the partition count and we'd be unable to do it globally
        - Statistics that cannot be computed globally from per partition statistics are known as ***non-decomposable / non-commutative / non-parallelizable***
            - count distinct, median, percentile, etc are typically non-decomposable
    - Handling these necessary requirements around metrics and backfill processing make Tables a more finnicky structure
    - Scala analogy:  
        - ```val table = topic.map { case (k: Array[Byte], v: Array[Byte]) => new String(k) -> new String(v) }.groupBy(_._1).map { case (k, v) => (k, v.reduceLeft( (aggV, newV) => newV)._2) }```
        - The schema is created as in Streams example
        - `.groupBy(_._1)` means group by the Key in the K:V message `_._2` is the message
        - `reduceLeft` part will simply perform an upsert
            - The `aggV` is the old value, and this is unused in the upsert since we just use `newV` - therefore this operation is ***stateless and decomposable***
            - If we were doing a rolling count such as `aggV + 1`, it would be ***stateful***, and depending on the operation it may or may not be decomposable

***A Topic is a queue of K:V byte pairs, Streams give them typed schemas, and Tables are aggregations and stateful representations of Streams***. In comparison to Github - Streams are the commit history, and tables and the repo's at a specific commit...one is the entire history, one is the present state

| Concept | Partitioned | Unbounded | Ordering | Mutable | Unique key constraint | Schema |
|---------|-------------|-----------|----------|---------|----------------------|--------|
| Topic   | Yes         | Yes       | Yes      | No      | No                   | No (raw bytes) |
| Stream  | Yes         | Yes       | Yes      | No      | No                   | Yes    |
| Table   | Yes         | Yes       | No       | Yes     | Yes                  | Yes    |

![Chess Stream Vs Table](/img/stream_record_vs_table_state.png)

At this point it's important to think about what consequences this may have:
- The metrics we create over streams are "heavy" to change, and if your business requirements are constantly changing recreating these stream processing queries and backfilling is extremely expensive
- Tables help mitigate that, and also bridge stream to batch since most batch processing engines can interact with Tables for downstream processing
    - You want to setup your state so future changing business requirements are easy to handle and don't require new code changes and backfills
- Having access to a stream allows you to reconstruct the state of the world at any given time $t$, but storing and recomputing everything is expensive!

Quote below from [Michael Noll Confluent Blog](https://www.michael-noll.com/blog/2018/04/05/of-stream-and-tables-in-kafka-and-stream-processing-part1/)
"You certainly don’t want to build needlessly complex architectures where you must stitch together a stream(-only) processing technology with a remote datastore like Cassandra or MySQL, and probably also having to add Hadoop/HDFS to enable fault-tolerant processing (3 things are 2 too many)."

### Aggregations
*Streams are the only first class data structures in Kafka* - A Table is an aggregation of a Stream, or potentially the transformations of one or more Tables (which in turn are just Stream aggregations)

Therefore, to understand the process end to end for a Kafka DAG of multiple Streams and Tables, we really just need to focus on aggregations (Stream 2 Stream is just mapping transforms)

1. All aggregations are computed per key
    1.1 All aggregations are done per partition, per key - therefore, if you use custom partitioning, your aggregation logic is much more complex
2. All aggregations are continuously updated as soon as new data arrives in the input stream
    2.1 Therefore, the output of an aggregation is *mutable*
    2.2 Therefore, *Tables are mutable*

### Changelog Streams
Even though a Table is an aggregation of it's input Stream, it would still have an output Stream! This is known as a **Change Data Feed (CDF) or Changelog Stream** andit's counterpart in RDBMS is Change Data Capture (CDC)

Since most Tables are created as upserts / incremental changes, most downstream consumers of Tables can be built off of their changelog Streams quite easily, this allows Tables to update downstream Tables (where the downstream Tables are aggregations of changelog Streams!)

It's actually quite easy to showcase that a simple upsert Table (where value is just last one seen) would produce the exact same input Stream as it's changelog Stream. This brings up an interesting design choice in Kafka - most changelog Streams are just piped back as Topics in Kafka, and that's how it ensures reliability and durability. This relationship is known as [***Stream-Table Duality***](https://docs.confluent.io/current/streams/concepts.html#duality-of-streams-and-tables), and it shows how you can go from Stream 2 Table 2 Stream 2 Table.... and so on

### Revisiting RDBMS vs Kafka
In RDBMS, the Table is the first order construct, and so databases are really good at interacting and focusing on the "present" 

In Kafka the Stream is the first order construct, and Tables are derivations of Streams, so Kafka works primarily with the entire historic past, and because of that can also work with the present

Kafka attempts to bridge both worlds, and get the best of both worlds, by providing native support for Streams and Tables via Kafka Streams and kSQL which enable declarative syntax for both

## Pitfalls
Kafka is great, and talking about streams above was nice, but the major pitfalls I see in Kafka are backfills, changing business logic, reliability, idempotent processing, OLAP processing, and many other items - Kafka is a racecar that can do so many great things efficiently, but it needs proper attention and care to reap the full benefits and many organizations don't have the resources or alignment to do this

**Key Example**: If you have an IoT job running that processes 10 messages / second, and your transformation on those messages needs to change, how do you backfill and then blue-green swap to the new transform without impacting downstream use cases? There's no "perfect solution" in these cases, and having constantly changing transformations hinders the efficiency of these architectures

TODO: Lambda and Kappa without storing data 85 times and losing all lineage everywhere
Most companies will bridge these gaps by having Stream Processing interact with OLAP data warehousing, and that brings things to [Lambda Architectures] and [Kappa Architectures]

- Stream Ingestion and Processing:
    - Data is ingested into Kafka topics
    - Stream processing frameworks (like Flink, Spark Streaming, Kafka Streams) process the data in real time, performing filtering, enrichment, and aggregations
- Materialized Views or Intermediate Tables:
    - The results of stream processing (e.g., aggregations, stateful metrics) are written to materialized views or tables, often in a fast, mutable store (like RocksDB, Redis, or a managed state store)
- Batch Export to OLAP Store:
    - Processed or raw data is periodically exported (using connectors or batch jobs) from Kafka or the stream processor to an OLAP database (like ClickHouse, Druid, BigQuery, Snowflake, Redshift, or Apache Pinot)
    - This is often done via tools like Kafka Connect, custom ETL jobs, or CDC pipelines
- OLAP Querying:
    - The OLAP store is used for ad-hoc analytics, dashboards, and reporting, supporting complex queries over large historical datasets
- Backfills and Reprocessing:
    - For schema or business logic changes, companies often reprocess historical data from Kafka (using topic retention or archived logs) and reload the OLAP store, sometimes using batch jobs to ensure consistency