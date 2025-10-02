---
layout: page
sidebar_position: 1
title: Technical Content
description: A collection of technical notes, implementations, and concepts
---

# 📚 Tech Notes

Why this? I had this all in word docs when I was going through interviews, so figured I'd put it in here somewhere

It's a mix of **Data Structures and Algorithms (DSA)**, **System Design**, **Machine Learning concepts**, and more. 

It's a structured dump of stuff I've pulled out of old word files and tweaked into linkable artifacts

---

## Highlights
Some of the better displays on here:
- [Typical reusable resources](/docs/architecture_components/typical_reusable_resources/index.md) which are examples of architecture components built from ground up
  - In memory implementations
  - Distributed implementations
      - In memory node + some manager and scaling
- [Pregel Graph Processing](/docs/other_concepts/graph_processing/PREGEL.md) and how I've used it in large analytics based product companies
- [Video Recommendations](/docs/design_systems/video_recommendations/index.md) which showcases a specific example of what's talked about in [Generic Search Systems](/docs/design_systems/search_system/index.md)
- [Spark Notes](/docs/other_concepts/SPARK.md)
<!-- - [Delta Sharing Data Feeds](TODO) -->
<!-- - [High Throughput Ads Experimentation System] -->
- Outside of these it's mostly a dump of notes around DSA, Systems Design, Leetcode, and other junk

## Architecture and Systems Design Examples

This section focuses on building specific systems, often inspired by technical interviews or real-world use cases. Examples include URL shorteners, YouTube Search, Top K Heavy Hitters, and more.



## Architecture Components
To implement these systems, you'll find notes under Architecture Components about databases, messaging, calculations, and other essential components.

There's also an entire section on [Typical Resources](/docs/architecture_components/typical_reusable_resources/index.md) where we build all of the typical components from scratch such as:
- Distributed Key-Value Stores
  - Front-end Load Balancers with Metadata
  - Distributed Queues
  - Distribued Logging
  - etc..
- Some includes Kubernetes (K8s) and Terraform configurations to demonstrate how to create these systems natively

---

## Data Structures & Algorithms

This section contains:
- General Data Structures and Algorithms.
- Their implementations, time/space complexities, and use cases.

---

## Other Concepts

This section includes generic concepts that don't fit into DSA or System Design, such as:
- Parallel Training Designs.
- Pregel Graph Traversals.

These are useful but don't belong in the other categories.

---

## Implementations

A collection of generic implementations, including:
- A Key-Value Store with Transactions.
- A Balanced Binary Search Tree from Scratch.
- ML Feature Store Architecture Diagram.

---

## Leetcode

This is a dump of LC problems and comments

---

## Arxiv
These are just papers I've read marked up with highlighter - my old iPad died and brought these here

---

## References

These are some of the resources I frequently use and reference throughout this repo:

- [Leetcode](https://leetcode.com): Great for DSA and Systems Design problems. I probably used this the most.
  - [Segment Tree](https://leetcode.com/articles/a-recursive-approach-to-segment-trees-range-sum-queries-lazy-propagation/)
- [3Blue1Brown](https://www.3blue1brown.com/): Amazing visual explanations for Linear Algebra, Probability, and Deep Neural Networks.
  - Highly recommend the [Attention](https://www.youtube.com/watch?v=eMlx5fFNoYc&vl=en) video for understanding Transformers.
  - Also I use their [Manim](https://docs.manim.community/en/stable/tutorials/quickstart.html) package for my own animations now
- [Jay Alammar's Visual Transformer Paper](https://jalammar.github.io/illustrated-transformer/): A fantastic resource for understanding Attention and Transformers.
- [Yuan Meng Embeddings Post](https://www.yuan-meng.com/posts/ebr/)
  - Useful for seeing the actual topological interpretations of embeddings, and why geomtric / metric space operations are allowed
- [Google ML Rec Systems](https://developers.google.com/machine-learning/recommendation): Useful for search, recommendation systems, and embeddings.
  - [Google Two Tower Article](https://cloud.google.com/blog/products/ai-machine-learning/scaling-deep-retrieval-tensorflow-two-towers-architecture)
- [Hello Interview](https://www.hellointerview.com): Great for Systems Design interview preparation.
- [Programiz](https://www.programiz.com): Excellent for DSA implementations and complexity analysis.
- [Medium Articles]
  - [NVIDIA Recommender Systems](https://medium.com/nvidia-merlin/recommender-systems-not-just-recommender-models-485c161c755e)
- [Spark]
  - [Spark on Cloudera 1](https://blog.cloudera.com/how-to-tune-your-apache-spark-jobs-part-1/)
  - [Spark on Cloudera 2](https://blog.cloudera.com/how-to-tune-your-apache-spark-jobs-part-2/)
  - [Spark on Cloudera 3](https://queirozf.com/entries/apache-spark-architecture-overview-clusters-jobs-stages-tasks)
  - [RDD vs Dataframe vs Dataset](https://www.databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html)
- [Spark Streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
  - [Spark Streaming](https://www.databricks.com/blog/2015/07/30/diving-into-apache-spark-streamings-execution-model.html)
  - [Spark Kubernetes](https://www.linkedin.com/pulse/spark-kubernetes-practitioners-guide-mich-talebzadeh-ph-d-)
- [Udemy AWS Solution Architect Course](https://www.udemy.com/course/aws-solutions-architect-professional/)
- [Cassandra]
  - [IntelliDZine Blog Post](http://intellidzine.blogspot.com/2013/11/cassandra-data-modelling-tables.html)
  - [Pantheon Secondary Indexes Pitfalls](https://pantheon.io/blog/cassandra-scale-problem-secondary-indexes)
- [Jay Alammar Illustrated]
  - [Transformer](https://jalammar.github.io/illustrated-transformer/)
  - [GPT2](https://jalammar.github.io/illustrated-gpt2/#part-2-illustrated-self-attention)
  - [SebastianRaschka](https://sebastianraschka.com/blog/2023/llm-reading-list.html)
- [LayerNorm](https://h2o.ai/wiki/layer-normalization/)
- [Another persons blog - AmitNess](https://amitness.com)
- [TRYEXCEPT - ML Systems Design Interviews](https://www.youtube.com/@TryExcept-10110)
- [Succinct data structures](https://blog.startifact.com/posts/succinct/)
- [Duke Stats 732 Paper on Choosing Priors](https://www2.stat.duke.edu/courses/Spring13/sta732.01/priors.pdf)
- [Sebastian Raschka LLM Reading List](https://sebastianraschka.com/blog/2023/llm-reading-list.html)
- [Encord - Contrastive Learning](https://encord.com/blog/guide-to-contrastive-learning/)
- [MinHash](https://spotintelligence.com/2023/01/02/minhash/)
- [MinHash + LSH](https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/)
- [Google Two Tower AI Blog](https://cloud.google.com/blog/products/ai-machine-learning/scaling-deep-retrieval-tensorflow-two-towers-architecture)
- [Multi Model Blog](https://slds-lmu.github.io/seminar_multimodal_dl/c02-00-multimodal.html)
  - [NLP + CV](https://slds-lmu.github.io/seminar_multimodal_dl/c01-00-intro-modalities.html#c01-01-sota-nlp)
- [Vinija Jain Blog](https://vinija.ai/)
- [Cloudflare Load Balancing](https://developers.cloudflare.com/reference-architecture/architectures/load-balancing/)
---