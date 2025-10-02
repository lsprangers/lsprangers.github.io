---
layout: technical
title: GPT Training Architecture
category: NLP, CV, and Transformers
difficulty: Advanced
description: Discussions around Loss Functions in NN's
show_back_link: true
---

## Training A GPT

### Pretraining
This is typical decoder-only generative training described in [GPT Arch](/docs/transformer_and_llm/GPT.md#architecture)

This involves predicting the next word in a sentence and updating weights accordingly

This is where data is scraped from all over the web into Terrabytes of free-text storage, tokenized, and stored

### Supervised Finetuning
This is also next token prediction, but also utilizes *instruction-output* pairs which are essentially a form of labeled data we'd need humans to create and annotate

The input is the instruction and potentially other context, and it outputs a sentence that we can score against what we'd prefer model to have (desired output)

Creating this desired output is typically done by a human, so we have much less data

### Alignment
This step is to align the LLM with human objectives / priorities

This is where we use [RLHF](/docs/training_and_learning/RLHF.md) 