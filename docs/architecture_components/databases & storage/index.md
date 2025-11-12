---
layout: technical
title: Databases and Storage
category: Architecture Components
difficulty: Advanced
description: Discussion around storage of data
---

# Storing Data
Storing data is a very wide spectrum, and so you split things up as best you can

## Blob Storage
you can checkout [Typical Blob Storage](/docs/architecture_components/typical_reusable_resources/typical_blob_storage/) to see what this is usually used for 

Binary Large Object (BLOb) storage, such as Amazon S3, Google Cloud Storage, or Azure Blob Storage, is one of the most common mechanisms for storing pretty much anything

There's no indexing, no schema formats specified, or anything like that - it's just a way to store dumps of data in a "directory structure"

## Disk Based
This relates to storing data on disk using mechanisms like [LSMTree](/docs/technical writing/architecture_components/databases & storage/Disk Based/LSMTREE.md), [BTree](/docs/technical writing/architecture_components/databases & storage/Disk Based/BTREE.md), or [Parquet Flat Files](/docs/technical writing/architecture_components/databases & storage/Disk Based/PARQUET.md)

- B-Tree's are a hierarchical data structure typically used for indexes in relational databases for $O(\log n)$ lookup
    - Other nuances like much higher read throughput, but lower write throughput (a write has to go to disk)
- LSMTree's are another hierarchical data structure typically used for looking up data in K:V databases in $O(\log n)$ time
    - Other nuances like much higher write throughput (write to in-memory without touching disk), and lower read throughput (going to disk based on indexes-of-indexes)
- Parquet is a flat file structure used for massive parallel processing engines
    - It was enhanced by the Delta Format

These are all different ways to store relational, and even K:V, data in disk but they all have vastly different use cases and best practices

## General SQL
Relational SQL with indexes, schema enforcement, and all the ACID goodness baked in

## NoSQL
Basically taking away schemas, indexes, and transactions in favor of massively scaling some form of documents / K:V pairs

This doesn't begin to cover everything, as NoSQL can be Document, Wide Column, Graph, K:V, setc. (Not Only SQL), but in most peoples day-to-day NoSQL refers to K:V storage of some sorts