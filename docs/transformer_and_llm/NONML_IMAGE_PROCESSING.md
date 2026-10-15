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

Selective search is a recursive greedy algorithm based on heuristics:
- Generate an initial set of segments based on [arxiv paper efficient graph based segementation](/arxiv_papers/efficient-graph-based-image-segmentation.pdf)
- Greedily combine regions
    - From set of regions, choose two that are most similar
    - Combine them into a single, larger region
    - Repeat while any regions have been merged

![Selective search progress](/img/selective_search_progress_and_output.png)

#### Initial Regions of Interest
Initial image regions of interests / segements are based on the [arxiv paper efficient graph based segementation](/arxiv_papers/efficient-graph-based-image-segmentation.pdf), which ultimately uses deterministic heuristics to segment regions. The TLDR is color differences, shade differences, solid lines, etc are all ways to initially segment out an image, typically the idea is to over-segment where no 2 regions from different segments are grouped together

Hypothetically, each pixel could be it's own segment, but these heuristics allow us to create fine grained regions of interest, and then selective search is designed to recursively join these smaller regions of interests into true segments

![Small fine regions of interests](/img/small_fine_regions_of_interests_efficient_graph_segmentation.png)