---
layout: technical
title: DNS
category: AWS SAP
difficulty: Advanced
show_back_link: true
---

## DNS and Route 53
DNS is the backbone for most web services. It translates human-readable domain names (like www.example.com) into IP addresses that computers use to identify each other on the network. AWS Route 53 is a scalable and highly available Domain Name System (DNS) web service designed to route end users to Internet applications by translating domain names into IP addresses

Route53 is the AWS managed DNS service that helps with:
- Domain Registration: You can register new domain names directly through Route 53
- DNS Routing: Route 53 translates domain names into IP addresses, directing user requests to the appropriate resources
- Health Checking: Route 53 can monitor the health of your resources and route traffic away from unhealthy instances
- Traffic Management: Route 53 supports various routing policies, including simple, weighted, latency-based, failover, and geolocation routing
- Integration with other AWS services: Route 53 seamlessly integrates with services like S3, CloudFront, and ELB

### Key Concepts
- Fully Qualified Domain Name (FQDN): The complete domain name for a specific computer, or host, on the internet (e.g., www.example.com)
    - `.com` is the Top-Level Domain (TLD)
    - `example` is the Second-Level Domain (SLD)
    - `www` is a subdomain
- Hosted Zone: A container for records that define how you want to route traffic for a domain and its subdomains
    - Public or Private
    - Can have multiple hosted zones for the same domain (i.e., different environments like dev, test, prod)
    - Private Hosted Zones are only accessible within a specific VPC, and are commonly used for internal DNS resolution within an AWS environment in a service mesh architecture
- Record Sets: Instructions that tell Route 53 how to route traffic for a domain or subdomain (e.g., A records, CNAME records)
    - `A` Record: Maps a domain name to an IPv4 address
    - `AAAA` Record: Maps a domain name to an IPv6 address
    - `CNAME` Record: Maps a domain name to another domain name
        - AKA an `Alias` record in AWS Route 53: A type of DNS record that maps a domain name to an AWS resource, such as an S3 bucket or an ELB
        - Allows us to point multiple URL's to the same resource without needing to manage multiple IP addresses
    - `MX` Record: Specifies mail servers for a domain
    - `TXT` Record: Used to store text information, often for verification purposes
        - i.e. this is just commonly used to verify domain ownership for services like Google Workspace or Microsoft 365
    - `PTR` Record: Maps an IP address to a domain name (reverse DNS lookup)
- TTL (Time to Live): The duration in seconds that a DNS record is cached by DNS resolvers
- Heartbeat: A health check mechanism that monitors the availability of resources and routes traffic accordingly
    - Route53 servers themselves can send heartbeats to endpoints to check their health
        - TCP, HTTP, HTTPS
        - Can be configured to check at regular intervals and take action if a resource is deemed unhealthy
        - An unhealthy resource can be removed from rotation, and traffic can be routed to healthy resources instead

In an AWS VPC, AWS will autoamtically create `NS` and `SOA` records for the VPC's DNS resolution:
- `NS` (Name Server) Record: Specifies the authoritative name servers for the domain
- `SOA` (Start of Authority) Record: Provides information about the domain, including the primary name server, email of the domain administrator, domain serial number, and refresh timers

#### AWS Hosted Zone, Record Set, and ALB Example
- `quick24x7.local` is our pretend domain name
- Private hosted zone are tied to one or many VPC's
    - Any instances / services within this VPC can resolve DNS queries for this domain
- We have multiple record sets defined within this hosted zone
    - An `A` record for `app.quick24x7.local` pointing to an internal IP address of an EC2 instance
    - A `CNAME` record for `db.quick24x7.local` pointing to an RDS endpoint

The above is fine, but the EC2 instance may go down and restart, and at that point would have a new IP address...if we scale up our services to multiple K8 pods with multiple underlying instances, etc it becomes unruly to manage IP addresses directly. Instead, we can use an `Alias` record to point to an AWS resource that can handle this for us, like an ELB

- The `Alias` record for `service.quick24x7.local` points to an ELB
    - The ELB can distribute traffic across multiple EC2 instances, containers, or IP addresses
    - If instances go down or are added, the ELB automatically adjusts, and the DNS record remains valid without needing to update IP addresses manually

An ALB or NLB will typically have static DNS names that do not change, so using an `Alias` record to point to the load balancer's DNS name ensures that traffic is always routed correctly, even as the underlying infrastructure changes...the way that these load balancers keep their own static URL is outside the scope of this topic, but is a key part of how AWS manages infrastructure behind the scenes

There are some [Stack Overflow Questions](https://serverfault.com/questions/1167031/how-do-application-load-balancers-maintain-high-availability-without-a-stable-ip) about this, which lead to other [Stack Overflow Answers](https://stackoverflow.com/questions/35313134/assigning-static-ip-address-to-aws-load-balancer/35317682#35317682) that go into more detail

And now I summarized these concepts in a [Load Balancing and ELB Deep Dive](/docs/architecture_components/typical_reusable_resources/typical_frontend/ELB_DEEP_DIVE.md) document

The general idea is that ALB will have a static DNS name that resolves to multiple IP addresses across zones, and as ALB's scale their backing IP addresses constantly change - therefore, to ensure DNS stays available and valid we would point to the ALB's DNS name via an `Alias` record / `CNAME` record rather than trying to manage IP addresses directly. Below shows how we can route a few different services using `Alias` and `CNAME` records:
```
service.quick24x7.local  IN  A     ALIAS  dualstack.my-alb-1234567890.us-west-2.elb.amazonaws.com
app.quick24x7.local      IN  A     ALIAS  dualstack.my-alb-1234567890.us-west-2.elb.amazonaws.com
db.quick24x7.local       IN  CNAME  mydatabase.abcdefg.us-west-2.rds.amazonaws.com
app.quick24x7.local      IN  A     ALIAS  dualstack.my-alb-1234567890.us-west-2.elb.amazonaws.com      
```

And in this situation, `dualstack.my-alb-1234567890.us-west-2.elb.amazonaws.com` itself will most likely resolve to multiple IP addresses that are managed by AWS behind the scenes, and can change over time as the ALB scales or underlying infrastructure changes

[This is a great blog on the topic](https://shlomoswidler.com/2009/07/elastic-in-elastic-load-balancing-elb/) that goes into more detail on how ELB's manage their own IP addresses behind the scenes, and then the [AWS Example at the bottom section](#how-aws-alb--nlb-work-without-static-ips) goes into more detail on how AWS manages this specifically for ALB / NLB

### Routing and Traffic Policies
Routing policies give granular control of DNS name resolution and resources users get directed to - this ultimately helps with speed, availability, and cost optimization. Some common routing policies include:
- **Simple Routing**: Routes traffic to a single resource
- **Weighted Routing**: Distributes traffic across multiple resources based on assigned weights
    - A rule with a value of 10 would get double the traffic as a rule with a weight of 5
    - Multiple DNS records that would have the same name and type, but different values and weights
        - An example would be having two web servers behind two different ALB's, and we want to send 70% of traffic to one and 30% to the other for testing purposes
        - `CNAME www.example.com` with weight 70 pointing to `alb-1.example.com`
        - `CNAME www.example.com` with weight 30 pointing to `alb-2.example.com`
    - Routing is just `weight / sum(all_weights)` to get the percentage of traffic going to each resource
- **Latency-Based Routing**: Routes traffic to the resource with the lowest latency for the user
    - Used when the same service is running in different AWS data centers (regions)
    - Route53 measures latency from the user's location to each AWS region and routes them to the region with the lowest latency
    - Regions are 1:1 with AWS data centers
- **Failover Routing**: Routes traffic to a secondary resource if the primary resource is unhealthy
    - Active-passive failover, so only one resource is active at a time, and the secondary one is used for high availability if the first one goes down 
    - "Going down" would be determined by health checks configured in Route53
    - Define primary and secondary resources in the record sets themselves
- **Geolocation Routing**: Routes traffic based on the geographic location of the user
    - Based on origin of client DNS queries
    - Continent, country, or state level routing
    - Useful for compliance with data residency requirements, or to provide localized content
- **Multi-Value Answer Routing**: Returns multiple IP addresses in response to DNS queries, allowing clients to choose from multiple resources
    - Similar to simple routing, but can return multiple healthy resources
    - Health checks can be associated with each resource, and only healthy resources are returned in DNS
    - Allows up to 8 potential query results
- **IP Based Routing**: Routes traffic based on the IP address of the user
    - Can create rules to route traffic from specific IP ranges to different resources
    - Useful for implementing access controls or directing traffic from known locations to specific endpoints
    - Also helps dealing with VPN, DDoS, corporate data center traffic, etc...

### DHCP Options Set and VPC DNS Settings
In a VPC we can set custom DNS settings for instances launched within that VPC:
- Enable DNS Hostnames: When enabled, instances launched in the VPC receive DNS hostnames
- Enable DNS Support: When enabled, the Amazon-provided DNS server in the VPC resolves DNS hostnames to IP addresses
These settings are important for ensuring that instances can resolve domain names correctly within the VPC environment

Can enable things via ***DHCP Option Set***:
- The DHCP options set allows us to configure DNS servers, domain names, and other network settings for instances in the VPC
    - `ec2.internal` is the default domain name for instances in a VPC
    - The default domain name is what's attached to the end of the instance's private DNS name
- We can specify custom DNS servers if needed, or use the Amazon-provided DNS server
    - These allow instances to resolve both internal and external domain names using a custom DNS server, but we'd have to provide the DNS server IP addresses ourselves to the DHCP options set
    - The DHCP option set would change the results of commands such as `ipconfig /all` on Windows or `cat /etc/resolv.conf` on Linux to show the custom DNS server IP addresses
- The domain name specified in the DHCP options set is appended to unqualified DNS queries, helping with name resolution within the VPC

### Firewalls
Firewalls are essential for securing network traffic and controlling access to resources. In AWS, firewalls can be implemented using DNS Firewalls, Security Groups and Network ACLs (Access Control Lists):
- **Security Groups**: Act as virtual firewalls for instances to control inbound and outbound traffic
    - Stateful: If an incoming request is allowed, the response is automatically allowed, regardless of outbound rules
    - Rules can be based on IP addresses, protocols, and ports
    - Applied at the instance level
- **Network ACLs**: Act as stateless firewalls for subnets to control inbound and outbound traffic
    - Stateless: Each request and response is evaluated against the rules independently
    - Rules can be based on IP addresses, protocols, and ports
    - Applied at the subnet level
- **DNS Firewall**: A managed service that allows us to filter and monitor DNS traffic
    - Can create rules to block or allow specific domain names or patterns
    - Helps protect against DNS-based threats, such as phishing or malware
    - Integrates with Route 53 Resolver to provide DNS filtering for VPCs

DNS Firewalls allow us to ensure our DNS queries are secure and compliant with organizational policies, and so if we have specific domains we want to block or allow, we can set up rules accordingly

So this section is around DNS Firewalls specifically:
- DNS Firewall allows us to create rules that filter DNS queries based on domain names or patterns
    - Can block access to malicious or unwanted domains
    - Can allow access to specific domains while blocking others
- DNS Firewall rules can be associated with VPCs to enforce DNS filtering for instances within those VPCs
- DNS Firewall provides logging and monitoring capabilities to track DNS query activity and identify potential threats
- DNS Firewall integrates with AWS services like Route 53 Resolver and CloudWatch for enhanced security monitoring and alerting


## How AWS ALB / NLB work without static IP's
[This is a great blog on the topic](https://shlomoswidler.com/2009/07/elastic-in-elastic-load-balancing-elb/) that goes into more detail on how ELB's manage their own IP addresses behind the scenes

