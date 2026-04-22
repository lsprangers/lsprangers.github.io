---
layout: technical
title: Parquet
category: Architecture Components
difficulty: Advanced
description: Discussion around Disk Based Databases
---

# Parquet

# Delta

## Incremental Reads AS OF
So if you picture `AS OF VERSION 5000` in Delta, the engine is not usually doing:
- `read 00000000000000000000.json`
- `read 00000000000000000001.json`
- ...
- `read 00000000000000005000.json`

Instead it is more like:
- find the latest checkpoint at or before version 5000,
- load that checkpointed table state,
- replay only the JSON commits after that checkpoint up to 5000,
- get the active file set for version 5000,
- then plan the scan over those files

That is why the metadata machinery exists: it turns “huge append-only file pile” into “here is the exact active file set for this version.”