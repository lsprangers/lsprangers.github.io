---
title: Ray
category: Other Concepts
difficulty: Advanced
description: Ray
show_back_link: true
---

## Ray
Ray is another open source framework for scaling AI and Python applications, typically used in parallel processing for ML workloads

Most Python multiprocessing is done utilizing `multiprocessing` in tutorials and other demonstrations, but actually creating a distributed Python application with communication overhead, data shuffling, network I/O, high availability, etc requires something a bit more robust - this is the use case of Ray 

Ray focuses on taking functions and classes from typical Python programs, and translating them into ***tasks and actors***
- Tasks are the unit of work scheduled by Ray and correspond to one function invocation or method invocation
- Actors are then the nodes themselves, or potentially singular CPU / GPU on nodes, that perform tasks
- To perform tasks, actors need a few things:
  - Shared memory stores help to share objects between workers without creating copies
  - In memory databases for storing metadata about other workers
  - Local network `eth0` access or some sort of networking device

TODO: Need to extend this with unstructured processing and inference pipelines which is what it's mostly used for

### Tasks
To actually run a function `func()` as a parallel, remote, and / or asynchronous call it needs to be decorated with `@ray.remote` - these will return futures, and then the actual function call will take place in the background as a Task

Tasks can then depend on other tasks, and so forcing one task to be dependent on others means it won't execute until the dependent ones return - i.e. **tasks are a DAG**

### Actors
Classes are extended to be actors with the same `@ray.remote` decorator. Whenever the new class is instantiated, Ray created a new Actor which is mostlt just a process that runs somewhere in the cluster, as scheduled by the scheduler, and holds a copy of the object

Method invocations on that actor turn into tasks that run on the actor process and can access and mutate the state of the actor. Therefore, actors have mutable state that can be shared across tasks that it runs. Individual actors execute methods serially like a normal Python process does, and so there aren't any race conditions inside of an actor

Therefore parallelism can be created by having multiple actors! Simply having multiple of them draining queue's and processing images, handling inference calls to respond with GPU based models, etc! It's all similar to running multiple python workers / processes, the major difference is in sharing objects / state across the actors in an efficient way and scheduling work to be done

#### Actor Handles
Actor handles allow other actors / tasks to invoke methods (start tasks) on the initial actor - meaning if actor B wants to start a task on actor A it can invoke actor A's handle

This can naturally be used for having a central queue actor, having a central message actor, etc that gets pushed to or pulled from