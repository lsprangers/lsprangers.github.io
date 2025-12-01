---
title: Generic Networking
layout: default
---

## Generic Networking
Going to dump the high level networking topics from OSI cert class, AWS Networking certs, a [Random Medium Article](https://medium.com/the-modern-scientist/networking-in-a-hurry-51455db8b72a) and anything else in general around hypothetical and real world uses of networking

### Theoretical
At a high level there are multiple components put into networking, and most are placed into 7 layers of the OSI model
- **L1: Physical**: Converts frames into bits and transmits them as electrical signals
    - This is the literal hardware sending electrical pulses around the world
- **L2: Data Link**: Groups packets into frames and manages physical addressing
    - One level up, we start to group packets together with common address schemas of where they need to go
- **L3: Network**: Handles logical addressing (IP addresses) and routing of packets across networks
    - This handles the implementation of routing packets efficiently
- **L4: Transport**: Breaks data into segments, ensures reliable delivery, and manages flow control via port numbers
    - Ensures that data gets to where it should be going, and helps to create reliable guarantees for packets
- **L5: Session**: Manages the establishment, maintenance, and termination of connections and sessions between applications
    - This ultimately deals with computer-2-computer sessions and allowing packets to be sent between computers
- **L6: Presentation**: Handles data formatting, encryption, and compression
    - Ensures data is in a usable format, and starts to put security and optimizations on top of raw data
- **L7: Application**: Provides network services directly to end-user applications
    - This is the layer closest to the end user, dealing with high-level protocols and services like HTTP, FTP, and SMTP

Each of these are a theoretical implementation that is a "tech spec" in which imlpementing companies try to adhere to 

#### Common Protocols
Each of the protocols below will build on top of each other, implementing new rules and contracts which ultimately help facilitate multiple different paradigms such as video streaming, email, high frequency trading, etc by utilizing different pieces of the puzzle

Each layer will have different protocols, data units, and use cases

![Protocols_Layers](/img/protocols_layers.png)

- **Ethernet/Wi-Fi**: Data link layer protocols for local area networking
    - This sits at Layer 2 of OSI model, Ethernet is used for wired connections, while Wi-Fi is used for wireless connections    
- **IP**: Network layer protocol for addressing and routing packets
    - This sits at Layer 3 of OSI model, responsible for logical addressing and routing packets across networks
- **TCP/UDP**: Transport layer protocols for reliable and unreliable data transmission
    - This sits at Layer 4 of OSI model, TCP is connection-oriented and ensures reliable delivery, while UDP is connectionless and faster but less reliable
- **HTTP/HTTPS**: Application layer protocols for web communication
    - This sits at Layer 7 of OSI model, deals with web traffic, and typically relates to web browsers and servers
    - Typical operations:
        - GET: Retrieve data from a server
        - POST: Send data to a server
        - PUT: Update existing data on a server
        - DELETE: Remove data from a server

#### Alice Bob Example
Alice and Bob are commonly used expressions in networking that relate to 2 parties trying to efficiently, securely, and remotely communicate 

- Alice's Request (local laptop) to Bob's Server (AWS VPC) `www.bob.com`
    1. Alice's Intent: Alice wants to access a webpage hosted on Bob's server
    2. Private IP + MAC Address: Alice's laptop has a private IP address (e.g. 192.168.1.2) in her Local Area Network (LAN) and a unique MAC address (e.g. 00:1A:2B:3C:4D:5E) tied to her network interface card (NIC)
        - Essentially your laptop and TV and everything in your home has a private IP address that is only reachable within your home network (LAN)
        - The MAC address is a hardware identifier that is unique to your device's network interface
        - The router in Alice's home network has a public IP address (e.g. 203.0.113.1) that is used for communication outside the home network
    3. DNS Query: Alice's device checks it's DNS cache for Bob's Server's IP address, if it's not there a DNS query is sent to resolve Bob's domain name `www.bob.com` to it's public IP address
        - The flow is discussed in [DNS Page](/docs/architecture_components/typical_reusable_resources/typical_frontend/DNS.md)
    4. DNS Cache Update: Alice's device will update it's local cache of Bob's Server's IP address if it's found
- Networking Layers
    1. Application Layer (HTTP Request): Alice's browser creates an HTTP `GET` request, focused on GETTING the `.html` and other files from Bob's webserver
    2. Transport Layer (TCP Segmentation): This request gets segemented by TCP
        - The actual `GET` request might be $230$ bytes total, and it would probably get padded to some total length like $256$, and then chunked into divisible segments
        - Each of these segments is called a TCP Segment, and these are what get sent over the network individually with TCP specific segment sequence ID's
            - This helps to ensure reliable delivery and proper sequencing of data (i.e. Bob's Server can check it's got all of the data, and can reorder segments if they arrive out of order)
    3. Network Layer (IP Datagram): Each TCP segment is then encapsulated in an IP datagram, this datagram includes Alice's private IP as the source and Bob's public IP as the destination
    4. Data Link Laye (Ethernet Frame): The IP datagram is further encapsulated into an Ethernet frame, which'll include Alice's MAC address and her router's MAC address
        - This gets turned into electrical signals or radio waves that travel over the physical medium (e.g., Ethernet cable, Wi-Fi)
- On the Road NAT + Routing
    1. NAT at Alice's Router: Alice's router uses Network Address Translation (NAT) to replace Alice's private IP with it's own public IP in the outgoing packets
    2. Routing over Internet: THese datagrams traverse the internet, hopping through routers using a variety of protocols (BGP, etc?) - in this process, routers use routing tables to determine the best path to the destination IP address. Payload is completely ignored, and routing is just done to figure out best path to source IP from destinations
- Entering Bob's Domain - VPC + Security
    1. Bob's VPC: Bob's server in Amazon VPC will sit in an isolated network within an AWS datacenter
        - Security groups will manage what data can enter and leave Bob's server, and they are stateful meaning if Alice's traffic can enter they'll allow it to leave back to Alice's server
        - Bob's SG will most likely allow ingress from all public IP's, or maybe just a select few that would include Alice's public IP (router)
    2. CGNAT in AWS: After reaching AWS, Alice's public IP based request is translated into an internal private IP using Carrier Grade NAT (CGNAT) which is then allowed to get into Bob's Server
- Bob's Server
    1. Data Reception: Bob's server receives the request - tons of examples of `socket` programming in various languages, or using a framework like FastAPI, Flask, or Express.js
        - These all handle the TCP/IP stack and provide abstractions for dealing with incoming network data
        - The server's TCP stack reassembles the segments into the original HTTP request
    2. HTTP processing: HTTP request is then processes by the application layer on Bob's server, and then will most likely interact with a database, file storage, etc... (backend processing) and return a request of `.html`, `.js`, and other content types
    3. If HTTPS is involved, there's a number of security and TLS considerations that happen before any processing is done, and this can typically be offloaded to 3rd party services
- Response back to Alice
    1. Bob's server creates an HTTP response
    2. Everything gets reversed, and Bob's server takes that HTTP response and sends it back through the network layers, eventually reaching Alice's device
    3. The return route datagrams are handled by the same internet provider and returned back to Alice's router with the internet provider's public IP replaced by Alice's private IP via NAT
- Completing the cycle
    1. NAT at Alice's Router: Alice's router translates the public IP back to Alice's private IP and forwards the ethernet frame to Alice's device
    2. Response delivery: Alice's device receives the response and processes it, completing the communication cycle

#### Concepts
1. Private and Public IP
    - Private IP: Device's will have a private IP inside a LAN, which ultimately gets translated to a public IP for internet communication when going through a router or ENI
    - Public IP: The IP address that is visible on the internet, assigned by the ISP or cloud provider, used for routing traffic to and from the device
2. DNS Query and Cache
    - DNS Query is how a domain name get's resolved into a public IP address that's findable over an internet provider
    - DNS Cache is a temporary storage of DNS query results to speed up subsequent requests for the same domain
3. TCP Segmentation and Reassembly
    - Segmentation is breaking down a message into manageable segments, each with a sequence number for re-assembly
    - Reassembly is the process of putting the segments back together in the correct order to reconstruct the original message
4. IP datagram and routing
    - IP Datagram: Each TCP segment is encapsulated in an IP datagram, which contains the source and destination IP addresses
    - Routing: Routers direct the datagram through the network based on the destination IP address
    - Multiprotocol Label Switching (MPLS) is an alternative method used in some specific networking strategies for more efficient routing
        - There are tons of specific implementations of this as well, all are dependent on situation and environment
5. Ethernet Frame and MAC Address
    - Ethernet Frame: The data link layer encapsulates the IP datagram into an Ethernet frame, which includes source and destination MAC addresses
    - MAC Address: A unique identifier assigned to network interfaces for communications on the physical network segment
6. NAT (Network Address Translation)
    - NAT is a method used by routers to translate private IP addresses to a public IP address and vice versa, enabling multiple devices on a local network to access the internet using a single public IP address
    - From Reddit ELI5: " Every device on the internet has an IP address. This address must be unique, there can be no two devices with the same IP. The number of IP addresses is limited, and mostly used up. There is a group of addresses that have been reserved for use only in internal networks. This works because the devices sharing an address cannot see each other - they are on different networks with no route between them. Nat is implemented by a device (a computer, a router, or a firewall) that has two network connections, one to the internal network, one to the internet. When a device on the internal network wants to connect outside, it sends its messages (packets) to the NAT device. The NAT device strips the address of the original device and substitutes its own, then sends it out to the internet. When the reply comes back, the NAT device then strips its own address, substitutes the address of the original device, and sends it to the internal network."
7. Handshakes
    - Initiation: Alice's browser initiates a connection with Bob's server by sending a TCP segment with `SYN`flag set
    - Acknowledgement: Bob's erver ack's this request by sending back a TCP `SYN-ACK` flags set
    - Final agreement: Alice's device responds with an `ACK` flag, completing the handshake
    - Purpose: Ensures both parties are ready for communicating
        - This handshake is extended by TLS in the future, including ways to authenticate that Bob is Bob and Alice is Alice
8. Firewalls and protocols
    - Firewalls: Software or Hardware based systems to enforce security rules
    - Protocols: PPP (Point-To-Point Protocol) is an alternative for direct connection between 2 nodes
9. Stateful vs Stateless
    - Stateful: These remember the state of previous packets / handshakes, and ultimately allows new packets based on established connections
    - Stateless: Makes decisions based purely on current packet without memory of past interactions
10. Headers
    - Metadata and Headers are used to provide information about the data being transmitted, such as source, destination, protocol, and other control information
    - Used in both TCP and IP fragments, and essentially are `k:v` pairs with information about the packet
11. Fragments and Bytes
    - Fragments are large IP datagrams that can be broken into smaller fragments that fit the MTU (Maximum Transmission Unit) of the network
    - Bytes: Each fragment and packet consists of bytes which are the base unit of digital data transmission
12. Sequence Numbers
    - These are used in TCP to order segments and ensure data is reassembled correctly

Some other concepts listed, but mostly are just repeat of above

### AWS VPC
Most of this was removed and now covered in [AWS SAP Networking](/docs/aws_sap/NETWORKING.md) AWS Solutions Architect area

The TLDR of AWS is:
- Internet Gateways are resources that allow subnets to reach the internet
    - Routing rules to IGW can reach the internet, and vice versa
- Transit Gateways allow for a hub-and-spoke VPC connectivity pattern
    - In the past this was done via VPC Peering, which meant $n^2$ connections for $n$ VPCs
- VPC Endpoints allow private connections between VPCs and AWS services without using the internet (AWS backbone)
    - They do not explicitly provide access across VPC's though - cross VPC private exposure goes through PrivateLink
- Security groups are stateful (return traffic auto allowed) firewalls for resources that operate at the ENI / Instance level
- ACL's are stateless (each new request is checked) firewall rules at the subnet boundary level

Tons more on actual networking over internet, on AWS backbone, and protecting servers along with load balancing, DNS, and service discovery which are all incredibly important topics in networking in the [AWS SAP Networking](/docs/aws_sap/NETWORKING.md) doc

### TCP vs UDP
TCP (Transmission Control Protocol) is a connection-oriented protocol that ensures reliable data transfer through error checking and acknowledgment mechanisms. UDP (User Datagram Protocol) is a connectionless protocol that allows for faster, but less reliable, data transmission without guaranteed delivery. Each has their specific use cases, and typically are the building blocks for higher level protocols like video streaming (DASH, HLS), gaming, VoIP, etc...

TCP:
- Connection-oriented: Establishes a connection before data transfer
- Reliable: Ensures data is delivered accurately and in order
- Error checking: Uses checksums and acknowledgments to verify data integrity
- Flow control: Manages data flow to prevent congestion
- Use cases: Web browsing (HTTP/HTTPS), email (SMTP), file transfers (FTP

UDP:
- Connectionless: No connection establishment before data transfer
- Unreliable: No guarantee of data delivery or order
- Minimal error checking: Basic checksums for data integrity
- No flow control: Sends data without managing congestion
- Use cases: Video streaming, online gaming, VoIP

### Alice and Bob With UDP
Using UDP, Alice sends a video stream to Bob without establishing a connection. Each video packet is sent independently, and Bob may receive packets out of order or miss some entirely. This is acceptable for real-time applications like video streaming, where speed is prioritized over perfect accuracy

- Alice Request:
    1. Streaming Intent: Alice wants to watch a live video stream hosted on Bob's server
    2. Private IP + MAC Address: Same as TCP example
- Setup:
    1. No DNS cache or query needed if Alice already has Bob's public IP for streaming
    2. Datagram creation happens directly without handshakes, where Alice's device sends a UDP datagram to request the stream
        - There is no segmentation or sequence numbers, each packet is independent
    3. No handshakes are performed, as UDP is connectionless
- UDP 
    1. Application Layer (Video Stream): Alice's video player sends video data packets using UDP protocol
    2. Transport Layer (UDP Datagram): Each video packet is encapsulated in a UDP datagram with source and destination ports
    3. Network Layer (IP Datagram): The UDP datagram is encapsulated in an IP datagram with Alice's private IP and Bob's public IP
    4. Data Link Layer (Ethernet Frame): The IP datagram is encapsulated in an Ethernet frame with Alice's MAC address and her router's MAC address
- On the Road NAT + Routing
    1. NAT at Alice's Router: Same as TCP example
    2. Routing over Internet: Same as TCP example
- Entering Bob's Domain - VPC + Security
    1. Same as TCP example
    2. Handling Datagram: Bob's server receives the UDP datagrams directly without reassembly, as each packet is independent
- Stream Delivery Back to Alice
    1. Continuous Stream: Bob's server continuously sends UDP datagrams containing video data back to Alice's device
        - It has no care if Alice receives every packet, or if they are in order - it just flings the packets over as fast as possible
    2. No Acknowledgments: Alice's device does not send acknowledgments for received packets, allowing for faster delivery
    3. NAT at Alice's Router: The datagrams are translated back to Alice's private IP and forwarded to her device (same as TCP example)
- Alice's Experience
    1. Video Playback: Alice's video player receives the UDP datagrams and plays the video stream, potentially with some packet loss or out-of-order packets, which may result in minor glitches or quality degradation


### HTTPS
HTTPS (Hypertext Transfer Protocol Secure) is an extension of HTTP that uses encryption to secure data transmitted between a client and server. It employs Transport Layer Security (TLS) to encrypt the communication, ensuring confidentiality, integrity, and authenticity of the data exchanged. HTTPS is widely used for secure web browsing, online transactions, and sensitive data exchange

- Encryption: HTTPS uses TLS to encrypt data, preventing eavesdropping and tampering
    - Encrypts the data being sent so that if anyone intercepts it, they can't read it
- Authentication: TLS provides server authentication, ensuring the client is communicating with the intended server
    - Proves that Bob is Bob, and that he setup the server Alice is requesting data from
    - Mitigates Man-in-the-Middle (MITM) attacks where someone "pretends" to be Bob
- Data Integrity: TLS ensures that data is not altered during transmission

#### Authentication Flow
1. Your browser requests the site's SSL certificate containing it's public key and identity
2. The TLS handshake happens where the website sends it's signed SSL certificate to your browser
    - Browser must verify it matches the domain you're trying to reach
3. Your browser verifies the certificate against trusted Certificate Authorities (CAs)
    - If valid, it proceeds; if not, it warns you about potential security risks
4. Your browser uses the public key to encrypt a symmetric session key, which is sent back to the server
    - This encrypted exchange of symettric keys uses TLS to enable secure transmission of data going forward

Essentially HTTPS builds on top of HTTP by adding a layer of security through encryption and authentication, making it suitable for sensitive communications over the internet. TLS enables authenticated and encrypted connections, ensuring data integrity and confidentiality between clients and servers, and SSL certificates provide the authentication mechanism to verify server identities

## Example - Video Streaming HLS
Video streaming actually often uses TCP along with sending out chunks of videos utilizing HTTP Live Streaming (HLS) or similar protocols

This framework will also use Adaptive Bitrate Streaming, so that if your network is experiencing difficulties it sends a lower bit file for a period of time until the network "catches back up" - this is what allows you to request high-def Youtube Video's, or change the playback quality

There's a system architecture review for [Youtube Video Playback](/docs/design_systems/youtube/index.md) that discusses uploading of files, chunking and indexing them to new bitrates, and serving via load balanced applications utilizing TCP HLS