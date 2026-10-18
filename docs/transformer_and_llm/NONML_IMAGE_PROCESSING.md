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
[Selective Search](/arxiv_papers/selectiveSearch.pdf) is a deterministic way to segment regions of an image. It's widely used in CNN architectures, specifically [FastRCNN](/docs/transformer_and_llm/CNN.md#fastrcnn). **Selective search proposes a number of bounding boxes that could potentially have an object**

Selective search is a recursive greedy algorithm based on heuristics:
- Generate an [initial set of regions](#initial-regions-of-interest---efficient-graph-based-image-segmentation) based on [arxiv paper efficient graph based segementation](/arxiv_papers/efficient-graph-based-image-segmentation.pdf), call these $\text{init}_{iroi}$ with size $\text{n}_{iroi}$
- Greedily combine regions until there is only 1 final region
    - From set of regions, choose two that are most similar
    - Combine them into a single, larger region
        - Every single iteration reduces the total count of distinct regions by exactly one

Let's say initially 950 regions are proposed, on the first loop 2 will be merged so there are 948 regions that didn't change, and 1 new region. In total there are 951 total regions that have been proposed, so the response at $t=2$ would be a list of size 951

The algorithm records every single bounding box generated at every step of the hierarchy along the way. Once the loop finishes and the tree is complete, the total accumulated list of historical bounding boxes (often capped at the top 2,000 most confident proposals for architectures like R-CNN) is returned as the final output

![Selective search progress](/img/selective_search_progress_and_output.png)

Ultimately it uses deterministic similarity heuristics to combine regions. The TLDR is color differences, shade differences, solid lines, etc are all ways to compare similarities of regions

![Small fine regions of interests](/img/small_fine_regions_of_interests_efficient_graph_segmentation.png)

#### Initial Regions of Interest - Efficient Graph Based Image Segmentation
Initial image regions of interests / segements are based on the [arxiv paper efficient graph based segementation](/arxiv_papers/efficient-graph-based-image-segmentation.pdf), which models a photo as an undirected graph and merges pixels into regions based on a bottom-up greedy approach. It utilizes a [minimum spanning tree](/docs/dsa/8.%20trees%20&%20graphs/index.md#minimum-spanning-tree) to build connected regions using difference calculations. It compares the internal difference of a region to neighboring regions, and merges regions together if the between-region edge difference is $\leq$ the internal difference
- The internal difference is the largest edge weight inside of a region
- Between region difference is calculated as the minimum difference between any 2 regions edges

![Deterministic Initial Regions of Interest](/img/deterministic_regions_of_interest_methods.png)

The calculation is modeled as:
- Initially the graph $G$ is represented by every pixel $v_i \in V$ as a node, and edges connect nodes $e_{i,j} \in E$
    - Initially the edges are 4-based (up, down, left, right) or 8-based to include corners
- Each edge weight $w(e)$ represents the dissimilarity (e.g., absolute intensity or color difference) between two pixels / nodes
    - $w(v_i,v_j)=|{I(v_i)−I(v_j)|}$
    - Can change whether it's grayscale or colored image
- All edges $E$ are sorted into non-decreasing order of their weights $w(e)$ via a heap or counting sort
- The algorithm iterates through the sorted edges and maintains components using a [disjoint-set data structure (Union-Find)](/docs/dsa/8.%20trees%20&%20graphs/index.md#disjoint-set)
    - Nodes are merged based on difference criteria
    - $\text{Internal}(c) = \text{Max}(w(e) \forall e \in c)$ is juts the largest edge weight inside of the component
    - $\text{Diff}(c_1, c_2) = \text{Min}_{{v_i \in c_1},{v_j \in c_2}, (v_i, v_j) \in E} w(v_i, v_j)$ 
    - Nodes merged if $\text{Diff}(c_1, c_2) \leq \text{Min}(\text{Internal}(c_1) + \tau({c_1}), \text{Internal}(c_2) + \tau({c_2}))$
        - $\tau(c) = {k \over c}$ is a separate metric that prefers smaller regions. The denominator represents the count of pixels in a component
        - This formula essentially will merge two components if the differences between those two regions are less than an already connected part of either component