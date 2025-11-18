---
layout: technical
title: Graph Neural Networks
category: Graph Neural Networks
difficulty: Advanced
description: Discussions around Graph NN's
show_back_link: true
---


## Graph NN
Graph's as a concept are defined in the [Graph DSA Topic](/docs/dsa/8. trees & graphs/index.md)

Graph Neural Networks (GNN's) can be directly applied to graph data structures, and provide a way to leverage the relationships and connections between nodes for machine learning tasks 

GNN's can operate on the graph level, node level, edge level, or even subgraph level - most of the same common tasks are still used in GNN's such as classification, regression, clustering, imputation, and link prediction

Graphs are typically stored in adjacency matrices, so there's no specific need to do anything special outside of typical matrix deep learning over matrices, but other times graphs are stored as lists of neighbors and traversing means iterating over all edges in total (i.e. neighbors of an unseen node)
- A dense adjacency matrix gives immediate access to linear algebra style operations (matrix multiplications) that can exploit highly efficient and optimized parallel computations
- A dense matrix is memory-intensive for large ***sparse*** graphs, where it stores a large amount of zero's, when compared to adjacency lists / edge lists
    - An adjacency matrix stores $O(v^2)$ space, where adjacency lists store $O(v + e)$ space

Ideally, graph calculations can reuse concepts from linear algebra over matrices, without storing large sparse matrices with redundant information

In the real world implementations, a majority of graphs are stored as sparse matrices using efficient formats that don't store all the zero entries explicitly, such as Compressed Sparse Row (CSR) or Compressed Sparse Column (CSC) formats, or as an edge list (two arrays of source / target indices). These formats still allow for linear algebra benefits, like running parallel linear algebra operations over them, or they utilize parallel graph traversal frameworks like [GraphX](/docs/other_concepts/graph_processing/index.md#graphx) or [Pregel](/docs/other_concepts/graph_processing/PREGEL.md)

GraphX and Pregel allow for massively parallel operations in tools like Spark, while utilizing edge list storage formats

### Early Days - CNN's Over Graphs
In the past CNN's were tried over Graphs where you take convolutions over sub-graphs of nodes - CNN's worked well on images, so the thought was that it should be like using CNN over an image with some missing pixels

Pooling layers, convolutions, subsampling, etc allow for CNN's to perform image classifiction, object detection, and many other tasks on images - ultimately fueled by their ability to capture local spatial hierarchies in data

This sliding window approach was thought to be generalizable to graphs as well, but the complex topology of graphs restricts this - images are more rigid with well defined dimensions, whereas graphs can have arbitrary structures and varying node degrees 

Moving forward, GNN's have taken more of a message passing / aggregation approach, where nodes aggregate information from their neighbors to update their own representations - this is the core idea behind many GNN and Parallel Graph Processing frameworks like GraphX and Pregel

## Basics of Graph Neural Networks
A lot of below comes from a few sources:
- [Neptune AI GNN](https://neptune.ai/blog/graph-neural-network-and-some-of-gnn-applications)

### Node Embedding
One of the most common GNN tasks is Node Embedding - where each node in the graph is mapped to a low-dimensional vector space, capturing both the node's features and its structural context within the graph with a goal of mapping similar nodes to nearby points in the embedding space. Similarity in the embedding space should approximate similarity in the graph structure or node attributes

![Node Embedding](/img/node_embedding_example.png)

For this $u$ and $v$ are nodes in the graph, and $z_u = f(u)$ and $z_v = f(v)$ are their respective embeddings. The goal is to minimize a loss function that encourages similar nodes to have similar embeddings - setup would have something like $\text{similarity}(u, v) \approx z_v^T z_u$

The encoder function should be able to:
- Perform locality (local network neighborhood) calculations
- Aggregate information from neighboring nodes
- Stack multiple layers (compute across multiple hops)

Most of these 3 things can be achieved by utilizing graph traversal algorithms, implemented via message passing in scalable parallel frameworks, to aggregate information from neighbors and update node representations

![Graph Propogation](/img/graph_propogation.png)

The locality information can be preserved through message passing, and neural networks can help facilitate the aggregation and transformation of node features during this process - neural networks allow information to be aggregated across layers in a linear and non-linear fashion, simply by doing linear algebra operations. In below freehand NN's are represented by gray boxes, which shows how we can represent a graph as linear transformations over dynamic inputs

![Aggregating Graphs](/img/graph_aggregator.png)

The dynamic input sizes are a problem, if you alter the above representation to one that's more "NN-like", you can achieve the below freehand - it showcases how a Graph NN architecture can be transformed into a feedforward NN architecture

![Graph NN As FeedForward NN](/img/graph_nn_as_feedforward_nn.png)

In the above diagram:
- Each node has a feature vector - $(X_A)$ is the feature vector of node $A$
- The inputs are the feature vectors, and a gray box takes the inputs and applies a linear transformation, aggregates them, and passes them forward to the next layer
    - In Layer-0 above, the input size to the gray boxes is dynamic (some nodes have more or less connections than others)
    - To handle this, the aggregation function needs to be permutation invariant, such as sum, mean, or max, ensuring consistent output size regardless of the number of neighbors

In the forward propagation steps we'd have:
1. Initialize node features: $h_v^{(0)} = X_v$ for each node $v$.
2. For each layer $k = 1, \dots, K$:
    - Neighborhood aggregation (mean): $\bar{h}_v^{(k)} = \frac{1}{|N(v)|} \sum_{u \in N(v)} h_u^{(k-1)}$
        - This equates to "averaging the feature vectors of all neighbors of node $v$ at the previous layer"
        - This layer is permutation invariant, ensuring consistent output size regardless of the number of neighbors - 2 neighbors or 100 neighbors result in same output size
    - Update / combine self and neighborhood: $h_v^{(k)} = \sigma\big( W_k \bar{h}_v^{(k)} + U_k h_v^{(k-1)} + b_k \big)$
        * $W_k$ weights for neighbor messages; $U_k$ self-feature weights; optional bias $b_k$
        * $\sigma$ any non-linearity (e.g. ReLU)
        - We merge the aggregated neighbor information $\bar{h}_v^{(k)}$ with the prior embedding $h_v^{(k-1)}$, which already encodes up to $(k\!-
1)$-hop information
            - Stacking layers expands the receptive field: after $k$ layers, $h_v^{(k)}$ depends (under mean aggregation) on nodes up to $k$ hops away
            - This depth-wise accumulation is analogous in spirit to RNN hidden states carrying context, but the model is still a feed-forward stack
                - It still "drags along" information, but it happens via feed forward NN
            - Only if $K$ exceeds (or matches) the graph diameter will $h_v^{(K)}$ potentially reflect information from every node; otherwise it covers a $K$-hop neighborhood 
                - 1 billion neighbors, all may not be covered..maybe only first 100
3. Final embedding: $z_v = h_v^{(K)}$ after $K$ layers of neighborhood aggregation and transformation

The above equations define a common message-passing / GraphSAGE-style GNN layer, and altogether just facilitate transforming a graph data structure into more feed-forward hierarchical structures that typical NN's "look like"

At the end of the day "message passing" just means we are aggregating info from many neighbors, and graph NN's are just regular NN's except you need a permutation invariant input layer to ensure the number of neighbor's doesn't affect dimension sizes

#### K-Hop Neighborhoods
I wasn't fully clear on the K-hop neighborhood concept, so dove into it a bit more 

Each hop in a K-hop neighboorhood represents a step away from the original node in the graph - so a 1-hop neighborhood includes all nodes directly connected to the target node, a 2-hop neighborhood includes nodes that are two edges away, and so on

In each hop, the nodes aggregate information from their immediate neighbors (1-hop), and as you stack more layers, the receptive field expands to include nodes that are further away (2-hop, 3-hop, etc)

Therefore, if the graph looks like it does below:
```
    A---G
   / \  |
  B   C |
 / \   \|
D   E---F
```

Focusing on node `C`:
- 1-hop neighborhood of `C`: Nodes `A`, `F`
- 2-hop neighborhood of `C`: Nodes `B`, `E`, `G`
- 3-hop neighborhood of `C`: Node `D` (there are actually many more, and most GNN implementations would include all nodes reachable within 3 hops, but this is just a simple example)

Now, for discussing node embeddings based on $K$-hop neighborhoods:
- In one layer, a node aggregates only its immediate neighbors (1-hop) plus possibly itself (if you include self-loops / residual terms).
- After 1 layer, `C`'s embedding $h_C^{(1)}$ depends on its 1-hop neighbors: `A`, `F` (and `C` itself if self features are included).
- After 2 layers, $h_C^{(2)}$ depends on nodes up to 2 hops: original 1-hop (`A`, `F`) and new 2-hop (`B`, `E`, `G`). The earlier neighbors do not disappear—information from them is already mixed into $h_C^{(1)}$ and propagated forward.
- After $k$ layers, $h_C^{(k)}$ depends on all nodes within $k$ hops; it does NOT enumerate every path explicitly, it composes aggregated representations, avoiding exponential blow-up in practice.

Symbolically expanding $h_C^{(k)}$ as nested applications of a generic aggregator $f(\cdot)$ quickly becomes messy and misleading (it double counts nodes and obscures weighting). Instead, modern implementations:
1. Maintain embeddings per layer ($h^{(0)}, h^{(1)}, \dots$)
2. Use a permutation-invariant operator (mean / sum / max / attention) over $N(v)$
3. Combine neighbor aggregate with transformed self embedding
4. Optionally normalize or sample neighbors (GraphSAGE style) to control computation for high-degree nodes

Practical notes:
- Neighbor sampling (limiting per-layer fan-out) prevents combinatorial explosion on power-law graphs.
- Caching 1-hop (and sometimes 2-hop) neighbor aggregates accelerates training for static graphs.
- Increasing $K$ enlarges the receptive field but can cause over-smoothing: node embeddings become indistinguishable as repeated averaging washes out local differences.

Going to write out the formula for 1st and 2nd layer in a k-hop example:
- $m_C^{(k)}$ represents the local aggregation of neighbors for a node
- $h_C^{(k)}$ represents the embedding of node C at layer k
- Layer 0 embeddings for each node:
    - $h_C^{(0)} = X_C$
- Layer 1 (neighbors of C are A, F):
    - $m_C^{(1)} = \frac{h_A^{(0)} + h_F^{(0)}}{2}$
    - $h_C^{(1)} = \sigma\!\left( W_1 \frac{h_A^{(0)} + h_F^{(0)}}{2} + U_1 h_C^{(0)} + b_1 \right)$
- Layer 1 for A (neighbors B, C, G):
    - $m_A^{(1)} = \frac{h_B^{(0)} + h_C^{(0)} + h_G^{(0)}}{3}$
    - $h_A^{(1)} = \sigma\!\left( W_1 \frac{h_B^{(0)} + h_C^{(0)} + h_G^{(0)}}{3} + U_1 h_A^{(0)} + b_1 \right)$
- Layer 1 for F (neighbors E, C, G):
    - $m_F^{(1)} = \frac{h_E^{(0)} + h_C^{(0)} + h_G^{(0)}}{3}$
    - $h_F^{(1)} = \sigma\!\left( W_1 \frac{h_E^{(0)} + h_C^{(0)} + h_G^{(0)}}{3} + U_1 h_F^{(0)} + b_1 \right)$
- Layer 2 for C (neighbors still A, F):
    - $m_C^{(2)} = \frac{h_A^{(1)} + h_F^{(1)}}{2}$
    - $h_C^{(2)} = \sigma\!\left( W_2 \frac{h_A^{(1)} + h_F^{(1)}}{2} + U_2 h_C^{(1)} + b_2 \right)$
        - Utilizing $h_A^{(1)}$ and $h_F^{(1)}$ from the previous layer allows us to "message pass" information from their neighbors through to this layer
        - Utilizing $h_C^{(1)}$ allows us to incorporate the node's own previous embedding, preserving self-information, and also allowing it's neighbors to contribute and update it's embedding
- Fully expanded $h_C^{(2)}$ in terms of layer-0 embeddings - it's illustrative only, full expansion can't be done because of parameter sharing so things must be done in steps:
$$
h_C^{(2)} =
\sigma\!\Bigg(
\frac{W_2}{2} \Big[
\sigma\!\left( W_1 \frac{h_B^{(0)} + h_C^{(0)} + h_G^{(0)}}{3} + U_1 h_A^{(0)} + b_1 \right)
+
\sigma\!\left( W_1 \frac{h_E^{(0)} + h_C^{(0)} + h_G^{(0)}}{3} + U_1 h_F^{(0)} + b_1 \right)
\Big]
+ U_2 \sigma\!\left( W_1 \frac{h_A^{(0)} + h_F^{(0)}}{2} + U_1 h_C^{(0)} + b_1 \right)
+ b_2
\Bigg)
$$

## Graph Convolutional Networks
Graph Convolutional Networks (GCN's) were first introduced as a method for applying NN's to graph structured data

The simplest GCN's had three operators:
- Graph convolution
- Linear layer
- Nonlinear activation

The operations were also typically done in that order, and the Node Embedding example above showcases a similar ordering
- Aggregate local neighbors (convolution)
- Apply linear transformation (linear layer)
- Use a nonlinear $\sigma$ activation for more robust relationships

The initial workflow above inspired GraphSAGE

### GraphSAGE Idea
GraphSAGE is a representation learning technique for dynamic graphs - this, in english, means that it can create node embeddings on new (previously unseen) nodes, which makes it inductive and useful for dynamic or growing graphs

The intuition is that GraphSAGE learns vector representations (embeddings) for nodes by repeatedly sampling a node's neighbors, aggregating their features (permutation invariant function), combining that with it's own features, and passing through neural layers - this is exactly what we saw above in the Node Embedding portion, and it allows generalization to new (previously unseen) nodes in the graph because it utilizes sampling and doesn't require the full adjacency matrix to compute a node's embedding. This means it doesn't require *all* of a node's neighbors (full adjacency matrix), and can create embeddings based on local samples

Simple Neighborhood Aggregation:
$$
h_k^{(v)} = \sigma(W_k \sum_{u \in N(v)} {h_u^{(k-1)} \over {|N(v)|}} + B_k h_k^{(k-1)}) 
$$

GraphSAGE:
$$
h_k^{(v)} = \sigma([W_k \cdot \text{Agg}(\{h_u^{(k-1)} : u \in N(v)\}), B_k h_k^{(k-1)}])
$$
- Generalized aggregation method: $ \text{Agg}(\{h_u^{(k-1)} : u \in N(v)\})$
    - Literally just mentions any aggregation on layers before it, in it's neighborhood
    - Other options outside of typical weighted average include
        - **Pooling**: Transform each neighbor embedding with a NN, then apply element-wise max-pooling
            - $\text{Agg}(\{h_u^{(k-1)} \space \forall u \in N(v)\}) = \max_{u \in N(v)} \sigma(W_{\text{pool}} h_u^{(k-1)} + b_{\text{pool}})$
        - **LSTM**: Use a unidirectional LSTM to aggregate neighbor embeddings (requires imposing an order on neighbors, which is not inherently defined in graphs)
            - $\text{Agg}(\{h_u^{(k-1)} \space \forall u \in N(v)\}) = \text{LSTM}(\{h_u^{(k-1)} \space \forall u \in N(v)\})$
- Concatenate neighbor embedding and self embedding via the $+$ in the simple neighborhood aggregation, but you can do any other combination operation (specified as "," in the GraphSAGE equation)