---
layout: technical
title: Distributed Training
category: Training and Learning (ML)
difficulty: Advanced
description: Discussions around Evaluation Frameworks
show_back_link: true
---

## Distributed Training
Distributed training can be done on a single machine, utilizing multiple CPU or GPU, or across machines utilizing all of the CPU / GPU across each machine

Most of the time data processing and distributed training go hand in hand, but they don't necessarily have to - however, if you have a leader / worker setup the entire architecture of data processing and ML training is realistically the same thing. You calculate something over slices of data, and aggregate the results, and propogate that back across each worker

In [Spark](/docs/other_concepts/SPARK.md) the above concepts are known as Tasks, Stages, and Shuffling for the most part - tasks are individual logic we can apply on partitions of data, and stages are groupings of tasks separated by shuffling data between workers

In the ML training world, you partition your input data into batches (partitions), you compute some business logic, most of the time it's a forward pass and gradient computation (task), you aggregate the results (map-reduce / aggregation) onto the "coordination worker" who stores the sum of all workers, and then you reveal those gradient updates back to each worker (shuffle)

![Distributed Training Freehand](/img/distributed_training_freehand.png)

Spark is a typical framework for doing distributed training as it's such a robust toolset, but there are so many other frameworks that help to coordinate the leader / worker paradigm and go beyond the typical toolkits that Spark provides - these are led by tools like Ray, Horovod, and the big cloud providers who wrap these up into highly available services

Spark itself only provides some generic toolkits from PySpark MLLib, and Tensorflow-Spark-Connector, but most of the time they work well out of the box

The rest of the below discusses Tensorflow Distributed Architecture, because Tensorflow lends itself to distributed training and tools like Spark, Ray, etc. take advantage of these distribution strategies and package them up for you

The problems below are covered by some distributed computing frameworks like Spark and Ray, and that's what they give you! Highly available and durable training runs:
- **Communication Overhead**: Moving data, activations, and gradients between devices (across PCIe buses on a single machine or network interfaces between machines) takes time and can become a significant bottleneck, especially as the number of workers increases. The ratio of computation time to communication time is a critical factor in determining the efficiency of distributed training
- **Synchronization and Consistency**: Ensuring that all workers are operating on consistent versions of the model parameters is important, particularly in synchronous data parallelism. Asynchronous strategies trade consistency for potential speed, introducing challenges related to gradient staleness
- **Fault Tolerance**: In large distributed systems, worker failures become more probable. A distributed training framework needs mechanisms to handle such failures without losing significant progress
- **Debugging**: Identifying and fixing issues in a distributed environment is inherently more complex than debugging a single-process program. Problems might arise from network issues, synchronization errors, or subtle differences in worker environments

## Distributed Tensorflow
Tensorflow is a generic ML modeling framework that helps to declare certain functionality and relieve some of the crappy numeric optimization and calculation steps that happen in bare-bones deep learning models

Things like overflows, log-mapping, etc... are handled by Tensorflow, and all of the numeric stability and chaining together layers is also handled out of the box

### Distributed Gradient Calculation
The key piece that differentiates parallel, distributed ML training from typical parallel, distributed data processing is setting up the [***Gradient DAG*** computation](/docs/old_math_notes/numerical_computation/index.md#gradient-based-optimization), and efficiently updating the gradient based on the aggregation of it's parts

Taking a function $f(x, y)$, the gradient will most likely be a multi-variable vector showcasing the partial derivatives of each variable with respect to the function $f$, but in our ML context most of the time these computations are chained together

At that point we apply the chain rule across each of these activation functions and computations, and compute the partial derivative for that specific step in the DAG - this is all done in Tensorflow for us, but combining these results so that the aggregation of parts is consistent with doing it all in one place is difficult

Most of the time Tensorflow's strategies, utilizing Mirrored Pooling Strategies, will take the gradients calculated on each worker over each mini-batch and aggregate them using summation or averaging

### Distributed Layers
The other side of the coin is splitting up the gradient DAG, and effectively splitting up the layers - in this scenario you send all data into a worker that processes from layers $[k, k + n)$, and then it would shuffle data to the next worker which computes $[k + n, k + 2n)$ and so on...

![Distributed Layer Freehand](/img/distributed_layer_freehand.png)

This is typically used when a single model and it's weights are literally too large to fit onto one machine, even with a small batch size being fed into it - gigantic LLM's and such may hit snags similar to this, especially when you're checkpointing model weights, historic computations, and other items during highly available training runs

Ultimately this is just performing logic (task) on data partitions, and so you'd expect the same machine to handle different data logic / layer computations - this may not be entirely true, so there are situations where this may be needed

In this setup the gradients and latest layer would need to be shuffled between workers

### Strategies
Tensorflow bakes a few of these strategies into their framework so that you don't have to manage the complexities around updating DAGs or model layers from distributed workers - this involves registering workers, setting up coordination, and ensuring each model checks with each other or some coordinated leader before continuing any training

"The fundamental idea behind `tf.distribute.Strategy` is to encapsulate the intricate details of distributed training coordination"

The tensorflow strategies are meant to allow you to switch between *Local Development Mode* and true *Distributed Training* by wrapping up your local `def train()` function and sending it to each worker - the act of wrapping it up in it of itself marks the task as distributed and a need for coordination, otherwise it just assumes local

`tf.distribute.Strategy` acts as an intermediary between your Keras API training code, and the actual workers, multiple compute devices (CPU / GPU / TPU), and / or multiple processes

**Core Functionality**:
- **Variable Distribution**: It determines how model variables should be created and managed across the available computational devices. For synchronous strategies like MirroredStrategy, this typically involves mirroring variables on each device. For asynchronous strategies, variables might reside on dedicated parameter servers
- **Computation Replication**: It takes the computational graph defined by your model and replicates the forward and backward passes across the participating devices or workers
- **Gradient Aggregation**: It implements the necessary communication protocols (like all-reduce) to collect gradients computed on each replica and aggregate them (usually by summing or averaging) before applying updates to the model variables. This ensures consistent updates in synchronous training
- **Data Distribution**: It integrates with tf.data.Dataset to automatically shard or distribute batches of data to the appropriate devices or workers, ensuring each replica processes a unique portion of the data in each step (for data parallelism)

#### Mirrored Strategy
On a single machine, with multiple GPU or CPU, you might use `tf.distribute.MirroredStrategy`, which creates copies of all model variables (mirror) on each GPU and uses all-reduce to aggregate gradients

![Single Machine Freehand](/img/single_machine_freehand.png)

`MirroredStrategy` is synchronous, meaning all devices must complete their computations before proceeding to the next step, and then shared across to each other GPU before continuing

Altogether it's quite simple:
- Duplicate the model
    - Mirror variables, optimizers, etc onto each device, specifically cloning required variables onto GPU
    - By default it utilizes all available GPUs, but you can specify a subset
    - Entire model and variables need to fit on each GPU
- Split the work / data (***Data Sharding***)
    - Each incoming batch of data is divided evenly across all GPU replicas
    - Example:
        - 4 GPU's 
        - Global batch size of $1,024$
        - Each GPU processes a local batch of $1,024 / 4 = 256$
    - Each GPU computes forward and backward passes independently
        - Each GPU computes the loss and gradients based on its local batch        
- Synchronize the results back together
    - Aggregate gradients using all-reduce from each GPU in a central process
        - May also utilize a library like NVIDIA NCCL for efficient communication from GPU-2-GPU without a central coordinator
    - Update model variables on each GPU with the aggregated gradients to ensure consistency across all replicas
- Continue to the next batch

![Mirrored Strategy Freehand](/img/mirrored_strategy_freehand.png)


#### MultiWorkerMirrored Strategy
For multi-machine setups, `tf.distribute.MultiWorkerMirroredStrategy` extends this concept across multiple machines, coordinating variable updates and gradient aggregation over the network

The TLDR is that we do the same overall distributed strategy, except instead of multi-process communication we now need to do multi-machine communication. Ultimately, it requires us to configure environment variables that specify `host:port` for every worker so that the machines apart of the cluster can reach each other - these are set in the `TF_CONFIG` environment variable on each worker

An example of setting for `worker0` - each worker gets the same config except it's `index: <int>` is supposed to represent which worker it is:
```bash
export TF_CONFIG='{
    "cluster": {
        "worker": ["worker0.example.com:2222", "worker1.example.com:2222"]
    },
    "task": {"type": "worker", "index": 0}
}'
```

For data sharding, compute strategy, and other coordination tactics there's now 2 components - the number of workers, and the number of GPU's on each worker 
- Global Batch Size = # of records in total over all workers
- Machine Batch Size = # of records that are sent to each VM
    - Machine Batch Size = Global Batch Size / # of workers
- Per Task Batch Size = # of records that are sent to each GPU
    - Per Task Batch Size = Machine Batch Size / # of GPUs per worker

So if we have $1,024$ global batch size, $4$ workers, and $4$ GPUs per worker, each VM processes $1,024 / 4 = 256$ samples, and each GPU will ultimately end up processing $1,024 / 4 / 4 = 64$ samples

The gradient calculation, forward pass, and all-reduce synchronization methods are the same, except we now share with many more GPU's that also need networking connectivity

![Multi Worker Freehand](/img/multi_worker_freehand.png)

Some considerations must be taken into account for network shuffle, hyperparameter tuning and learning rate updates, and saving and checkpointing:
- Network shuffle is not a joke - there will be GB of data being passed around workers, and it's important to ensure that the network can handle this load without becoming a bottleneck
- Hyperparameter tuning and learning rate updates may need to be coordinated across workers to ensure consistent training dynamics, and specifically there are `num_replicas_in_sync` extra gradient updates (larger total batch size) so exploding and vanishing gradients are more likely to occur (extra samples added in), particularly when using techniques like gradient accumulation which make debugging difficult
- Saving and checkpointing models must also account for the distributed nature of training, ensuring that all replicas are synchronized and that checkpoints are consistent across workers
    - Having a highly available, durable, and fault tolerant cluster setup is a critical requirement that comes with it's own set of distributed software engineering challenges
    - Typical CAP theorem problems arise, and ensuring consistency while maintaining availability and partition tolerance can be difficult in practice

## Final Thoughts
Distributed training is a useful tool because most deep learning models running on Tensorflow need to use ginormous datasets as input to reach some sort of optimal point, utilizing multiple compute units can speed up this process, but there are so many pitfalls that need to be properly configured to utilize this setup properly

We haven't even covered parallel data processing, data generation, and OOM issues that come with folks trying to shove entire datasets into RAM - a lot of this is covered by `tf.Dataset` objects, which is out of scope for this document, but it's worth noting that efficient data input pipelines are crucial for maximizing the benefits of distributed training - otherwise this is worthless!