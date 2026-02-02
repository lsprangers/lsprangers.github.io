---
layout: technical
title: 8. Trees & Graphs
category: Data Structures & Algorithms
difficulty: Advanced
description: Examples, definitions, and general knowledge around Trees & Graphs
show_back_link: true
---

## Trees

### Binary Tree
A binary tree is simply a hierarchical tree that has at most 2 children for any node

A Graph would mean any number of connections for a node, and there are similarities there, but binary (2) means at most 2 children and 1 parent

```python
class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right
```

Binary Tree's are both specific types of Graphs, and so are Linked Lists actually

### Binary Search Tree
Binary Search Tree's are tree's who, for any node, have:
- All left children $\lt$ node value
- All right children $\gt$ node value

The reason these are different from regular Binary Tree's are this specific relationship - at each step you can reduce the total search space by half, resulting in $O(\log n)$ search time

You can reduce it because there's a specific relationship $gt$, $lt$

### Self-Balancing Binary Search Tree
- Self Balancing BST's have the same property as Binary Search Tree's, except they will balance themselves out via different methods
- The reason for this balancing is that Binary Search Tree's worst case lookup time degrades to $O(n)$ if the tree represents a Linked List
  - This usually happens when you insert nodes in order and it becomes all right or left sides
#### AVL Tree
#### Red Black Tree

### Segment Tree
[Article used](https://leetcode.com/articles/a-recursive-approach-to-segment-trees-range-sum-queries-lazy-propagation/)

A segment tree is a Binary Tree where each node represents an interval, and each node would store one or more properties of an interval that'd be queried later on

Most of the time it's segements / indexes of an array, and the total sum, count, or some aggregation over them, which allows us to find a certain aggregation over a range of data in potentially $O(\log n)$ time

![LeetCode Segment Tree](/img/lc_segment_tree.png)

- Typically the root holds the entire interval of data we're interested in traversing
- Each leaf of the tree represents a range of just one single element
- The internal nodes would represent the merged or unioned result of their children nodes
- Ideally, each child node would represent about 1/2 of it's parent
- Implementation:
  - Single callable function
  - Recurses down until at leaf node, and stores singular value in leaf node
  - After exiting later on in recursive call merge the child values via $O(1)$ array lookup

```
void buildSegTree(vector<int>& arr, int treeIndex, int lo, int hi)
{
    if (lo == hi) {                 // leaf node. store value in node.
        tree[treeIndex] = arr[lo];
        return;
    }

    int mid = lo + (hi - lo) / 2;   // recurse deeper for children.
    buildSegTree(arr, 2 * treeIndex + 1, lo, mid);
    buildSegTree(arr, 2 * treeIndex + 2, mid + 1, hi);

    // merge build results
    tree[treeIndex] = merge(tree[2 * treeIndex + 1], tree[2 * treeIndex + 2]);
}

// call this method as buildSegTree(arr, 0, 0, n-1);
// Here arr[] is input array and n is its size.
```

- The more important part is querying
  - you can't read partial overlaps, it would be too confusing
  - Need to traverse down until you get to a section that's smaller than your desired interval, and worst case add in from other sections as well
    - Can hopefully use some internal / middle nodes, and complete the aggregation using other leaf nodes
- Updating values means finding the leaf node of the actual index, and traversing back up and out to update that leaves parents

### Prefix Sum
- The Prefix Sum is defined, for 1-D arrays, in [Arrays and Strings](/docs/dsa/1.%20arrays%20&%20strings/index.md#prefix-sum)
- The Prefix Sum also comes up in Tree Traversal because you can use it during a tree traversal technique to find things like 
    - *Total number of paths that sum to X*
    - *Total number of paths less than or equal to X*
    - etc
    - The same "problems" that Prefix Sum solves for Arrays it can solve for in Trees as well
  
There is just one thing that is particular for the binary tree...there are two ways to go forward - to the left and to the right

To keep parent->child direction, you shouldn't blend prefix sums from the left and right subtrees in one hashmap
![Tree Path Prefix Sum](/img/tree_pfxsum.png)

So to do this for Binary Tree you start off by defining some global variables
```
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:

    resp = 0
    target = targetSum
    freq = defaultdict(int)
    preorder(root, 0)
    return(resp)
```
And then you need to create the traversal code

Weird part is removing it from `freq` after passing, but just means you take it out so other traversals aren't affected by it, and is from [Backtracking](/docs/dsa/9.%20backtracking/index.md) - it ensures that when you return from a recursive call (i.e., move back up the tree), the prefix sum count for the current path is removed from the frequency map

```
target = 3
  1
 / \
2   3

root(1) - currSum = 1, freq = {0:1, 1:1}
left to 2 - currSum = 1 + 2 = 3, freq = {0:1, 1:1, 3:1}
Done
Move back up
freq[3] -= 1 --> freq = {0:1, 1:1, 3:0}
Right to 3 - currSum = 1 + 3 = 4, freq = {0:1, 1:1, 3:0, 4:1}
```
Although this wouldn't affect this specific problem, with a large enough tree there'd be sums thrown all throughout here that would most likely affect the outcome

```
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        def preorder(curr: Optional[TreeNode], currSum: int) -> None:
            nonlocal resp # use the global variable

            # check existence here, not if left then left, if right then right
            if not curr:
                return
            
            currSum += curr.val
            if currSum == target:
                resp += 1

            resp += freq[currSum - target]
            freq[currSum] += 1
            preorder(curr.left, currSum)
            preorder(curr.right, currSum)

            # Remove this from map so you don't use it in other parts of tree
            freq[currSum] -= 1

        resp = 0
        target = targetSum
        freq = defaultdict(int)
        preorder(root, 0)
        return(resp)

```

## Traversal Types

### Depth First Search
Depth first search (DFS) prioritizes searching as far as possible along a single route in one direction until reaching a leaf node before considering another direction

DFS is typically only used in tree traversals, as graphs have circles and odd structures - tree's you can "go to the end" meaning a leaf node in a reasonable fashion

DFS utilizes a similar template structure to binary tree's above, but in DFS you choose what operations you do with the nodes themselves
```python
def dfs(node):
    if node == None:
        return

    dfs(node.left)
    dfs(node.right)
    return
```

There are 3 main types of DFS, and all of them relate to where you engage with the root node:
- **Inorder** traversal is left, root, right
- **Preorder** traversal is root, left, right
- **Postorder** traversal is left, right, root

```python
def dfs(node):
    if node == None:
        return

    # operation(root) - preorder
    dfs(node.left)
    # opertaion(root) - inorder
    dfs(node.right)
    # operation(root) - postorder
    return
```

![DFS Traversal Types](/img/dfs_traversal_types.png)

#### Recursion Stack
Each function call to `dfs()` solves and returns the answer ot the original problem (in the call stack) as if the subtree rooted at the current node was the input

Most use cases of DFS utilize recursion, and underneath the hood recursion is simply a [stack](/docs/dsa/3.%20stacks%20&%20queues/index.md#stacks)

In the below tree, if we ran an inorder traversal the output would be `3, 1, 0, 4, 2, 5`
```python
    0
   / \
  1   2
 /   / \
3   4   5

def dfs(node):
    if node == None:
        return

    dfs(node.left)
    print(root) - inorder
    dfs(node.right)
    return
```

Looking at the call stack we would see:
- `call_stack = []`
- `dfs(root) --> call_stack = [dfs(0)]`
  - Inside of `dfs(0)`
    - Call `dfs(0.left) --> call_stack = [dfs(0), dfs(1)]`
      - Inside of `dfs(1)`
        - Call `dfs(1.left) --> call_stack = [dfs(0), dfs(1), dfs(3)]`
          - Inside of `dfs(3)`
            - Call `dfs(3.left) --> call_stack = [dfs(0), dfs(1), dfs(3), dfs(None)]`
              - Inside of `dfs(None) --> return None`
              - `call_stack = [dfs(0), dfs(1), dfs(3)]`
            - Call `print(root) --> 3`
            - Call `dfs(3.right) --> call_stack = [dfs(0), dfs(1), dfs(3), dfs(None)]`
              - Inside of `dfs(None) --> return None`
              - `call_stack = [dfs(0), dfs(1), dfs(3)]`
            - Exit `dfs(3)`
        - Call `print(root) --> 1` (at this point output is 3, 1)
        - Call `dfs(1.right) --> call_stack = [dfs(0), dfs(1), dfs(None)]`
            - Inside of `dfs(None) --> return None`
            - `call_stack = [dfs(0), dfs(1)]`    
- And so on, and so forth!

The `call_stack` is just a stack that's pushe and popped to by the actual underlying python recursion, and this feature is available in basically every language. For DFS you can also implement this yourself, and it becomes an ***Iterable DFS*** solution where no recursion is involved - you simply do all of the stack calls yourself

Preorder is the cleanest implementation of this, and inorder and postorder are a bit tricky

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
  def maxDepth(self, root: Optional[TreeNode]) -> int:
    if not root:
      return 0

    stack = [(root, 1)]
    ans = 1

    while stack:
      curr_node, curr_depth = stack.pop()

      # preorder operation(root)
      ans = max(ans, curr_depth)

      # dfs(left)
      if curr_node.left:
        stack.append((curr_node.left, curr_depth + 1))
      # dfs(right)
      if curr_node.right:
        stack.append((curr_node.right, curr_depth + 1))      
```

In this way, you never leave the initial `maxDepth` call, and you just implement everything on a stack yourself

Time complexity - there are $n$ nodes, so we are guaranteed to do $O(n)$ work 
  - Typically `operation(root)` is an $O(1)$ operation, but it may also be some other $O(k)$
  - If it's $O(1)$ then the entire thing is $O(n)$, if it's $O(k)$ then $O(n \times k)$
  - Altogether, the time complexity is $O(n \times k)$, where $k = 1$ is typical

Space complexity is 
  - Usually $O(n)$ in the worst case, as you're placing all of these calls onto a stack and if the tree is straight up and down (linked list) you can reach $O(n)$
  - If the tree is perfectly balanced, space complexity becomes $O(\log n)$

### Breadth First Search
Breadth First Search (BFS) is another way to traverse tree's and graphs, but is different from DFS in that it checks row by row instead of traversing down left, right, etc depth wise

The real difference between the 2 lies in their efficiencies on problems:
- BFS is better if the node is higher up, or if the logic requires level based logic
- DFS is better if the node is easily found traversing depth wise, or if the logic requires it!
- DFS space complexity, in typical cases, revolves around height of the tree and ends up being $O(\log n)$, but BFS is based on the largest span of the tree, and in a perfectly balanced tree would result in $O(n)$ as the bottom row would have $n \over 2$ nodes in it
- Time complexity they're usually equivalent, unless the tree structure and problem statement are weird enough to cause them to deviate
  - Using underlying deque data structure is required, as using a list wil cause time complexity to explode with inserts

```python
from collections import deque

def print_all_nodes(root):
    queue = deque([root])
    while queue:
        nodes_in_current_level = len(queue)
        # do some logic here for the current level

        for _ in range(nodes_in_current_level):
            node = queue.popleft()
            
            # do some logic here on the current node
            print(node.val)

            # put the next level onto the queue
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
```

## Binary Search Tree
In a binary search tree, there's some special properties where, for any Vertex V, it's right child is greater than it's value, and its left child is less than it's value

Ultimately it's just a way to restructure a Linked List so that search is in $O(\log n)$ time - this entire concept is the idea of [Self-Balancing Binary Search Trees](/docs/dsa/6.%20binary%20search/SELF_BALANCING.md) such as [B-Tree's](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE.md). Self balancing tree's have less efficient writes (since they need to find where to place nodes and do some restructuring), but the idea is that reads are much more efficient

A Binary Search Tree has similar code structure to Lists

```python
def search_bst(root, target):
    while root is not None:
        if root.val == target:
            return True
        elif target < root.val:
            root = root.left
        else:
            root = root.right
    return False
```

BST's follow similar time and space complexity to [Binary Search](/docs/dsa/6.%20binary%20search/index.md), but when you traverse a BST itself you use recursion / DFS for the actual recursion, and you'd simply choose `left` or `right` instead of going down both paths

## Graphs
At it's core a Graph is a data structure consisting of two components - vertices (or nodes) $V$ and edges (connections between nodes) $E$

Then a Graph $G = (V, E)$ is defined by these sets of vertices and edges, both $V$ and $E$ are sets of objects

Let's say there are $n$ vertices, with $m$ edges overall, where each node can have up to $f$ features

In most scenario's the set $E$ will consist of ***triplets***, which are objects of $(V_i, V_j, w)$ where $w$ represents the weight of the edge between vertices $V_i$ and $V_j$. Other times it will include other information, so $(V_i, V_j, [R])$ that $R$ represents a set of relationships, but ultimately the relationships are defined by concepts such as "friends with", or "employs" or some other relationship that may or may not have weight. These features can be represented in a node feature matrix $R \in \mathbb{R}^{n \times f}$

A Graph $G$ is often stored and represented digitally using an adjacency list or adjacency matrix $A$ - then $A \in \mathbb{R}^{n \times n}$ where each node is both a row and a column, and $A[i, j]$ represents the edge between vertices $V_i$ and $V_j$

Most data structures can actually be considered specific dimensional graphs, lists are 1-dimensional graphs, trees are hierarchical graphs, images are consistently dimensioned graphs (pixel sizes), etc

![Everything Is Graph](/img/everything_is_graph.png)

### Structuring
There are 2 main ways to structure a graph in memory, either via an Adjacency List or an Adjacency Matrix
- An Adjacency List is simply a list of lists, where each index represents a vertex, and the list at that index represents all of the connected vertices
  - This is typically more space efficient for sparse graphs, where not every vertex is connected to every other vertex
- An Adjacency Matrix is a 2-D matrix where each row and column represents a vertex, and the value at that index represents the weight of the edge between those vertices (or 1 if unweighted, or 0 if no edge)
  - This is typically more space efficient for dense graphs, where many vertices are connected to many other vertices

In most real world scenarios graphs are sparse, and so Adjacency Lists are more commonly used, and even those structures are further optimized and compressed to ensure space efficiency

Representing a graph digitally is a large topic, and there are many more advanced structures like Compressed Sparse Row (CSR) or Compressed Sparse Column (CSC) formats that are used in large scale graph processing systems

For common API's on graphs we usually store 2 data structures:
- Node list / set
- Edge list / set

These 2 data structures allow us to traverse and manipulate the graph effectively, and are the basis for most graph algorithms - they also allow us to have ***heterogeneous*** graphs where different nodes and edges can have different types and properties. At the end of the day each of these properties typically extend an `Object`, so you can store any kind of data you want in them - the traversal algorithm is then expected to handle the different data types accordingly

### Graph Types
Graphs can have a few different topological setups as well - including:
- **Multi-Relational**: A graph that has more than one type of relationship between vertices
  - In a social network we can have friend, family, coworker, etc..
    - Formally, a multi-relational graph is defined as $G = (V, T, E)$ where $T$ is a set of edge-types
  - The adjacency matrix in this scenario would be a $3-D$ matrix (a ***Tensor***), where $A[n1, n2, type] = 1$ if there's an edge of type `type` between `n1` and `n2`
    - The tensor dimension here would be $V \times V \times T$
- **Multiplex**: A graph where there are multiple types of edges between the same pair of vertices, and furthermore each edge has it's own weight
  - It introduces intra-layer (within) and inter-layer (between)
    - Intra layer edges are edges that connect nodes for that layer type
    - Inter layer edges are routes that connect nodes across different layer types
  - Using transportation network as an example, where nodes are cities and the types are transportation types (flight, rail, train, car, walk, etc...)
    - Intra layer edges represent getting between 2 citites using a single transportation type
    - Inter layer routes represent getting between 2 cities utilizing more than 1 transportation type

### Sub Graph and Node Statistics
Graph statistics revolve around profiling graphs, sub-graphs, and other components by using various metrics and algorithms to understand their structure and properties - some are basic counting, some are combinatorics, and some are more advanced distributions. They answer questions about centrality, sparsity, density, connectivity, and other metrics

A common one to start off is cluster (sub-graph) density, and the intuition is finding the ratio of observed edges to possible edges within a cluster or sub-graph

- $\text{possible connections} = \frac{n \cdot (n-1)}{2}$
- $\text{observed connections} = e$
- $\text{cluster density} = \frac{\text{observed connections}}{\text{possible connections}}$

The "hello world" of graph statistics is centrality utilizing the [Florentine Families Dataset](https://networks.skewed.de/net/florentine_families), which showcases relationships between families in Renaissance Florence, and typically should always have the Medici family as the most central node

To get to centrality and other metrics, there are some common statistics we'll define below:
- **Degree**: The number of edges connected to a vertex
  - In-Degree: Number of incoming edges to a vertex (for directed graphs)
  - Out-Degree: Number of outgoing edges from a vertex (for directed graphs)
- **Degree Centrality**: The number of edges connected to a vertex, normalized by the maximum possible degree
  - If there are 8 nodes in a graph, and a specific node has 2 edges to 2 other nodes, it's degree centrality would be \(\frac{2}{7}\)
- **Path Length**: The number of edges in the shortest path between two vertices
- **Clustering Coefficient**: A measure of the degree to which nodes in a graph tend to cluster together
  - For a vertex, it's the ratio of the number of edges between its neighbors to the number of possible edges between those neighbors
  - For the whole graph, it's the average clustering coefficient of all vertices
- **Betweenness Centrality**: A measure of how often a node appears on the shortest paths between other nodes
  - Betweenness shows how often a node lies on the shortest path between two other nodes, and these nodes can be considered "route hubs" of sorts
  - Cincinnati is a good example used to illustrate betweenness centrality in transportation networks, no one ever stops there, everyone just drives through it
- **Eigenvector Centrality**: A measure of a node's influence based on the influence of its neighbors
  - Sum of centrality scores of neighbors
- **Closeness Centrality**: A measure of how close a node is to all other nodes in the graph, based on the average shortest path length from the node to all other nodes
  - Inverse of average shortest path length to all other nodes
  - Gives information on how close a node is to all other nodes, and simply showcases what node, even if it's not as important, is closest to everything
- Subgraph classifications and definitions:
  - **Closed Triangles**: Sets of three nodes where each node is connected to the other two nodes
  - **Ego Graphs***: Subgraphs consisting of a focal node, and all the nodes that are connected to that focal node
    - Most likely is star shaped
  - **Motifs**: Patterns of node connectivity that occur more than would be expected by chance
    - Basically a catch all for sub-graph patterns - closed triangles and ego graphs are specific motifs
- **Clustering Coefficient**: Measures the proportion of closed triangles in a node's local neighborhood
  - Can be used to find communities in a network, which help to show how clustered a node is
  - $\frac{\text{# of triangles in a node's local neighborhood}}{\text{# of possible triangles in a node's local neighborhood}}$
#### Eigenvectors in Graphs
Seeing an [Eigenvector](/docs/old_math_notes/linear_algebra/index.md#eigenvalues-eigenvectors-and-eigendecomposition) scared me - they're actually utilized in Graph Theory to understand how certain graphs change as operations are performed on them 

Eigenvectors can be used to find equilibrium points of graphs, which ultimately are points that aren't affected by any changes that are made to it

Graphs are just matrices, so eigenvectors help us understand their properties and behaviors - an adjacency matrix represents the connections between nodes, and therefore eigenvectors represent directions in which the graph can be transformed without changing its structure

An adjacency matrix can be seen as a transformation that acts on "node vectors", or functions defined on the graphs nodes

The intuition of an eigenvector on an adjacency matrix is that it allows us to find important nodes in a graph, where the eigenvector centrality of a node is proportional to the sum of the centralities of its neighbors

[Some intuition from Reddit](https://www.reddit.com/r/3Blue1Brown/comments/18kieax/intuition_behind_eigenvector_centrality_in_graph/)

[Some definitions on GeeksForGeeks](https://www.geeksforgeeks.org/data-science/eigenvector-centrality-centrality-measure/)

[Some Medium Articles](https://medium.com/the-modern-scientist/graph-neural-networks-series-part-2-graph-statistics-4f271857ec70)

If we wanted to find a function below that essentially brings a node to the real numbers, we can use a vector with one entry for any node - i.e. a **node vector**
$$f(\text{node}) \rarr \mathbb{R}$$

Backtracking a bit, this ends up relating to *harmonic functions*, which are function $f: \mathbb{R} \rarr \mathbb{R^2}$ that is always equal to it's average on circles - this means the function is always reverting towards it's average within some bounding box

The analogy of eigenvectors on graphs is a node vector so that each entry is always equal to the average of the entries of it's neighbors - i.e. within a small bounding box (neighbors), we want the eigenvector entries to always be equal to the average of it's neigbors. Therefore, if an eigenvector's value is large, we can see that it's node (the average of it's neighbors) means that node and it's neighbors must be a sort of critical central component

This node vector intuitively encodes some information about adjacency between nodes, and ultimately this encoded vector would have to be constant over each connected component of a graph (they're all neighbors)

Therefore, at the end, ***eigenvector centrality (eigencentrality) is a measure of the influence of a node in a network!***

PageRank and Katz centrality are related concepts that build upon eigenvector centrality to rank nodes in a network, and they are natural variants of this eigencentrality

***The $v^{\text{th}}$ component of the related eigenvector gives the relative centrality score of the vertex $v$!***

What can this help us with graph profiling:
- Graph structure: Eigenvectors can reveal overall "sub-clusters" within a graph, and reveal if the entire graph is highly connected
- Centrality measures: The eigenvector values are measure's of node importance that consider both the node's direct connections, and their neighboring node's
  - Assigning higher scores to nodes that are connected to other highly connected central nodes
- Network dynamics: Eigenvectors can be used to understand the stability or equilibrium of processes on the network, and can even help us find steady state distributions and feeback loops (similar to markov chains)
- Community detection: Eigenvectors can be used in community detection algorithms to identify groups of nodes that have similar connectivity patternss

##### Proof / Math
- For a given graph $G := (V, E)$ with $|V|$ vertices
- $A = (a_v, t)$ is the adjacency matrix such that 
  - $a_{v, t} = 1$ if vertex $v$ is linked to vertex $t$
  - 0 otherwise
- $M(v)$ is a set of neighbors of vertex $v$

Then, the relative centrality score of a vertex $v$ can be defined as:
$$x_{v} = {\frac{1}{\lambda}} \sum_{t \in M(v)} x_t = {\frac{1}{\lambda}} \sum_{t \in G} a_{v,t} \cdot x_t$$

Rearranging the above equation (somehow) you can get to vector notation where:
$$\bold{A}\bold{x} = \lambda \bold{x}$$

There'll be many eigenvalues $\lambda$ for which a non-zero eigenvector solution exists, but extra conditions such as all entries in the eigenvector be non-negative (Perron-Frobenius) implies that only the greatest eigenvalue is considered for eigenvector centrality

***The $v^{\text{th}}$ component of the related eigenvector gives the relative centrality score of the vertex $v$!***

### Graph Statistics
Now they Sub-Graph and Node Statistics are covered above, there's a natural way to extend those to entire graphs

The typical proposal is to extract these metrics utilizing [Graph Kernel Methods](https://ethz.ch/content/dam/ethz/special-interest/bsse/borgwardt-lab/documents/slides/CA10_GraphKernels_intro.pdf) which are classes of ML algorithms that can be used to learn from data that's represented as a graph

Most graph kernel methods are proper ML algorithms, and so we'll define them further in [Graph Neural Networks](/docs/other_concepts/graph_processing/GRAPH_NN.md#graph-kernel-methods)

## Graph Traversal
- Traversing a graph has generally 2 strategies, either Depth first or Breadth first
- Depth first means exactly as it says, from any single node you traverse as far down / as far away as you can possibly go
- Breadth first on the other hand means from any node you explore each degree, or "level away", equally
  - BFS is typically used in ***shortest path problems*** because as you go out a degree each level, you're guaranteed to hit the shortest path first, wheras DFS would need to search every path and then take `min()`
    - Although for BFS to find the optimal solution, each edge has to have ***equal and positve weights***, and so it wouldn't work for weighted edges - that's typiaclly when you would use [Djikstra's](#djikstra) algorithm

$V$ is the number of Vertices, and $E$ is the number of edges

| Operation        | Time Complexity    | Space Complexity   |
|------------------|--------------------|--------------------|
| Traverse         | $O(V + E)$         | $O(V)$             |


This theoretical discussion is useful, but in large scale processing graph traversal is typically done via message passing over super-steps in a breadth first search format

### Maze
Maze's are a special kind of graph where you essentially have a connected 2-D diagram

Most common examples are [Finding The Nearest Exit](/docs/leetcode_coderpad/leetcode/python/nearestExitFromEntranceInMaze.md) or something similar, where you will use Breadth First Search to traverse outwards checking over the course of a structure

### UnionFind / Disjoint Set union
- Union Find is a data structure that allows us to find a representation of clusters in a disconnected graph
  - It allows us to find connectivity of 2 nodes, i.e. if they're in the same component, in $O(1)$ time
  - Optimizations:
    - ***Path Compression:*** So that root / parent identification will be updated as you traverse down a graph
    - ***Union by Rank:*** So that our tree's don't become unbalanced over time
- For the time complexities below, $\alpha(n)$ is the *Inverse Achermann Function*, which "grows slowly and is effectively constant for all practical inputs"
- An [Implementation](/docs/dsa/implementations/optimized_unionfind.md) in C++ can be reviewed for actual runtime info

| Operation        | Average Complexity |
|------------------|--------------------|
| Union (Put)      | $O(\alpha(V))$     |
| Find (Get)       | $O(\alpha(V))$     |
| Delete           | Not Applicable     |
| Traverse / Search| $O(n)$             |

### Connected Components
- Connected Components is a way for us to find all of the clusters in a graph, where connectivity can be *weak*, *strong*, or a few other types like *unilaterally*
  - *Weak* connected components can be thought of as *undirected* connected components, so that edges are just generic edges
  - *Strongly* connected components would require *directed* edges between all ***pairs of vertices*** meaning there has to be a way to get to any node, NodeA, from any other node in the component NodeB
- Algorithms:
  - ***Breadth First Search***:
    - Start a BFS traversal from every unvisited node $node_i$
    - Traverse all neighbors $node_{j's}$ of $node_i$, marking them as visited
    - Continue the traversal until all nodes in the connected component of $node_i$ are visited
    - Repeat for all unvisited nodes to find all connected components.
  - ***UnionFind*** above will have the `root` vector at the end corresponding to all of the unique connected component ID's

#### *Map Reduce Connected Componenets
Pregel is a way to do generic BFS and Graph Traversals in the MapReduce world, and there are ways to implement Connected Components via BFS using Pregel framework

you discuss Pregel in other areas, but it's useful to note here as some popular large scale data processing engines use this

### Minimum Spanning Tree
A ***Spanning Tree (ST)*** is a connected subgraph where all vertices are connected by the minimum number of edges

In my opinion it seems similar to a Span in a Vector Space which describes all of the orthonormal basis vectors that can be combined to create any vector in that space, but it's really not

The pink edges below show the ST
![ST](/img/st.png)

A ***Minimum Spanning Tree (MST)*** is when there are weights in a graph, you ideally can find the ST with the smallest total weight

An undirected graph can have multiple ST's and MST's

A ***cut*** in Graph Theory is a way to split up the Vertices and Edges in a Graph into 2 distinct sets, essentially cutting it to create 2 disjoint subsets

![Cut](/img/cut.png)

So the ***cut property***, which will help us run different algorithms, says for any Cut $C$ of the Graph $G$, if the weight of an Edge $E$ in a Cut-Set $C_s$ is strictly less than all other Edges in $C_s$, then $E$ belongs to all MST's of $G$

The [proof above would rely on contradiction](https://stackoverflow.com/questions/3327708/minimum-spanning-tree-what-exactly-is-the-cut-property) and goes something along the lines of "well if you didn't have that edge, $E$ in the MST, then you could add it and create a cycle that crosses the cut at least twice (first and newly added edge), and then if you removed the other Edge $E^`$ greater than it, it would result in a MST less than the original one"

MST algorithms are useful to find solutions to things like "min number of vertices to connect all points" similar to traveling salesman

#### Kruskal
Kruskal's Algorithm is for creating a [Minimum Spanning Tree](#minimum-spanning-tree) from a Weighted Undirected Graph. It uses sorting and [UnionFind](#unionfind--disjoint-set-union) to solve for MST 

- Kruskal's Algorithm will:
  - Sort all edges, taking $O(E \times log(E))$ time using a typical sorting algorithm
  - Starting smallest, for each edge:
    - Check if the vertices of the edge are in the same connected component - which can be done via [UnionFind](#unionfind--disjoint-set-union) and takes $O(\alpha(V))$ lookup and add time
      - This essentially shows us if it would create a cycle / unnecessary edge
    - Once you reach $V - 1$ edges we've constructed our MST

| Time Complexity    | Space Complexity   |
|--------------------|--------------------|
| $O(E \times log(E) + \alpha(V)) = O(E \times log(E))$         | $O(V)$             |

#### Prim
Prim's Algorithm is another algorithm for creating a [Minimum Spanning Tree](#minimum-spanning-tree) from a Weighted Undirected Graph. It uses 2 sets to solve for MST

- Start with `MST = set()` empty set, and `NVisited = set(all_V)` full of every vertex
- Start with an arbitrary vertex
  - For each step find all edges that connect `MST <--> NVisited` and take the minimum edge, and add that Vertex into MST
    - *Remember - The edge that connects two disjoint sub-graphs is a ***cut***
      - Time complexity is all around building min-heap, and then after that you are simply traversing unvisited nodes which is at most $O(V)$ so the min-heap building will dominate time complexity
      - Inserting into min-heap is $O(log V)$, and you do that for all edges $E$
  - So at each step find the minimum edge crossing the cut, add the Vertexes to MST, and remove them from NVisited

Finding all the edges that connect the 2 sets is the majority of complexity here, and typically is solved using

| Time Complexity    | Space Complexity   |
|--------------------|--------------------|
| $O(E \times log(V))$ | $O(V)$             |

Python Code

Pseudocode:
$U$ is the set of visited Vertices, $V - U$ is the set of unvisited Vertices
```
T = ∅;
U = { 1 };
while (U ≠ V)
    let (u, v) be the lowest cost edge such that u ∈ U and v ∈ V - U;
    T = T ∪ {(u, v)}
    U = U ∪ {v}
return(T)
```

### Shortest Path
[Breadth First Search](#graph-traversal) can help us find the shortest path between 2 nodes ***in an unweighted graph***, but it can't help when the graph is weighted because there are so many more options!

#### Edge Relaxation
The ***Edge Relaxation Property*** is the general property describing that although a path might take more hops, the weights on it might be smaller. In the below example `A -> C -> D` has a total weight of 2, while `A -> D` has a weight of 3
![Edge Relaxation Example](/img/relaxation.png)

#### Djikstra
Djikstra's Algorithm can help solve the shortest path problem for graphs with ***non-negative weights***

It solves the shortest path problem for a single Vertex, to all other Vertices

you also showcase this problem in [Pregel Graph Processing Docs](/docs/other_concepts/graph_processing/PREGEL.md#single-source-shortest-path-djikstra) - in most cases you can't hold an entire graph in memory, and we'll have it written to disk somewhere, and Pregel is a Graph Traversal SDK for distributed datasets using [Spark](/docs/other_concepts/SPARK.md)

Djikstra's algorithm is greedy, and essentially starts from a central point `u` and expands outwards, continually getting the min from the seen vertices to find shortest path to other vertices, it uses a min-heap to continuously select the vertex with the smallest known distance

you hold the state of our source vertex to each other vertex in the graph, and you hold "previous vertex" and length information in this table which will help us traverse recursively if you needed to rebuild the path. you can lookup distance from source to any other vertex in $O(1)$ once it's complete, and then rebuilding path is at worst $O(E)$ because it might be a linked list, and building this data structure and traversing the graph resutls in us visiting each vertex and each node so it would be around $O(V + E)$ time complexity, but for each edge in a vertex you need to find the min vertex which is $O(log V)$, therefore total time complexity is $O(V + E \times log(V))$ and $O(V)$ space (since you need to store visited node info)

| Time Complexity    | Space Complexity   |
|--------------------|--------------------|
| $O((V + E) \times log(V))$ | $O(V + E)$ |

- Use cases:
  - Network delay times from source to all sinks
  - Traveling salesman that needs to cover all houses
  - ...

#### Bellman-Ford
Bellman-Ford can help solve shortest path for all graph types ***including negative weights***

### Topological Sorting / Kahns Algorithm
Topological Sorting can help us traversing graphs when there are dependencies in directed acyclic graph's (DAGs), which is different from the above undirected weighted graphs

A key property is ***acyclic*** meaning there are no cycles in the graph! It wouldn't make sense if our prerequisites were required for our prerequisites!

- Use cases:
  - Course scheduling with pre-requisites
  - Workflow DAGs
  - ...

The main algorithm for this is ***Kahn's Algorithm*** where you will basically iterate over all vertexes that have `indegree = 0`, and do something with them, and then decrement their downstream vertexes. This ultimately creates "levels" where multiple classes or jobs could be ran at the same time, and once they're all done you should be ready for our downstream vertexes (decrement indegree)

Since you are only iterating over edges and vertexes and doing increment / decrement, our space and time complexities are $O(V + E)$

| Time Complexity    | Space Complexity   |
|--------------------|--------------------|
| $O(V + E)$         | $O(V + E)$         |


You can also utilize straight up [DFS for topological sort](/docs/leetcode_coderpad/coderpad_implementations/python_files/dependencyGraph.py) in some dependency graph problems by utilizing the 3-color masking method. Ultimately this relates to tracking state along the call stack, and if something is currently in the stack (lookup in `state = defaultdict(int)` dict) with `state = 1`, then it's a loop as you'll eventually form a cycle

[Leaves Of A Binary Tree](/docs/leetcode_coderpad/leetcode/python/findLeavesOfBinaryTree.md) also has implementations for DFS, better DFS, and topological sort (BFS)

```python
state[u] = 1
for v in deps[u]:
    dfs(v)
state[u] = 2
order.append(u)
```

You need to do postorder traversal for this to work, as for any node you need to go completely explore all of the nodes it depends on - so you'll need some sort of dictionary like `services_depends_on` where each key is a specific node, and each item in the value list is another node that it will depend on. Once you go through all of those, and eventually add them to your `order` response, it'll be a topologically sorted array


## Graphs In the Wild

### Storage 

### Traversal / Compute