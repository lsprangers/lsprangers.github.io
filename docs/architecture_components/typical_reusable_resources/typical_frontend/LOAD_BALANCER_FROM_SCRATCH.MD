---
layout: technical
title: Load Balancer From Scratch
category: Architecture Components
difficulty: Advanced
description: Architecting a Frontend Solution
---

## Load Balancer From Scratch
So in the above main file, we sort of skip over how an actual load balancer would be created from scratch

You'd ultimately need something that can take in requests, and forward to specific targets based on some rules, and upon scaling needs to register itself with specific DNS servers

This is not a trivial thing to do, and starts to depend on central service registries like ZooKeeper + ETCd to keep things together

### Functional Requirements
- What should this do from an end user perspective? What can I do to interact with it?

### Non-Functional Requirements
- Availability: 
- Durability: 
- Scalability: 
- Throughput: 
- Reliability: 
- Consistency: