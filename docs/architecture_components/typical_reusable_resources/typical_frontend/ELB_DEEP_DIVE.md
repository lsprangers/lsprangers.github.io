---
layout: technical
title: Elastic Load Balancer Deep Dive
category: Architecture Components
difficulty: Advanced
description: Architecting a Frontend Solution
---

## ELB Deep Dive
Referencing the blog posts:
- [Shlomo ELB Deep Dive](https://shlomoswidler.com/2009/07/elastic-in-elastic-load-balancing-elb/)
- [AWS ELB Architecture](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html)

I wanted to summarize some of the key concepts that kept confusing me around load balancing, DNS, and high availability - the key part is and has always been "how do I give someone a URL that doesn't change, but have the underlying infrastructure be highly available and scalable?"

ELB's actually have 2 levels of elasticity:
1. The ELB itself is elastic - it can scale up and down based on demand, adding and removing load balancer nodes as needed
    - Ensures we aren't limited by a single node's throughput, and that we have highly available entry points into our system
2. The ELB routes to backend targets that can also scale up and down based on demand
    - Ensures we aren't limited by a single node's throughput and connection limit, and that our application is highly available and scalable

Part 1 is handled completely by AWS, and part 2 is handled by you - you need to ensure your backend targets (EC2 instances, containers, IP addresses, Lambda functions) can scale up and down as needed

For DNS, most AWS blogs mention you should use `CNAME` or `Alias` records to point to the ELB's DNS name rather than trying to manage IP addresses directly - this is because ELB's can scale up and down, and their underlying IP addresses can change at any time. By using `CNAME` or `Alias` records, you ensure that your DNS always points to the correct ELB, regardless of its underlying IP addresses

Example flow of a request to `www.example.com` that is backed by an ELB:
- The client makes a DNS query for `www.example.com`
- The DNS resolver looks up the `CNAME` or `Alias` record for `www.example.com`, which points to the ELB's DNS name (e.g., `my-elb-1234567890.us-west-2.elb.amazonaws.com`)
    - The DNS record is hosted in "our" Route53 Hosted Zone
- The DNS resolver then looks up the ELB's DNS name, which resolves to multiple IP addresses associated with the ELB's load balancer nodes
    - The ELB DNS record is managed by Amazon `amazonaws.com` domain 
- The DNS resolver returns one of the IP addresses to the client
- The client connects to the returned IP address, which is one of the ELB's load balancer nodes
- The ELB routes the request to one of its backend targets based on the configured routing rules

![DNS ELB Freehand](/img/dns_elb_freehand.png)

ELB's are distributed, highly available, and fault tolerant - therefore it doesn't have a single IP address. Instead, it has multiple IP addresses across multiple availability zones. When you create an ELB, AWS automatically provisions load balancer nodes in each availability zone you specify. Each node has its own IP address, and the ELB's DNS name resolves to all of these IP addresses. When a client makes a request to the ELB (ELB Service), the DNS resolver (ELB Service + DNS Service) returns one of the IP addresses associated with a load balancer apart of the ELB Service. The client then connects to that IP address, and the LB routes the request to one of its backend targets based on the configured routing rules. ELB is a managed service. Within it you create logical load balancers (ALB, NLB, GWLB). They’re not physical appliances you manage; AWS runs a distributed fleet of LB nodes per AZ and the ELB Service control plane provisions/scales them and publishes the DNS name that resolves to the LB nodes

Most of the above scaling problems could be handled by Round Robin DNS that points to a pool of load balancers which scale up and down, but ELB handles this along with more intelligent routing capabilities, health checks, SSL termination, and integration with other AWS services - making it a comprehensive solution for load balancing in the cloud - *this is why ELB is considered a managed service rather than just a simple load balancer*

### ELB IP Address Distribution and Discovery
ELB's have a pool of underlying IP addresses relating to ELB machines, which are just EC2 instances managed by AWS. This pool ***initially*** containts of one ELB node per AZ, but that pool scales up and down based on demand. Any AZ that has no healthy instances will not receive any traffic

ELB machine scalability is never clearly defined by AWS, but generally they will add more ELB nodes as traffic increases - be it steady or rapidly. Also, the choice of which IP address to serve to a client is not clearly defined - it could be random, round robin, or based on some internal load balancing algorithm. The key point is that the ELB's DNS name resolves to multiple IP addresses, and the DNS resolver returns one of those IP addresses to the client. AWS mentions ELB does round robin among the least-busy backend nodes, and there were discussions of stickiness in the past (same client IP going to same ELB node), but this is not clearly stated anywhere

## How AWS Manages ELB High Availability
So in the backend there's some pool of load balancer nodes (ELB Nodes) which run as EC2 machines in AWS's managed compute plane - how does AWS ensure these ELB nodes register themselves with DNS and stay healthy?
- When an ELB is created, AWS provisions load balancer nodes in each specified AZ
- Each ELB node registers its IP address with the ELB's DNS name in Route53
- AWS continuously monitors the health of each ELB node
    - If an ELB node becomes unhealthy, AWS removes its IP address from the ELB's DNS name
    - If an ELB node becomes healthy again, AWS adds its IP address back to the ELB's DNS name
- As traffic increases, AWS automatically provisions additional ELB nodes and registers their IP addresses with the ELB's DNS name
- As traffic decreases, AWS automatically decommissions ELB nodes and removes their IP addresses from the ELB's DNS name

This is simple in bullet points, but point 2 and point 3 are non-trivial to implement at scale - you'd need a central service registry to keep track of ELB nodes and their health status, and you'd need a way to update DNS records in real-time as ELB nodes come and go. This is likely done using a combination of AWS's internal services and technologies like ZooKeeper or etcd to manage state and coordination among ELB nodes, and is the heart of building out a highly available load balancing service like ELB using Kubernetes or other orchestration platforms

