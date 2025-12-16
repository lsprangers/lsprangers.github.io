---
layout: technical
title: Kafka
category: Architecture Components
difficulty: Advanced
description: Discussion around Kafka Brokers
---

## Kafka
Kafka at it's core is a [distributed queue](/docs/architecture_components/typical_reusable_resources/typical_distributed_queue/index.md) with extra bells and whistles that ultimately have it categorized as a [distributed broker](/docs/architecture_components/typical_reusable_resources/typical_broker/index.md)

It's also slightly linked to [PubSub](/docs/architecture_components/typical_reusable_resources/typical_distributed_pubsub/index.md)? All of these things are generally linked together!

![Queue, PubSub, and Kafka](/img/queue_pubsub_kafka_flowchart_freehand.png)

- Queue are FIFO data structures, which Kafka is
    - Publishers subscribe
    - Consumers will pull a message, and typically the message is pulled by ***only 1 consumer***
- PubSub servers are similar to queue's, but they build on top of them with slightly different semantics
    - Publishers still push messages
    - There are typically ***one or more consumers***
        - Because of this, the PubSub server is usually responsible for ***pushing to consumers*** instead of consumers pulling like in a queue
    - Some PubSub servers allow for consumers to pull, and at that point they're similar to multi-consumer queue's
- Kafka itself will have Topics, similar to PubSub, except each Topic is further split into Partitions
    - These Partitions act as SQS message queue's where consumers will pull off them, but they deviate from message queue's in that each consumer will access each message 1+ times. Kafka doesn't host each message only once like SQS message queue's do
    - Ordering is guaranteed within a partition, but not in a Topic
    - Routing to Partitions is an important thought topic, as incorrect routing or partitioning can lead to bad aggregations on the other side if order matters 

![Queue, PubSub, and Kafka](/img/queue_pubsub_kafka_architecture_freehand.png)

## Optimization