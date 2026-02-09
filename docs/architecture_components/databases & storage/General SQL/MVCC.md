---
layout: technical
title: Multi Version Concurrency Control (MVCC)
category: Architecture Components
difficulty: Advanced
description: Discussion around Relational SQL Databases
---

## Multi Version Concurrency Control (MVCC)
MVCC is a larger concept than just a protocol as it involves almost all aspects of DBMS design and implementations

It's the most widely used schema in DBMS's, and is used in almost all modern day database management systems that need to implement concurrency controls over transacted data. NoSQL systems, RDBMS, and other database management systems all benefit from it, and even systems that don't support multi-statement transactions still benefit from its usage

MVCC has a DBMS maintain multiple physical versions of a single logical object that's in a database.When transcations write / commit a new object, the DBMS writes a new version of that object, and so as new transactions read that object, it reads the newest version that existed when the transaction started. If there's a transaction inbetween that updates the data, the older transaction will still utilize the older version of the data

The largest fundamental concept is ***writers don't block writers and readers don't block readers***. This is done via versioned assets of data that are kept until all transactions utilizing that data are committed and they can be cleared

Read-only transactions can read a consistent [snapshot](/docs/architecture_components/typical_reusable_resources/typical_distributed_kv_store/ISOLATION_LEVELS.md#isolation-levels) of the database without having to use locks of any kind. Alongside that multi-version DBMS's can easily **support time travel** queries which allow reading of data at a certain point in time

### MVCC Database Design
A DBMS with MVCC enabled will have these implementations typically:
- Versioned storage which stores different versions of the same logical object
- When a transaction begins, the DBMS takes a snapshot of the database (copying transaction status table) 
- DBMS uses the snapshot to determine which version of objects are visible to the transaction

After that, 4 crucial MVCC design decisions are to be made by the actual database designer:
- **Concurrency control protocol**: How does the database handle multiple transactions updating data objects?
    - Two phase locking, timestamp ordering, optimistic concurrency control, etc
    - Snapshot isolation allows for copying of a transaction table to support efficient reads of what data a transaction knows about
    - **write conflicts** can be solved by first writer wins (when multiple try and update same object)
    - **Write skew anomaly** is still non-serializable, meaning if transaction1 tries to update all white marbles to black, and transaction2 tries to update all black marbles to white, there's potentially no linear serializable sequence for those 2 to occur correctly
- **Version storage**: How the DBMS stores different physical versions of a logical object, and how transactions query that data
    - Append only storage with indexes for sorting on timestamps and keys 
        - Each new version involves updating indexes so transcation can find values efficiently
    - Time travel storage is when a DBMS maintains a separate table called time travel, which stores older versions of tuples. On every update the DBMS copies the old version to the time travel table and overwrites the tuple in the main table with new data
        - Pointers in main table point to old versions of data
    - Delta storage, similar to time travel, stores only deltas of tuples. Transactions can recreate older versions by iterating through the dataset deltas
- **Garbage collection**: Reclaiming physical versions from database over time that are no longer useful
    - Reclaimable if no possible active transcation can "see" it
    - This background vacuuming is done by background threads / processes
- **Index management**: All primary key indexes always point to the version chain head, but how often does the DBMS update indexes on new transactions in that chain
    - This one makes less sense, but idk


