----
Title: How We Implemented Graph Traversal via MapReduce
Date: 2025-01-30
----

# Why does this even matter
A lot of ML and analytics is done on Spark nowadays, and most of the goodness from Spark goes away when people abstract things out like graph traversals, which undermine most analytics use cases around graphs. 
We've had a lot of difficulty getting GraphX to scale, and so instead of that we implemented our own way of doing graph traversal via MapReduce. 

## Takeaways
You absolutely use an enormous amount of space and offset this by having many things ran in parallel while ultimately getting the desired result faster. The same thing could be achieved in a regular Scala file using some thread safety and actors across a Queue, but when you scale up to millions of nodes and billions of edges that dream goes away. 
