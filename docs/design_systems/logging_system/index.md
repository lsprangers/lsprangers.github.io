---
layout: technical
title: SaaS Logging System Product
category: Design Systems
difficulty: Advanced
---

## Logging System
So there was a disgusting take home assignment posted in a reddit thread, described [in problem statement](/docs/design_systems/logging_system/PROBLEM_STATEMENT.md#code-challenge-audit-log-api) and I'm mostly going to try to scope things out and do it here over the course of weeks / months / never do it

## Requirements
From a high level after checking it out, seems that it's looking for something similar to Datadog where:
- Include clients in general infrastructure around distributed components
    - Clients are simple HTTP at first
    - Eventually evolve into streaming abilities as well
- Clients are able to call into central audit service to interact in typical CRUD fashion
- Multi-tenant meaning that they may be actually trying to create just the central component and selling it, similar to datadog, and client SDK's are used by customers
- Full blown authorization, security, user management, billing, and all of that crap
    - Meaning there'd need to be complete other teams working on auth, security, user management, etc
- ***They basically asked someone to create a multi-tenant SaaS audit / logging product***
- Separate services from core service:
    - Searching logs
    - Analytics over logs
    - Exporting logs / analytics

---
### First Thoughts
- This is datadog, and the most important piece of this is data storage and retrieval
- The entire thing is storing gigantic amounts of data, making it viewable, and making it searchable / aggregable at some level

### Functional Requirements
Literally 80 billion functional requirements, not going to cover any of them here they're in problem statement

### Non Functional Requirements
These are all the basics...
- Available
- Scalable
- Durable
- They say consistent, but that's just dumb we'll say eventually consistent
- Ton of other stuff, but TLDR it needs to be sell-able to clients

## Layers
Each layer will also need to handle multi tenancy and client isolation, client data can't "touch" eachother or be physically together, and all services need to ensure authentication and authorization to all data assets 

So there are 3 major layers in here to focus on:
- ***Data***: 
    - Need multiple database / data storage components for each of the separate services, but that can be done with typical components seen before
    - The hardest part of this will be data isolation by client which is do-able but forces clients do be the first partition in any database setup
- ***Infrastructure***:
    - Major choices are K8's and running your own, using some cloud components / resources, or using a hybrid approach
- ***Application***:
    - Purely the application code that interacts with the Data Layer, and both of them sit on top of the Infrastructure Layer

---
- ***Components***
    - AWS Components:
        - ***Cognito*** for user authentication and authorization, and is a serverless component so it doesn't need to be on our infrastructure layer, and will only interact with the application layer
            - JWT web based access
            - Company / user segregation
            - Sync with on prem AD groups if they have them
            - Scalable, available, etc - covers the requirements
        - ***EKS*** for container management can be considered an infrastructure component
            - We're going to have to host some middleware / API's, so EKS will be our container orchestration and scaling choice
            - ECS is fine, but it's scaling metrics and vocabulary are annoying
            - Control plane lives in AWS VPC on their EC2's, and EKS control plane will spin up EC2's and containers on our VPC
                - Therefore, this is apart of the infrastructure layer as it doesn't care about app code, it'll just put up apps based on metrics
        - ***API Gateway*** for initial request handling and routing
            - Helps with user flow
                - Integrates with Cognito for authentication and authorization
                - Sets up sessions to be forwarded appropriately to different services
            - Scalable routing out of the box
                - Highly available service that integrates with ECS and EKS
            - Helps to implement a service mesh out of the box that can route calls to EKS services that also scale up or down
                - No need for us to setup service discovery, DNS, health checks (outside of configs), or anything else
            - API GW also supports both HTTP and WebSockets streaming, but sounds like this may be an issue later on since the log streaming back to clients is closer to more SSEvents and not dual-way communication
                - Nevermind, they specifically mentioned WebSockets  
                