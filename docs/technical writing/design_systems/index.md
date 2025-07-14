---
title: Design Systems
layout: default
---

## General Notes
There are some things that are generally true across system design questions
#
## Functional Requirements
These requirements describe what the system must do, such as "allow POST request to create a new User" or "be deployed in multiple partitioned regions for GDPR compliance" 

These are the sorts of requirements you'd get from a product manager or some form of stakeholder, and then you'd need to design a system with other engineers given current environment

### Non-Functional Requirements
Non Functional requirements, I think, are things that are supposed to be derived from [Functional Requirements](#functional-requirements)...a NFRequirement of "Scalable" could be inferred from "Needs to be deployed to all users" where we know that there are millions of concurrent users at any time



#### Scalable
This usually just means it's going to be called a lot, and so we'll need partitions, meaning there are tradeoffs on the Availability-Consistency spectrum we need to choose
    - Almost every system always needs to be scalable, i.e. needs partitions, i.e. has main trade-offs between availability and consistency

#### Durable
Basically we need to write to disk somewhere

#### Availability-Consistency During Network Partition
When we know we want a scalable, partitioned system we then need to choose what happens in the worst case (i.e. when there are breaks between the partitions)
    - When our partitions can't talk to each other do we keep the entire system up (Available) even if some of the nodes can't talk to each other (not Consistent)
    - Or do we ensure the system stays in it's last known Consistent state, but can't serve some requests (not Available)

#### Availability-Consistency In General
Generally we still need to choose between highly performant availability, and linearizable consistency, or something inbetween
    - The typical example is read replicas of databases
    - If we have N read replicas, and there's 1 leader and N-1 replicas, do we allow those N-1 to serve reads after the 1 may have gotten a new write?
        - If we do we're choosing highly performant and highly available over strict consistency

***There are ways to handle all of these trade-offs, and the Availability-Consistency spectrum spans a large space that's covered by many database types, isolation levels, and choices - all of them are useful in different scenarios***

### Typical Patterns
Almost every single system a set of similar patterns, and there are components listed throughout our repo for "typical reusable" components such as frontend infra, queue, KV store, and cache

