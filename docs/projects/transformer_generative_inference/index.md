---
layout: technical
title: Transformer LLM Real Time Inference
category: Projects
difficulty: Advanced
description: Project Showcases
show_back_link: true
---

# Transformer LLM Real Time Inference
This is mostly a showcase of a lot of the stuff that's been done in my job for transformer (NLP), embeddings (NLP), image segmentation, and multi-model tasks

A large amount of these models are served as HTTP endpoints which are called in large scale batch, or real time streaming pipelines. That also makes them useful for HTTP request / responses as well from clients, and most of these setups handle both gracefully as they don't really care where the request is coming from. Large batch pipelines in spark utilize `forEachBatch` as to not overwhelm the system, and HTTP clients utilize asynchronous HTTP `GET` calls - at the end of the day it's all the same

Anything real-time (under 20ms) is handled by NVIDIA Triton Servers. An example of the theory behind these lives in the [ML Inference Example under event driven architecture](/docs/event_driven_architecture/event_driven_software/EVENT_LOOP.md#ml-inference-example) - these are much harder to work with versus generic HTTP API's in something like Go or Java, but the general declarativeness of the framework to utilize GPU's can't be overlooked. For anything else non real-time, most of the time a highly available service in Go or Python is utilized - Go is better at true parallelism + easy to use concurrent data structure, Python has a lot of ML community building on top of it (but bad CPU bound runtimes), and so it's always a toss up. [Ray] is also another great framework for scaling out non real-time ML services, and can be utilized to scale out Python into truly parallel processing that can help run CPU + I/O intensive workloads

We'll cover 3 main examples here:
- **Triton Inference**: Real time use case, scaling patterns, and highly available clusters
- **Go API**: Lightweight model use case, scaling, parallelism, and concurrency, and how highly available clusters look
- **Ray Cluster**: Taking a Python API from `locahost:127.0.0.1` to a distributed inference cluster