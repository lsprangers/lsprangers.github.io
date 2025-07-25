---
layout: technical
title: Self Balancing Binary Search Trees
category: Data Structures & Algorithms
difficulty: Advanced
description: Binary Search
show_back_link: true
---

## Self Balancing
Ultimately Self Balancing Tree's are a way to restructure a Linked List so that search is in $O(\log n)$ time - one example is [B-Tree's](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE.md)

Self balancing tree's have less efficient writes (since they need to find where to place nodes and do some restructuring), but the idea is that reads are much more efficient

Self-balancing trees hope to ensure **O(log n)** time complexity for operations like search, insertion, and deletion. The key goal is to avoid degeneration into a linked list.

### Summary Table

| Tree Type     | Balanced By         | Insert/Delete Cost | Read Speed | Write Amplification | Best For                  |
|---------------|---------------------|---------------------|------------|----------------------|---------------------------|
| Red-Black     | Node coloring       | Moderate            | Good       | Low                 | General-purpose, language libs |
| AVL           | Node height         | Higher              | Best       | High                | Read-heavy workloads       |
| B/B+ Tree     | Node fanout/splits  | High (disk-aware)   | Excellent  | Medium–High         | Disk systems, DBs          |

## Types
The rest of the stuff below is ChatGPT generated stuff, TLDR; many types with different read and write amplifications and use cases, all to ensure degeneration of sorted Linked List

### Red-Black Tree (RBT)

- **Type**: Binary Search Tree (BST)  
- **Balance via**: Color properties (Red or Black) and rotation  
- **Properties**:
  1. Each node is either red or black.
  2. The root is always black.
  3. Red nodes cannot have red children (no two reds in a row).
  4. Every path from a node to descendant leaves has the same number of black nodes.
- **Performance**:
  - Insertion and deletion: O(log n), with fewer rotations than AVL.
- **Use Cases**:
  - Widely used in **standard library implementations** (e.g., `TreeMap` in Java, `std::map` in C++).
- **Tradeoff**: Slightly less strictly balanced than AVL trees → fewer rotations but may result in slightly deeper trees.

---

### AVL Tree

- **Type**: Binary Search Tree (BST)  
- **Balance via**: Node height (balance factor of -1, 0, or 1)  
- **Properties**:
  - Each node maintains a balance factor: height(left subtree) - height(right subtree).
  - Tree self-adjusts using single or double rotations after insert/delete.
- **Performance**:
  - Faster lookup than Red-Black Trees due to stricter balancing.
  - Insert/Delete can be more expensive due to rebalancing.
- **Use Cases**:
  - Systems where **read-heavy access** is prioritized (e.g., databases, file indexes).
- **Tradeoff**: More rotations and updates per insert/delete → can amplify writes.

---

### B-Tree (and B+ Tree)

- **Type**: Multi-way (not binary) Search Tree  
- **Balance via**: Splitting and merging nodes when they become too full/empty  
- **Properties**:
  - Nodes can have multiple keys and children.
  - Maintains sorted keys and allows fast range queries.
  - All leaves are at the same depth (perfectly balanced).
  - **B+ Tree**: Internal nodes only store keys; all values are in the leaves, which are linked for range scans.
- **Performance**:
  - Optimized for disk-based systems by minimizing disk I/O.
  - Read/write are still O(log n), but with large "fan-out" (more keys per node → shallower trees).
- **Use Cases**:
  - **Databases, filesystems, key-value stores** (e.g., MySQL, PostgreSQL, LevelDB).
- **Tradeoff**: More complex insert/delete logic; needs buffer/page management.

---

## Write Amplification vs Read Efficiency

### Write Amplification

- **Definition**: When a single logical write causes multiple physical writes on storage.
- **Causes in trees**:
  - Rebalancing (rotations, node splits/merges)
  - Updating internal structures (e.g., heights, balance factors)
  - Disk-based systems: page writes due to small changes
- **Which tree is most write-amplifying?**
  - **AVL Tree**: Strict balancing causes more frequent rotations
  - **B-Tree**: Page splits/merges in disk can amplify writes (especially in LevelDB/LSM Trees)
  - **Red-Black Tree**: Less aggressive balancing → lower write amplification
- **Mitigation**:
  - Use batched inserts or write-optimized data structures (e.g., LSM Trees)
  - Buffer changes in memory (write-ahead logs, caches)

### Read Efficiency

- **Definition**: How fast and efficiently data can be located and read from the tree.
- **Influencing factors**:
  - Tree height (lower = fewer comparisons)
  - Node layout (in-memory vs disk pages)
  - Locality (cache-friendliness, range scan support)
- **Comparison**:
  - **AVL Tree**: Most balanced → best read performance (shallowest height)
  - **B+ Tree**: Excellent for range scans (linked leaf nodes)
  - **Red-Black Tree**: Slightly deeper than AVL → slightly less efficient reads
- **Optimization**:
  - Use B+ Trees for disk and range efficiency
  - Cache top levels or index pages in memory

---

