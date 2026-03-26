---
layout: technical
title: LLM Systems, Hardware, and Code
category: LLM Systems, Hardware, and Code
difficulty: Advanced
description: Discussions around NN's, Transformers, LLMs, and other topics
show_back_link: true
---

## LLM Systems, Hardware, and Code

In the [transformer and llm](/docs/transformer_and_llm/index.md) section, we cover the theory behind LLM's, [Transformers and Attention](/docs/transformer_and_llm/TRANSFORMERS.md), and specific models like [BERT](/docs/transformer_and_llm/BERT.md) and [GPT](/docs/transformer_and_llm/GPT.md). In this section, we cover the systems, hardware, and code that make it possible to train and run LLM's at scale, and talk about some of the systems behind them like training, inference, optimizations, and more

There's a great [example of utilizing an event loop in Python / Go and C++ infrence process on GPU's in a monolithic way to have 8 models running on a single VM to handle a high concurrency and low latency inference system in a monolith](/docs/event_driven_architecture/event_driven_software/EVENT_LOOP.md#low-latency-monolith-deployment). This ties into showcasing [Triton](https://github.com/triton-inference-server/server/tree/main/docs/user_guide), which is an open source NVIDIA software package that handles all of this for us on NVIDIA GPU's

![GPT, BERT, and Others](/img/gpt_bert_others.png)

![BERT vs GPT](/img/bert_vs_gpt.png)

### Training
[LLM Training](/docs/llm_systems/LLM_TRAINING.md) is done over gigantic corpa of data, and requires a lot of compute. We talk about the systems behind training, including data pipelines, distributed training, and more

Most of these systems have Human In The Loop components where human feedback is used to improve the model, and that will get into how a sentence with multiple potential outputs is framed as a reward function for the model to optimize for, and how that is used in practice to train LLM's

Various training datasets are used, mostly around sourced web content from social media, online encyclopedias, and structured curated text
![LLM Training Dataset Sources](/img/llm_training_dataset_sources.png)

### Metrics
- ***Utilization*** = Output achieved $\div$ Capacity paid for
- ***GPU Allocation Utilization*** = GPU-seconds running application code $\div$ GPU-seconds paid for
- ***GPU Kernel Utilization*** = GPU-seconds running kernels $\div$ GPU-seconds paid for

When utilizing GPU's, there are a few metrics to use to figure out how much you get out of it. The time to actually reserve, setup, and place code onto a GPU is known as **Allocation**, and then once code is sitting on the GPU the actual utilization of SIMD processing, which is commonly known as **kernel compute**, showcases our actual ability to use the GPU for what it's best for

Just because an allocated GPU is running application code doesn’t mean it is running code on the GPU. The term of art for “code that runs on the GPU” in the popular CUDA programming model for GPUs is “kernel”, and so we call the fraction of time we spend running code on the GPU the GPU Kernel Utilization

This utilization metric is reported by, among others, the beloved `nvidia-smi` command line tool wrapping NVIDIA’s Management Library for their GPU hardware, and so it is commonly checked and cited

## References
Wanted to give explicit references here because a lot of this has come from various websites, but pulled info from specific book below

[Sebastian Raschka Book](https://www.manning.com/books/build-a-large-language-model-from-scratch) was a great resource, along with some of his personal website and blog posts
- [Sebastian Raschka LLM Reading List](https://sebastianraschka.com/blog/2023/llm-reading-list.html)
- etc..
