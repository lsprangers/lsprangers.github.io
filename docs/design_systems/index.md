---
title: Architecture & Systems Design Examples
layout: default
---

## Systems Design
Most of this section is around prepping for interview Sys Design questions

This section is around using the below architecture components and implementations to build out high level systems design - common to what is seen in interviews:
- [Architecture components](/docs/architecture_components/index.md): Which are examples of production grade components for messaging, event based architecture, communication protocols, database storage, and other items
- [Typical reusable resources](/docs/architecture_components/typical_reusable_resources/index.md): Which are examples of these architecture components built from ground up
    - Under here are:
        - In memory implementations
        - Distributed implementations
            - In memory node + some manager and scaling

![Search System](/img/SysArchTemplate-ECommerce%20Search%20System.drawio.png)

---
Some of the better examples so far:
- [Search system](/docs/design_systems/search_system/index.md) which is a representation of a generic E-Commerce website search and recommendation system on user login
- [Video recommendations](/docs/design_systems/video_recommendations/index.md) for recommending videos on a users feed (like Youtube)
- [Video serving (Youtube)](/docs/design_systems/youtube/index.md) showcases serving of actual videos with different encodings and features enables
- [Peer-to-peer](/docs/design_systems/p2p/index.md) describes a peer-2-peer filesharing service

### General Notes
There are some things that are generally true across system design questions

#### Functional Requirements
Functional requirements demonstrate ***how a system should behave***

These requirements describe what the system should do, such as "allow POST request to create a new User" or "be deployed in multiple partitioned regions for GDPR compliance" 

These are the sorts of requirements you'd get from a product manager or some form of stakeholder, and then you'd need to design a system with other engineers given current environment

#### Non-Functional Requirements
Non-Functional requirements describe ***how a system should perform***

Non Functional requirements, I think, are things that are supposed to be derived from [Functional Requirements](#functional-requirements)...a NFRequirement of "Scalable" could be inferred from "Needs to be deployed to all users" where you know that there are millions of concurrent users at any time



##### Scalable
This usually just means it's going to be called a lot, and so we'll need partitions, meaning there are tradeoffs on the Availability-Consistency spectrum you need to choose
    - Almost every system always needs to be scalable, i.e. needs partitions, i.e. has main trade-offs between availability and consistency

##### Durable
Basically you need to write to disk somewhere

##### Availability-Consistency During Network Partition
When you know you want a scalable, partitioned system you then need to choose what happens in the worst case (i.e. when there are breaks between the partitions)
    - When our partitions can't talk to each other do you keep the entire system up (Available) even if some of the nodes can't talk to each other (not Consistent)
    - Or do you ensure the system stays in it's last known Consistent state, but can't serve some requests (not Available)

##### Availability-Consistency In General
Generally you still need to choose between highly performant availability, and linearizable consistency, or something inbetween
    - The typical example is read replicas of databases
    - If you have N read replicas, and there's 1 leader and N-1 replicas, do you allow those N-1 to serve reads after the 1 may have gotten a new write?
        - If you do we're choosing highly performant and highly available over strict consistency

***There are ways to handle all of these trade-offs, and the Availability-Consistency spectrum spans a large space that's covered by many database types, isolation levels, and choices - all of them are useful in different scenarios***
