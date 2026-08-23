---
layout: technical
title: GPU Usage
category: ML Systems, Hardware, and Code
difficulty: Advanced
description: Discussions around NN's, Transformers, LLMs, and other topics
show_back_link: true
---

# GPU Usage
GPU usage for modern ML systems is mostly split between training and inference

In training you run distributed pipelines to feed data into distributed gradient descent on GPU's, GPU's really just act like a gigantic bus shoveling tons of data through to update model weights. Inference is slightly different since you're most likely serving it behind an API, and you need to use some API metrics like P99 latency to ensure the request / response of the API is small enough. You still need to use clever batching techniques as copying data to and from GPU is expensive, but it's a different game compared to training where you just shovel as much data in as the GPU can handle

[NSight Systems](/docs/llm_systems/gpu_course/index.md#profiling-cuda-applications) is the NVIDIA tool for profiling CUDA applications, which is a good example of how to monitor GPU / CPU applications and the usage, memory footprint, etc of each of them. It's similar to the Spark UI where knowing how to read it can give insight on spill, skew, and inefficiencies

## GPU Monitoring and Metrics
Most GPU metrics will be sourced from [CUDA API](/docs/llm_systems/gpu_course/index.md) backends, specifically with NVIDIA GPU Manager or some other OTEL service like datadog

Profiling these metrics to figure out what's going on is