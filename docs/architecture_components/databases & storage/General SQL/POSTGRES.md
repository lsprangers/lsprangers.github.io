---
layout: technical
title: Postgres
category: Architecture Components
difficulty: Advanced
description: Discussion around Relational SQL Databases
---

# Postgres
Postgres is, in my opinion, the most useful, used, and general purpose Open Source SQL Database on the market

There are certain scenarios where Postgres doesn't do its job well, but for most "run of the mill" scenarios Postgres will cover everything you need with great support and good documentation

Postgres storage + indexes help drive a number of reusable patterns across system design:
- [Transctional Outbox](/docs/architecture_components/messaging/index.md#transactional-outbox) pattern acts as a registered outbox with the durability of transactions to ensure state transitions between messages are kept
- [Sharded priority queue's](/docs/design_systems/workflow_scheduler/index.md#implementation-details--follow-ups) can be built using [BTree indexes](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE/index.md)
- Boolean search systems can utilize GIIN Indexes

And many more - Postgres, and other relational databases, are built to provide data structures on top of data sitting on disk, and to expose those via API's. Therefore, utilizing indexes on top of data allow us to create similar in-memory patterns on distributed systems!

## Indexes
Indexes are way to store pointers, sorted structure, tree based structure, and other ordered constructs on top of data we store. When we update underlying data, we update indexes and data structures over them as well, so they mean there's extra work during writes, but they allow reads to be highly efficient

### BTree
[BTree indexes](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE/index.md) are covered elsewhere, but they're the out of the box best sort of structure to create an $O(\log n)$ tree based structure based on column(s) to do efficient searching instead of $O(n)$ lookups. All insertions, deletions, reads, and even sequential range access are $O(\log n)$, which is what has especially helped in creating a [distributed priority queue](/docs/design_systems/workflow_scheduler/index.md#implementation-details--follow-ups)

Each index essentially creates a [balanced tree on disk](/docs/architecture_components/databases%20&%20storage/Disk%20Based/index.md)

Query planners can even use indexes for pattern matching for `LIKE`, `~`, etc if the pattern is a constant or has the anchor at the end

### Hash Index
These are typical to a [dictionary / map lookup where we duplicate the entire data with a hashing function](/docs/dsa/2.%20hashing/index.md), and then do amortized $O(1)$ lookup. Similar to a dictionary, we store a number of buckets the hash function routes to, and traverse the bucketed linked list until we find the actual value. If the number of buckets equals the number of rows it's a true $O(1)$ lookup

These only handle equality `=` operators

### GIN Index (GIN, GINI)
Generalized INverted Indexes (GIN, or GINI) are essentially reverse lookup indexes - similar to the end of a book index. A book has a number of words on a page, but the index shows all pages any word is on, in the same way a GIIN Index would show what documents, pages, files, etc any lookup query is apart of (usually a word)

This makes them extremely useful for [inverted index boolean search systems](/docs/design_systems/search_system/INVERTED_INDEX.md), where we essentially lookup all files that have all words apart of a query, and then finds the intersection of all of them. The query "the quick brown fox" would find all files each word is apart of, find the intersection, and return the files in a list

They're useful if there's multiple values in a column like a `JSONB` or `ARRAY` structure, because we are essentially creating the index over a single table instead of multiple tables. You'd have to take a book and make every word of it an array to actually utilize a GINI index over it, which isn't very useful, and so most implementations are focused on making the multi-value lookups $O(1)$

### Block Range Index (BRIN)
Can be thought of as a smaller, cheaper, and more "meta" version of a BTree Index. They allow the use of an index on a "very large table" that would previously be impractical to use a BTree on without horizontal partitioning

### Generalized Search Tree Index (GiST)
Generalized search tree's allow the building of general tree structures over generic data - it's an abstract version of a BTree, and are useful to index geometric data types or full text searches