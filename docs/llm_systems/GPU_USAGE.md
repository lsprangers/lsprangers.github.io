---
layout: technical
title: GPU Usage Metrics in LLM Systems
category: LLM Systems, Hardware, and Code
difficulty: Advanced
description: Discussions around NN's, Transformers, LLMs, and other topics
show_back_link: true
---


### GPU Metrics
- ***Utilization*** = Output achieved $\div$ Capacity paid for
- ***GPU Allocation Utilization*** = GPU-seconds running application code $\div$ GPU-seconds paid for
- ***GPU Kernel Utilization*** = GPU-seconds running kernels $\div$ GPU-seconds paid for

When utilizing GPU's, there are a few metrics to use to figure out how much you get out of it. The time to actually reserve, setup, and place code onto a GPU is known as **Allocation**, and then once code is sitting on the GPU the actual utilization of SIMD processing, which is commonly known as **kernel compute**, showcases our actual ability to use the GPU for what it's best for

Just because an allocated GPU is running application code doesn’t mean it is running code on the GPU. The term of art for “code that runs on the GPU” in the popular CUDA programming model for GPUs is “kernel”, and so we call the fraction of time we spend running code on the GPU the GPU Kernel Utilization

This utilization metric is reported by, among others, the beloved `nvidia-smi` command line tool wrapping NVIDIA’s Management Library for their GPU hardware, and so it is commonly checked and cited