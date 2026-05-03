---
layout: technical
title: Messaging Components
category: Architecture Components
difficulty: Advanced
description: Discussion around Messaging Components
---

# Messaging Components

![Queue, PubSub, and Kafka](/img/queue_pubsub_kafka_flowchart_freehand.png)

# Messaging Infrastructure

## Kafka

## PubSub

## Queue

## Event Bus / Bridge

# Messaging Patterns

## Two Phase Commits (2PC)

## Transactional Outbox
A transactional outbox pattern emerges when you have multiple things you need to do that can't be apart of the same database transaction - i.e. updating a database row, and then sending a message to an event broker, while also sending a message to an external service. The problem arises with the database transaction, ***if the transaction commits, the messages must be sent, if the transaction fails the messages must not be sent (or must be reverted)***

### Main Problem
How can we enforce these rules without coupling the downstream message broker message / API call inside of the database transaction? We don't want to do networking calls that might fail in the middle of a database transaction, as the network calls can easily take hundreds of milliseconds to seconds long, and the entire time the row is locked

Furthermore, the messages must be sent to the message broker / API service in the order they were committed by the main service to the database. The ordering must be preserved across multiple service instances that update the same aggregate

### Solutions
The transactional outbox pattern in a database transaction covers this, ensuring that a database transaction that commits by a table can always be received by a downstream service

![Transactional Outbox Pattern](/img/transactional_outbox.png)

The main idea is to continue to use the database that stores the main transaction as a continuous source of truth, but we don't want to store attribute columns like `status = DISPATCHED` or `status = NEEDS_PICKUP`, because then that table would continuously be read from, updated (status updates), and queried while also being continuously written to - instead we can store a separate ***Outbox Table*** that acts as a separate log of items to consume and update in the main table

- **Participants**:
    - *Sender* is the service starting, committing, and overall "sending" the transaction
    - *Database* stores tables and messages
    - *Message relay* is the downstream service polling the message outbox
        - If a message relay polls a message and updates the outbox to processing, but fails to publish the message to a downstream service, there's a potential for multiple message postings
        - Therefore the downstream consumers ***must be idempotent*** as this is an ***at least once*** semantic style message protocol
    - *Message outbox* is a table that stores the messages to be sent
        - In a relational database this can be a generic table with indexes on `(state, created_at, <>)` attributes so lookup of `DISPATCHED` messages is easy
            - Use `FOR UPDATE SKIP LOCKED` to skip already polled messages by message relay services
            - Can partition based on a `processed_at` column so any that are null (not processed) can be quickly retrieved as well
        - In a NoSQL database the outbox can be a property of each database record
- **Results**
    - No need for [two phase commit](#two-phase-commits-2pc)
    - Messages are guaranteed to be sent if and only if the database transaction commits
    - Messages are sent to the message broker in the order they were sent by the application

### Real World Implementations
There are 2 main implementations of the transactional outbox pattern - the main one described above is the Polling Table solution, which is described above

Separately you can mine the transaction log / WAL so that any change to the database table you're trackng can be immediatelly seen without a separate table. However, in this scenario if the log miner fails it will need to store it's last published offset somewhere so it can restart from that place. If it's published sequence number 5, and has 6-8 currently in memory and fails, when it reboots it needs to start from 6 and not 8

![Transactional Outbox WAL Mining](/img/transactional_outbox_wal_mining.png)

