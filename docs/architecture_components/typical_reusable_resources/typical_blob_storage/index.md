---
layout: technical
title: Distributed Blob Storage
category: Architecture Components
difficulty: Advanced
description: Architecting a Blob Storage Solution
---

## Distributed Blob Storage
Distributed Blob Storage is at it's core a key-value store for Binary Large OBjects (BLOBs) such as video, image, audio, or anything...all data is binary so anything is BLOB

Some common examples are Amazon S3, Google Cloud Storage, and Azure Blob Storage

The main idea behind all of these are large scale, "infinitely scalable", durable storage with client(s) in many languages to interact with servers

Apparently it started with requirements of Write-Once Read-Many (WORM), but today I think a lot of groups are doing both writes and reads at a high rate

## System Design
System design should allow for:
- Clients based on SDK's that can upload and download BLOBs from their local compute
- Typical distributed components of rate limiting, available, durable, etc...
- Authentication and authorization
- DNS offloading + regionality concerns
- BLOBs aren't able to be deleted

### Functional Requirements
Functional requirements are around "what the system should do" and the generic API's or abilties it should have

- Create a container: A container is a logical grouping of BLOBs, where BLOBs are ordered inside the container and have certain policies attached to them
    - PUT data
    - GET data
    - Delete data
    - List blobs
    - Delete a container (if empty?)
    - List containers
- Versioning
    - PUT data should create a new version of the old data without explicitly deleting the old data
    - This new data should be returned in a subsequent GET
- Policies
    - There should be policies attached to data that can move it / delete it over time if the user requests it

### Non-Functional Requirements
- Availability: System should be available
- Durability: Once data is successfully uploaded it shouldn't be lose unless explicitly deleted
- Scalability: System should handle a lot of BLOBs
- Throughput: Transferring GB of data from thousands of users
- Reliability: Should detect and recover from failure promptly
- Consistency: System should be consistent with uploads and downlaods
    - Eventual consistency is enough, and you don't need strictly strong consistency across all replica nodes
