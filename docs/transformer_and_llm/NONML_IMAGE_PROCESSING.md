---
layout: technical
title: Non-ML Image Processing
category: NLP, CV, and Transformers
difficulty: Advanced
description: CNN Foundations, ResNet, and DenseNet Architectures
show_back_link: true
---

## Non-ML Processing
In a large number of CNN, Transformer, Multimodal, etc architectures there's a fair amount of non-ML processing that is utilized for features

Most of this revolves around deterministic algorithms with hand created criteria for segmentation, line identification, bounding boxes, etc

### OpenCV
[OpenCV](https://docs.opencv.org/4.13.0/index.html) is a humongous open source project that has most of these algorithms / feature creation as out of the box classes that are able to be ran on local images

### Selective Search
[Selective Search](/arxiv_papers/selectiveSearch.pdf) is a deterministic way to segment regions of an image. It's widely used in CNN architectures, specifically [FastRCNN](/docs/transformer_and_llm/CNN.md#fastrcnn)