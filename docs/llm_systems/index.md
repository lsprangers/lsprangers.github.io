---
layout: technical
title: ML Systems, Hardware, and Code
category: ML Systems, Hardware, and Code
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
