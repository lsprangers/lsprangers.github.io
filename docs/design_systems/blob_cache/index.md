---
layout: technical
title: Blob Cache
category: Design Systems
difficulty: Advanced
description: Complete Blob Cache Design
show_back_link: true
---

# Blob Cache
Design a blob caching service. Clients request large immutable blobs by key. The system should reduce reads to origin storage, handle high throughput, hot keys, cache misses, node failures, and eviction

## General Assumptions
- Blobs are immutable
- Blob keys are `TenantID + BlobID + Version`
  - Version is decided by system, not by client
  - Can return version to client
- Cache is read through, so if a certain blob key isn't in the cache it will fetch it from source of truth blob storage
- Correctness can be based on key semantics (i.e. we know exactly what content a client is looking for), we can include a LFU / LRU expiry, or remove them based on total size. The LRU is best fit for a purpose like research simulation platform where a simulation will fetch content millions of times in a short period of time, and then be done using it. The frequency doesn't necessarily matter, the timing does
- Cache doesn't accept writes, writes should go directly to source system
- Large datasets will be fetched frequently in short bursts of time, so we should store Blobs in a parallel paginated setup on high performance software so that downloading from an SDK can be done in parallel from pages
  - This will lead to hot keys during a simulation run where specific datasets are called thousands of times quickly. In these scenario's we can continue to serve content to clients and potentially push back on them during massive parallel API calls if necessary
- Load balancers should be used to route out to per-key cache servers (i.e. use "sticky" routing based on `hash(key)` to a node ring to find server placement), each cache server is "dumb" - if new servers are added we don't have to reroute any cache data, as the new servers will simply act as new read through and go fetch the data
- We are choosing the servers themselves to store data on disk to serve requests as quickly as possible, however for some specfic datasets if they're terrabytes in size a network file system architecture may be better where we route the client to a downloaded asset they can continuously utilize. This is dependent on typical workloads, but this could be a future feature instead of main implementation

## Flow

### Routing
```
Client / SDK
  -> API Gateway / Auth
  -> Cache Router
      - validates tenant/key
      - computes hash(TenantID + BlobID + Version)
      - selects primary + replicas
  -> Cache Node
      - memory metadata index
      - SSD blob/chunk storage
      - per-key request coalescing
  -> Origin Blob Store
      - S3/GCS/ADLS/internal object store
```

### Cache Node Internals
```
Cache Node
  - in-memory index:
      key -> chunk metadata, size, path, checksum, last_accessed
  - local SSD:
      blob chunks/pages
  - eviction manager:
      byte-aware LRU / segmented LRU
  - fetcher:
      range reads from origin
  - singleflight map:
      key/chunk -> in-flight fetch promise
```

## Paths

### Read Path
```
1. Client requests blob key.
2. API layer authenticates and authorizes tenant access.
3. Cache router computes consistent hash over full immutable key.
4. Router selects primary cache node, optionally with replicas.
5. Cache node checks local metadata index.
6. If present:
   - validate chunk/file state
   - stream from local SSD to client
7. If absent:
   - acquire per-key or per-chunk singleflight lock
   - fetch from origin object store
   - write to local SSD
   - update metadata index
   - stream to client
8. Other concurrent requests for the same key wait on the same in-flight fetch.
```

### Hot Keys
```
1. primary + replica reads
2. hot-key detection
3. promote hot keys to more replicas
4. client-side range parallelism
5. request coalescing on misses
6. origin miss rate limiting
```

### Failure Handling
```
virtual nodes
replica reads
origin rate limiting
background warming for known hot datasets
circuit breaker / backpressure
```

# Follow Ups
A blob is 500 GB. A simulation cluster of 5,000 workers starts reading it at the same time. How to avoid:
- every worker causing an origin fetch
  - On the in-memory map / metadata we can acquire a lock, or simply just update the value to be "Fetching" or something similar. We want to make it apparent something is going to fetch that
  - "Concurrent requests for C attach to the same in-flight fetch"
- one cache node becoming the bottleneck
  - Replicas! If we are setting defaults, or creating replicas based on internal metrics, we can route requests to primaries who can further route requests to replicas
  - Furthermore, we might want to route to nodes based on chunks instead of just blob keys
- evicting useful chunks during the run
  - Keeping up an LRU cache that doesn't evict during runs means first updating the LRU cache with the new file before going and fetching it, therefore the new file is at the beginning. We should evict based on files, not chunks
- downloading the whole blob before serving the first byte
  - Response unit is chunk, not file. Split up that return into asynchronous threads with chunk metadata


## ?s
- Streaming from SSD back to client
  - Read from local disk incrementally and write them to network socket incrementally
client asks for chunk 17
cache node finds chunk 17 on local SSD
cache node reads 1 MB at a time from SSD
cache node sends each 1 MB block over HTTP/gRPC

```python
with open(local_chunk_path, "rb") as f:
  while block := f.read(1024 * 1024):
      response.write(block)
```

Furthermore, can do stream through caching from original object store:
```
origin object store -> cache node -> client
                      |
                      +-> write to local SSD
```

- Concurrent requests with in-flight fetch
  - If 5,000 workers all request the same chunk at once, then we can simply mark the metadata value as a fetch future
```python
cache[chunk_key] = fetch_future
```
Once the future lands, all of the downstream workers waiting for it would see the same future 


- The entirety of the system is now based on `tenant, blob, version, chunk` as the ID
  - Yes
- "Run-level leases or pinning, TTL backed lease while the simulation is running"
