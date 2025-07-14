---
layout: technical
title: Communication Protocols
category: Architecture Components
difficulty: Advanced
description: Discussion around Protocols including HTTP, gRPC, and others
---

# Table of Contents
- [Protocols](#protocols)
- [Levels](#levels)
    - [HTTP vs gRPC](#http-vs-grpc)
        - [Serializable Calls](#serializable-calls)
    - [Websockets](#websockets)

## Protocols
The biggest gap most people have in their understanding of distributed systems is the protocols that are used to communicate between the different components

This is a very high level overview of some of the most common protocols used in distributed systems, and how they work - async vs sync, push vs pull, HTTP vs gRPC, etc

## Levels
- **Push:** Server initiates data transfer to client
- **Pull:** Client requests data from server
- **Synchronous:** Client waits for server response before - continuing
    - Communication occurs with a request-response pattern. The sender sends a message and waits for the receiver to acknowledge receipt before continuing
- **Asynchronous:** Client can continue without waiting for server response
    - Communication occurs without waiting for a response. The sender sends a message and continues processing without waiting for the receiver to acknowledge receipt

After that we start getting into weird next levels of things

- **Long Polling:** Client repeatedly requests, server - holds connection until data is available
    - This is a form of pulling, but instead of repeatedly pulling (polling) the server from the client, we request a pull once and then the server holds the connection until it sends data
- **SSE:** Server pushes updates to client over a single - HTTP connection
    - This is a form of push where the client registers a place it can accept connections to, and over time the server, ***in a one-way fashion***, sends data to the client
- **Webhooks:** Both the client and the server open up a [Websocket](#websockets) to each other, and they are able to send data to each other in real time

### HTTP vs gRPC
The TLDR; of these two is that HTTP is useful when you can't have both client and server accessing files inbetween (IDL schema files), and so they have to communicate with generic HTTP messages that send over data in JSON, XML, or other common formats. HTTP API's do typically have open source documentation like OpenAPI / Swagger, which one could argue is a "shared schema"...so maybe this is a moot point

If I setup an API to access some functionality, I don't want to setup the client on every persons phone to have an updated schema definition everytime my schema changes, so I'll just use a generic REST API, but if I have 2 services in my own private network that can have constant CICD and coupled / monitored updates then gRPC is faster and more performant

There's a [sub-document around gRPC](/docs/technical%20writing/architecture_components/communication%20protocols/grpc.md)

ChatGPT answer:
    - HTTP: Best for external-facing APIs where flexibility and compatibility with a wide range of clients (e.g., browsers, mobile apps) are more important than performance.
    - gRPC: Best for internal microservices communication where performance, strict schema enforcement, and features like streaming are critical.

- **HTTP**: A stateless protocol used for communication between clients and servers. It is widely used for RESTful APIs and web applications
    - Example: REST APIs, GraphQL APIs
- **gRPC**: A high-performance, open-source RPC framework that uses HTTP/2 for transport and Protocol Buffers for serialization. It supports bi-directional streaming and is designed for low-latency communication
    - Example: Microservices communication, real-time applications
        - A producer calls a remote function (e.g., processDocument()) on a consumer, which performs the task and returns the result.   
    - Typically more efficient than HTTP for internal communication due to binary serialization (e.g., gRPC)
    - A protocol that allows a program to execute a procedure on a remote server as if it were a local function
    - RPC will ***serialize the data*** and ***the response*** between the different functions, but doesn't necessarily serialize the function itself
        - This is why you need to have IDL schemas in files that can be accessed between the 2 servers
            - IDL: Avro `.avsc`, Proto `.proto`, etc...
            - Then both servers will be able to create getter, setter, and caller methods so that server1 can call server2 which will run a specific function 
```
syntax = "proto3";

service DocumentService {
    rpc ProcessDocument (ProcessDocumentRequest) returns (ProcessDocumentResponse);
}

message ProcessDocumentRequest {
    string arg1 = 1;
    nt32 arg2 = 2;
}

message ProcessDocumentResponse {
    string result = 1;
}
```


#### Serializable Calls
[Celery](/docs/technical%20writing/architecture_components/messaging/Queue/index.md#celery) ***is not gRPC***, but can be thought of in a similar vein where you serialize a function along with it's arguments, and send it somewhere else to be executed

There is nothing new about serializing something to unpack somewhere else



gRPC is actually a superset of HTTP, and is built on top of HTTP/2. It uses Protocol Buffers (protobuf) for serialization, which is more efficient than JSON used in traditional HTTP APIs. gRPC also supports features like authentication, load balancing, and bidirectional streaming.



### WebSockets
- **WebSockets**: A protocol that provides full-duplex communication channels over a single TCP connection - it's used for real-time applications where low latency is required
    - The [RAFT Project](https://github.com/lsprangers/raft-course) from before showcases Websocket protocols