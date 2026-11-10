---
layout: technical
title: Chronon
category: Design Systems
difficulty: Advanced
description: Complete Video Recommendations
show_back_link: true
---

# Chronon
Chronon is one of the newer more open source full feature platforms that more companies are beginning to use

It allows you to connect to most data warehouses and streaming platforms so that you can have online feature stores for real time inference alongside historic batch jobs for large scale simulations

Most of Chronon pipes rely on idempotent updates for at least once deliveries. All of the components here are at least once, and rely on good keys to to upserts, otherwise it's basically impossible to ensure correctness

```
Application databases                 Application events
        │                                    │
        └──────── CDC / event publishing ────┘
                              │
                        Durable event log
                         /             \
                        /               \
             Warehouse ingestion     Stream processing
                      │                     │
             Raw historical data      Fresh feature updates
                      │                     │
             Curated shared tables          │
                /             \             │
       Analytics / BI     Chronon batch      │
                          computation       │
                           /       \        │
                  Training data    Online feature store
                                           │
                                     Model inference
```

## Lab Setup
```bash
docker pull apache/kafka:4.1.2
docker pull mongodb/mongodb-community-server:8.0-ubi8-slim

docker run -d \
  --name fs-kafka \
  -p 127.0.0.1:9092:9092 \
  apache/kafka:4.1.2

docker run -d \
  --name fs-mongo \
  -p 127.0.0.1:27018:27017 \
  mongodb/mongodb-community-server:8.0-ubi8-slim

docker exec fs-kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic purchases \
  --partitions 3 \
  --replication-factor 1

python3 generate.py \
  | docker exec -i fs-kafka /opt/kafka/bin/kafka-console-producer.sh \
      --bootstrap-server localhost:9092 \
      --topic purchases \
      --property parse.key=true \
      --property key.separator="|"

# Multiple consumer groups acting like DWH vs Online FStore
docker exec fs-kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic purchases \
  --group warehouse-demo \
  --from-beginning \
  --max-messages 20 \
  --timeout-ms 15000

docker exec fs-kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic purchases \
  --group features-demo \
  --from-beginning \
  --max-messages 20 \
  --timeout-ms 15000


#                        ┌─ warehouse group → historical tables
# Purchases -> Kafka ────┤
#                        └─ features group  → fresh feature state
```