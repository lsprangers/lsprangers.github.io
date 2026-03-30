---
layout: technical
title: Event Loop + CPU and I/O Bound ML Example
category: Event Loop
difficulty: Advanced
description: Discussions around Event Driven Software
show_back_link: true
---

## Event Loop
The first start of any event driven software system is the event loop - which is just a continuous, non-blocking, asynchronous loop that pushes new requests to other queue's / files to handle later on by some other process
```python
while True:
    # Blocks until some registered file descriptors are ready, with an optional timeout
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            # New connection ready to be accepted
            accept_wrapper(key.fileobj)
        else:
            # Existing connection ready for I/O service
            service_connection(key, mask)
```

Event loops are core components in API's, streaming frameworks, and pretty much anything software, coupling this with concurrency, multi-threading, multi-processing, etc in different languages like Python (which has the GIL issue), Java, C++, etc all means there's no "one size fits all" solution

![Python Event Loop](/img/python_event_loop2.png)

Covering the main aspects, theory, and implementations of event loops in Python first without parallel multi-threading, and then in Java / Go which utilize different mechanisms for concurrency and multi-threading, will give us a good start to how events can be processed in different languages

The main use case of an event loop is to have something (a thread) that can accept connections over multiple [sockets](/docs/event_driven_architecture/event_driven_software/SOCKETS.md), and can pass on these connections and future work to other processes / threads to do actual work. The event loop should continuously run and ensure that as soon as a new connection reaches a socket, it's ingested to be processed. There's no way to continuously check [sockets](/docs/event_driven_architecture/event_driven_software/SOCKETS.md) except for a `while True:` loop

There's more theory in the [sockets document](/docs/event_driven_architecture/event_driven_software/SOCKETS.md) around:
- [Select](/docs/event_driven_architecture/event_driven_software/SOCKETS.md#select)
- [A proper application server](/docs/event_driven_architecture/event_driven_software/SOCKETS.md#proper-application-server)
- [I/O vs CPU Bound](/docs/event_driven_architecture/event_driven_software/SOCKETS.md#io-bound-vs-cpu-bound)
    - Event loops can be blocked by CPU Bound work in a single threaded (Python GIL) environment, and so they're best for I/O bound work or passing off work to other processes
    - AsyncIO and other frameworks help with I/O bound applications, they won't do much for CPU bound
    - We can copy a model-per-process in Python to get to multi-processing CPU abilities, but the memory and communication overhead is high
        - Outside of that, there needs to be centralized communication between processes which typically involves queue's, pipes, etc from the main `multiprocessing` fork. If this main portion fails, there's no graceful recovery
        - `multiprocessing` does allow for listeners and clients which are wrapped up `sockets` with `send() and recv()` implemented

<!-- Collapsible Python snippet -->
<details>
  <summary>Show Python Script</summary>

```python
import selectors
import socket
import types

# Create a default selector
sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    """Handles accepting a new connection."""
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # Register the new connection for reading
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    """Services an existing connection."""
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)
            if recv_data:
                data.inb += recv_data
                data.outb += b"Echo: " + recv_data # Prepare response
            else:
                # Connection closed by client
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
        except BlockingIOError:
            pass # Expected in non-blocking mode

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            try:
                # Send the response
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
            except BlockingIOError:
                pass # Expected in non-blocking mode

# Set up the listening socket
host = '127.0.0.1'
port = 65432
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
lsock.setblocking(False)
print(f"Listening on {(host, port)}")

# Register the listening socket with the selector to monitor for read events (new connections)
sel.register(lsock, selectors.EVENT_READ, data=None)

# The main event loop
try:
    while True:
        # Blocks until some registered file descriptors are ready, with an optional timeout
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                # New connection ready to be accepted
                accept_wrapper(key.fileobj)
            else:
                # Existing connection ready for I/O service
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
    lsock.close()
```

</details>


### Callbacks
Callbacks are essential as they allow the main event loop thread to communicate with other processes / threads - the background processes need to return the output, results, event, etc back to the main thread to return back to the client. A callback is registered to handle the result of an operation (like a network request, file read, or ML inference). So when the operation finishes (possibly in the background), the event loop or worker thread invokes the callback, passing it the result - this allows the main thread to remain responsive and not block while waiting for this background operation to complete

![Event Loop Callbacks](/img/event_loop_callbacks.png)

In something like Java, the typical event loop for an ML model inference would revolve around accepting new POST requests from a client, and passing off the actual request to background processes in true parallel processing fashion:
- Event Loop Thread
    - Listening on a specific Socket (IP + Port)
    - Accepts the client POST request
    - Submits the ML inference task to a thread pool
    - Registers a callback (often as a lambda or via `Future`/`CompletableFuture`
- Worker thread(s) on another core
    - Runs the ML inference in the background
    - When done, the worker thread itself executes the callback
- Callback
    - The callback (which sends the result back to the client) is executed by the worker thread that finished the task
    - If you want the response to be sent from the main event loop thread (for thread safety or framework requirements), you must explicitly schedule the callback to run on the event loop thread (e.g., using a queue or framework method)

```java
ExecutorService pool = Executors.newFixedThreadPool(10);

void handlePostRequest(Request req) {
    pool.submit(() -> {
        Result result = runMLInference(req.data);
        // This callback runs in the worker thread!
        sendResponseToClient(req, result);
    });
}
```

## ML Inference Example
ML Inference is typically a useful example as you have high I/O procesing when a client sends a request to get the model output, and in the middle there may need to be features, cache lookups, etc done alongside the input data (like user items), and then it turns into a CPU bound process to actually run model weights against input before returning it to the client

So how can we build a low latency, high concurrency, CPU / GPU saturated model serving framework? Start by looking at requirements:
- Need to ensure all CPU / GPU are utilized to their fullest abilities
    - Need to ensure batching is done
    - Model per core, or even multiple model per core
- CPU needs to handle I/O and offloading to background processed
    - Extremely high I/O rates (1,000+ req/second throughput) from clients and any databases / lookups
    - All the rest of the CPU / GPU cores can be completely utilized for inference (CPU bound)
- Read heavy workload, models won't be changing inside of the actual containers

There can be an orchestration layer that handles I/O, client connectivity, etc in one language that calls CPU bound heavy workloads in another language. Data serialization between the two can be done via [gRPC](/docs/architecture_components/communication protocols/grpc.md) so that each language can efficiently serialize and deserialize incoming data. This doesn't force microservices on us as this can all be deployed in containers on a singular VM based on the number of cores on each, or this could be migrated out into microservices as well fronted by load balancers - no major difference other than network hops and discovery. Funny enough, this is how [NVIDIA Triton Servers](https://resources.nvidia.com/en-us-ai-inference-content/accelerated-inference) are setup to run, including [Triton gRPC](https://github.com/triton-inference-server/server/blob/main/docs/customization_guide/inference_protocols.md), [Triton Batching](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/batcher.md), and [Triton Caching](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/response_cache.md)

![NVIDIA Triton Decoupling](/img/nvidia_triton_decoupling.png)

There are a few languages / options we can utilize with different pros / cons:
- **Python** is the usual choice, but it doesn't work well for true parallel processing. It can cover I/O bound applications via AsyncIO, but has a poor environment for utilizing all CPU / GPU for a model outside of the `multiprocessing` module
    - Main thread would need to do all of the batching, I/O, scheduling, etc and use multiprocessing on all other cores to spin up models and have them run actual inference
- **Rust** is the most performant, but is (in my personal opinion) quite possibly the most disgusting language in the world to work in. It has true parallelism capabilities, and great request / response patterns along with saturating all CPU / GPU on a machine
- **Go** is easier to work in than Rust, but less performant
- **Java** is easier to work in than Rust, but less performant
- ***Rust, Java, and Go*** all have some form of native support for Tensorflow, PyTorch, etc based models for serving, but there would need to be some pre-processing that's completed or the model may need to change to be serialized into these languages as Python dumping out a `pickle.dump(model_weights)` may not be 100% supported in each language
    - Furthermore the pre-processing of inputs may need to change for each of these languages to support proper data types 
    - All of these languages have true I/O bound + parallelism for CPU bound work, and scheduling models on cores and tying them to different abstract processed with proper communication channels


### Low Latency Monolith Deployment
The best setup for low latency ($\lt$ 40ms) inference with concurrency will start with a monolith split up between an orchestration process (Go, Python, etc) and GPU based inference processes (C++, Python calling C++) where inter-process communication (IPC) happens via gRPC or low level sockets / pipes. For this example we'll stick with Python as the AsyncI/O framework, and C++ as the inference process that interacts with NVIDIA A100 GPU's on a device

We'll host BART-large on each GPU which requires:
- 413 MB of VRAM to load in float16 precision for inference
    - For transformer models in `fp16` (half-precision), you typically need 2GB of VRAM per 1 billion parameters for weights alone
    - Add 20% on top for activations, framework overhead, etc

Triton is a good example of how all of this would actually look if we wrote out C++ code to interact with GPU's, and created some sort of client API to send requests, and had a C handler API to actually interact with backend processing - it's very complicated 

#### Triton Walkthrough For gRPC
The actual gRPC API that handles accepting new inference calls can be modeled after the ***Triton*** example:
- [gRPC New Request](https://github.com/triton-inference-server/server/blob/main/src/grpc/infer_handler.cc#L671)
    - That `RequestModelInfer` call is the async-server pattern in gRPC C++: it requests that gRPC match an incoming `ModelInfer` RPC to this state and enqueue an event on the completion queue (`cq_`) when it arrives
        - `RequestModelInfer` eventually comes through as "gRPC runtime, please notify me (via the completion queue) when the next `ModelInfer` call arrives, and bind it to this state object"
        - i.e., when you accept one client request, you must re-arm yourself for future requests. So it's a continuous "I received this one, send me more"
    - In gRPC async C++ servers, “accepting” an RPC is not implicit and doesn't release unless you keep posting receives
- [gRPC Process Request](https://github.com/triton-inference-server/server/blob/main/src/grpc/infer_handler.cc#L680)
    - When a request has `step.START` it will 
        - [start a new request `StartNewRequest`](https://github.com/triton-inference-server/server/blob/main/src/grpc/infer_handler.cc#L731) which posts another `service_->RequestModelInfer(...)` so the server is ready for the next incoming call
        - [Runs `Execute()`](https://github.com/triton-inference-server/server/blob/main/src/grpc/infer_handler.cc#L779) to process the current state
- Processing a request is eventually done by [`TRITONSERVER_ServerInferAsync`](https://github.com/triton-inference-server/server/blob/main/src/grpc/infer_handler.cc#L1005) which is the C API entry point that submits an inference request to the Triton core for asynchronous execution
    - This will immediately return (if Triton Core accepts it), and then the results come back later on via callbacks that were registered in `TRITONSERVER_InferenceRequest`
    - Triton then creates `TRITONSERVER_InferenceResponse` and delivers them via response callback
    - The [response allocators](https://github.com/triton-inference-server/server/blob/main/src/grpc/infer_handler.cc#L974) are how Triton knows where, how, and what to send back and the structure of the actual response buffer

Actual inference is then handled in [Triton Core Repo](https://github.com/triton-inference-server/core/)
- The [Dynamic Batch Scheduler](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc) covers dynamic batching of new gRPC requests
    - This will [create and enqueue a request](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L185)
        - Potentially do a [cache lookup if enabled](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L218)
    - If not dynamic batching, [immediately send the request](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L218)
    - Otherwise [add to batcher](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L218), [enqueue it](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L218) into schedulers internal priority queue, [decide to wake up batching thread](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L218), and if woken up start the actual call with [`cv_notify`](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#284)
- Every new gRPC request becomes an `InferenceRequest`, and is added to the scheduler via `Enqueue()`
- In Dynamic Batching, there's [a new thread created if it doesn't exist](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L218)
    - The thread itself runs the [`BatcherThread` method](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L302)
        - This creates payloads
        - Waits for [Execution PayloadSlots](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L367)
        - Also waits for [GetDynamicBatch()](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L379) to return
            - This walks over the enqueue'd requests
            - Ensures it's not larger than `max_batch_request_size`
            - Returns `0` when it's finally ready to send a pre-set batch size
                - If 0, constructs a [`curr_payload`](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L389)
                - Continuously dequeue's these requests 
            - Eventually, it'll [finally enqueue a payload to the model!](https://github.com/triton-inference-server/core/blob/main/src/dynamic_batch_scheduler.cc#L437)

#### Low Latency Monolith Realistically
Given no one wants to write any of the above code ever again, the best bet is to write clients that utilize an open source serving framework for the actual inference runtimes
- Triton is great for true low latency, high concurrency, parallel inference that works on NVIDIA GPU's, or any CPU
    - Can serve any model with custom configs, and has pre-sets for ONNX, Tensorflow, PyTorch, etc
    - This specifically allows for multi-GPU clusters
- Ray Serve is a useful framework for distributed processing, potentially semi real-time, but more useful for non real-time scenario's that need distributed compute and processing
    - Pipelines, reinforcement learning, enqueue'd distributed serving ($\lt$ 1s), etc
    - Work with both GPU or CPU workers
- Tensorflow Serve is useful for Tensorflow only, and somewhere inbetween Triton and Ray Serve
