---
title: Multi Tenant SaaS Applications
layout: default
---

## Multi Tenant
I thought this deserved an entire section as it uses + covers specific implementations of:
- [Architecture Components](/docs/architecture_components/index.md)
- [Data Structures & Algos](/docs/dsa/index.md)
- [Event Driven Architecture](/docs/event_driven_architecture/index.md)
- Some processing frameworks
    - [Spark (Distributed OLAP + Stream)](/docs/other_concepts/SPARK.md)


And many many other things to create SaaS applications for thousands of customers - most of the major cloud providers are built around creating these sorts of applications

The "old way" of doing things, known as managed service / software providers, was to provide binaries, containers, and altogether "installable" software to companies IT teams, and they would setup an environment and then configure and run the software - some modern companies still do this for large scale data processing frameworks that may not make sense to expose as an API

Management, monitoring, debugging, and upgrades of this software fell on client companies IT team, and the providing company continued to push out new functionality with `X.Y` major and minor version releases. This had pros and cons, but it was never "quick" - customers managed their solution, enabled create one-off customizations, versions per customer, etc to sell all of this software, and ultimately it causes strain on everyone when corners are inevitably cut

Cloud companies and infrastructure also changed things, as it allowed software companies to fully host, manage, sell, and scale their software for each client in a pay-as-you-go fashion versus the rigid "old way"

In the "new way" software companies will host small services, ***microservices***, of their software which they will manage, operate, deploy, and expose to their clients via API's over *shared infrastructure*. The shared infrastructure piece can be a logical, physical, or mix model - if we do actually store all data on the same physical machine but we "logically separate" it, then things are logically separated!

Pretty much every aspect of software business is made more manageable with this setup, except that the software company now has more responsibilities, but they can track usage per tenant, deploy fixes, sunset versions, etc. With this new model adding new tenants to a service also naturally fit in to dynamic scaling of cloud resources, and so software companies would scale out their applications by paying more to cloud companies, and in return they would get profit from their new tenants - in this they wouldn't need to vertically scale any of their current compute, but just add more nodes for each new tenant

Doing this right is incredibly hard, and if you do it incorrect you fail even faster versus shipping things then "old way" where your software is a bit more stuck in the clients environment

There are a number of classic SaaS components, and each is just as important as the actual business logic

Like most things in software, it's an interconnected catch-22, if you do the side components wrong, your business application won't scale, and if you do the business application scaling wrong, your side components won't matter

![SaaS Components](/img/saas_components.png)

Defining ***multi-tenant*** is also quite hard, and vague, with many definitions that are appropriate and acceptable. The main focus of being multi-tenant is that multiple customers, tenants, share some underlying infrastructure such as a database or compute node

There may be some services and infrastructure that's shared, and some that are physically isolated - whether it's the service compute, database, or a mixture of both or neither, the infrastructure and application logic are tied together but do exist in separate layers

![Physical And Logical SaaS Components Example](/img/physical_logical_saas_components_example.png)

There are some ***fully dedicated*** models where every single tenant has isolated resources and services, and at this point the software company is acting more as software management and DevOps to ensure each customer has the correct physically isolated environment

![Physical Fully Dedicated Example](/img/physical_fully_separated_saas_example.png)

So multi-tenancy doesn't imply shared resources specifically, it could be fully dedicated environments as well. Therefore, the ***definition of multi-tenant is any environment that onboards, deploys, manages, and operates tenants through a single, unified experience***

At the end of the day, SaaS is actually a business model AND a software model, but one can't appropriately exist without the other

## Architecture Fundamentals
Main point of this section is to outline how tenancy plays a role in the 3 main layers:
- Application
- Infrastructure
- Data

Alongside that, how to group and organize the different elements of a multi-tenant architecture to focus on the fundamental services and layers:
- Core Business Logic
    - Applications
    - Proprietary algorithms
    - etc
- Horizontal Services
    - Authentication
    - Authorization
    - Security
    - Onboarding
    - Profile and User Management
    - Integration
    - Deployment and Versioning
    - etc....

There's no good list as some of the above things even overlap with eachother, take profile and user management - it's basically a specific implementation and abstraction of the combination of security and onboarding (to some degree)

The "old way" of managed services deployed in client IT environments means there's an underlying assumption that it's installed, ran, and managed by each customer and they are responsible for all of the horizontal items above

You simply provide them the core business logic!

## Application Versus Control Plane
The first major split in architecture is the ***Application Plane***, which will host our core business logic and tenant provisioning, and the ***Control Plane*** which manages administration, high availability, onboarding, billing, etc!

![Application Plane vs Control Plane](/img/saas_app_vs_control_plane.png)

The typical thought is that the control plane is the pane of glass used to orchestrate and operate all of the moving parts of the SaaS solution. It helps to act as the multi-armed octopus provisioning the shared infrastructure the tenants will be using. *This control plane is separate from a Kubernetes Control Plane which enables the Compute and Data Planes to be highly available*

Control plane applications are meant to be more administrative, whereas the application plane is meant to have actual microservices and business logic in them that has decoupled state from the admin panel, and the admin control panel can update that state if needed. The book states that the control plane isn't actually multi-tenant, and it's only supposed to provide surrounding services for the tenant to utilize the core business logic services, but I think that distinction is right and wrong. Take billing for example, it will have certain state dedicated to a specific client, and only that client should access the billing state they own, and so the billing service itself has multiple tenant state inside of it even though it's not apart of the core business logic

The application plane is where features, functionality, and business logic lives - it's where a majority of the multi-tenant architecture and logic lives

Altogether, the application plane is our business logic and infrastructure that's shared between tenants, and the control plane manages and operates these tenant environments through a unified experience

### Control Plane
The control plane has an extensive ad far reaching set of components, and can be thought of as anything "not core business logic" at the end of the day

The below components are the ones most commonly used

#### Onboarding
Getting a new tenant introduced, integrated, and setup on a new SaaS product is an entire workflow and service in it of itself

![SaaS Onboarding Flow](/img/saas_onboarding_flow.png)

The onboarding flow typically consists of a generic UI new tenants can sign up on, and that will trigger some workflow to create an identity for that tenant, which ultimately will be used as the identifier and "section" of the application plane

The identifier, identifier footprint (multiple ID's), profiles, users, billing codes, etc are all created in this onboarding step, and are required for all future flows especially in authentication + authorization

The onboarding flow also ensures the shared infrastructure is ready for new clients, creates any partitions or zones that are needed, and gets everything prepped

#### Identity
Identity services are heavily tied to authentication and authorization - we want to know who is requesting information (authentication), and if they're allowed to do it (authorization). We can only do those two things if we have some notion of identity, and an understanding of our core groups of tenants and their users / groups

Typically there's a `Many User : 1 Tenant` cardinality in B2B, and a `1 User : 1 Tenant` in B2C

This brings up issues around federated identities, hierarchical identites, RBAC, and many other areas - these directly affect our application code, because if you try to run some logic for a tenant you need a `select * from table where tenant_id = XYZ`, and that may return one, many, or none!

#### Metrics
We need some sort of monitoring and observability to understand how our tenants are using our system, and how our system's performance is doing - if it's taking 2 days to load a page, that's bad and we'll lose customers, but if one specific customer is hitting an API 1,000 GET per second they may be ruining things for everyone else

If at certain times, like 9-5 during business days, the system experiences double or triple the typical load when users are active we would need to scale, and potentially we'd need to scale certain portions of the system for specific clients - metrics help us understand all of this, and can even help automate this process as a dynamic scaling solution

Metrics are also useful to paint a picture of the business, user flow, service usage, and billing / customer success per tenant

Adding in metric instrumentation means adding in proper API calls, log file calls, etc so it means we must alter application, infrastructure, and data layers to process these metrics and make them visible

Ultimately, there's a desire to understand the system to ensure clients are happy and being fulfilled, and alongside that understanding usage for billing purposes is always helpful

#### Billing
Billing providers, accepting payment, ensuring clearing, and assigning usage to customers is all apart of billing

Customer usage can come from a mixture of [Metrics](#metrics) and [Identity](#identity) that we then assign certain credit usage to ultimately bill, and this is a common setup in most SaaS architectures

A common definition is ***metering*** which will measure tenant activity and usage to generate a bill later on - some common examples are:
- Bandwidth consumption
- Compute usage
- Number of requests
- etc...

Or a combination of all of these can also be used with thresholds, consumption minimums, etc

#### Tenant Management
Every tenant needs to be centrally managed and configured - this is typically represented as the tenant management service, which again, is a combination of a number of these services with some extra logic on top

The core functionality of tenant management is just to create and manage the state of tenants / users including:
- Unique ID's
- Billing plans
- Security policies
- Identity configuration
- Status
- etc...

Some SaaS architectures bundle this into [Identity](#identity), but this means that Identity manages authentication, authorization, tenant management, etc which is not necessarily a good split - there are configurations to manage outside of [Identity](#identity)

### Application Plane
How and where multi-tenancy shows up in the application plane is much more abstract, and can vary significantly based on a wide range of factors and environment

The deployment tooling, tech stack, and organization structure are some of the largest pieces that affect multi-tenancy in the application plane

There are times where you can build everything to handle all aspects, or where you can use 3rd party SDK's like [Launch Darkly](https://launchdarkly.com/) for feature flags, [Heap / Mixpanel](https://mixpanel.com/compare/heap/) for user click data, and other pieces for other portions. These ultimately help you to do things in the application plane, in the control plane, and inbetween the two

#### Tenant Context
The application plane is always functioning in the context of specific tenants, and this context is typically represented as a token or some other construct that packages all of the attributes of your tenant

The most common example / usage is JSON Web Tokens (JWT's) which combine tenant information into one construct that's shared across all moving parts of the multi-tenant architecture. JWT's are used to authenticate and authorize all tenant information (context) across services without having an explicit service or code that relies on the context. This ***JWT is therefore known and referred to as tenant context***

Tenant context has a direct influence on the design of your application architecture and how it processes requests, which also affects both your infrastructure and data layers - the processing of tenant context affects routing, logging, metrics, data access, and many other pieces

![Tenant Context SaaS Example](/img/tenant_context_saas_example.png)

Tenants authenticate against [Identity](#identity) that was created during [Onboarding](#onboarding) to acquire their tenant context (JWT), this context is innjected into a service of the application (during initial request), and flows into each downstream interaction of the system which allows each service to acquire and aplpy that context across use cases to ensure they pull only that clients information, and treat this request in terms of that client. These interactions will generate [Metrics](#metrics) based on the clients usage which we will want to [Bill](#billing)

Each service will need to use this tenant context, and each service should be designed knowing this. Packaging up this context in ways that limit complexity while promoting agility is a continuous balancing act for architects and developers

#### Tenant Isolation
Multi-tenancy focuses squarely on placing customers and their resources into environments where resources may be shared or at least placed side by side in common infra environments

This means multi-tenancy must ensure tenant resources are protected against any potential cross-tenant access whether it's from logical isolation, physical isolation, or something in the middle

- Logical isolation is the idea of storing tenant resources and data into the same infrastructure, but separating it into buckets per tenant that may have different access policies and configurations
- Physical isolation is storing tenant resources and data on completely separated physical environments
- Something in the middle may be something like Blob Storage where a bucket may represent one logical unit, but each directory underneath is can be forced to reside on completely separate physical block devices and servers

Each of the layers and components may have certain aspects that are separated logically or physically - for example we may have tenants share compute resources without any isolation, but their backend databases have customer data physically isolated and metadata logically isolated

Physical isolation doesn't guarantee that tenant 1 cannot access tenant 2's data - if our security policies are too broad, there's nothing stopping a tenant on compute 1 from accessing other tenants data on a physically separated database. Physical isolation typically makes it easier, and removes any sort of "accident" from exposing data, but it's not an automatic guarantee

To prevent cross-tenant exposure, the application, infrastructure, and data planes must introduce constructs that prevent this access, and each layer must adhere to these restrictions with the same understanding

#### Data Partitioning
Services need to store data and state of tenants, and figuring out data storage solutions themselves for a service are hard enough between K:V stores, RDBMS, NoSQL, document storage, graph storage, disk based, etc...

Now after choosing these tools, we also need to ensure for some compliance, governance, usage patterns, and application reasons we partition data (either logically or physically!)

The design of different storage models and the choice of how to store data is known as *Data Partitioning*. Picking a strategy that partitions tenant data based on tenant profile of that data, which means it can be stored in dedicated constructs (physically isolated) or land in some shared construct (logically), which are even further compounded by the storage mechanism and data structures

#### Tenant Routing
Now that data is being stored in some way, and we have control plane services to create tenant context, we will need to route clients incoming requests appropriately! If the first two parts are done, this part is basically done, but all 3 are a venn diagram of overlapping components

If our data is physically isolated, and a client is routed to machine 1 to process some data, and that machine goes down and the subsequent request is sent to machine 2, is that a proper application routing mechanism? Is there some local state on machine 1 in RAM that is now lost? Is each request stateless, or stateeful? etc...

The actual routing mechanisms to each VM in a cluster, how each VM routes to databases, leaders vs replicas, consistency, etc are all part of our routing logic and it may have serious consequences for our business

This happens in load balancers, service meshes, DNS routing, databases (leaders vs replicas), caches, and many other components in a horizontally scaled distributed system

If we are using cookies to track users carts, and our cart metadata is stored in RAM in a machine, every single subsequent request must be sent to that machine to ensure cart is tracked otherwise the user will have an incomplete experience

![Tenant Routing SaaS Example](/img/tenant_routing_saas_example.png)

#### Multi Tenant Deployments
Every application requires some DevOps technology and tooling that can deploy versions, do weighted routing, complete rollbacks, and apply policies 

Different flavors of the tenant application plane model will add new considerations though - tenants may have a mix of dedicated and shared resources, so understanding which ones to re-deploy, which ones need to be highly available, and where to apply policies and routing will all influence the DevOps implementation of app deployments

Some deployments even need to consult other services to determine which client dedicated services need updates, upgrades, or maintenance - so some services may be deployed multiple times based on certain criteria, and potentially even inject client context and state into new deployments

Technically this isn't apart of the application plane, it's apart of the infrastructure plane, but ***wiping your hands and ignoring this will directly impact the success of your application and agility***

### Gray Area
Control and application planes cover most of the fundamental multi-tenant architecture constructs, but still some concepts don't fit perfectly or cleanly into either of these planes

#### Tiering
Tiers are used to create different variations of an offering with separate price points such as basic, advanced, and premium

Basic tenants may have constraints on performance, number of users, throughput, etc whereas premium tenants have higher thresholds, and better ***service level agreements (SLA's)***

Tiering actually has a fairly large impact on building out a multi-tenant architecture, as ensuring policies and application / infra layers are ready to support this tiering without changing much code is difficult - some applications even create tiering services inside of their control plane that live as first class concepts

Given that tiering is apart of onboarding, context, billing, application routing, etc it's really apart of both control and application plane layers

The general thought pattern is to leave it in the control plane though, as it can engage with identity and authorization services and embed it's state in context (JWT) which is passed through to the application plane - the gray area comes from the application plane needing to react to this context, and any change in tiering strategy would require changes to the application plane

#### Administration
Users can be a lot of things, and just like AWS there may be roles, service principals, users, and generic private keys that can all be assumed to perform some action, and so identity and administration are difficult to pin down

***Tenant administration*** itself refers to altering configurations, identity, and other items using some UI or CLI via admin privileges - they can usually alter the configurations for control plane services, and configure, manage, and maintain application level constructs and how the SaaS application is used

Tenant users then use the SaaS application the admin has setup and configured

***System administration*** means developers on the SaaS business side who *have access to the control plane* to manage, operate, and analyze the health and activity of SaaS environments. Generally, it's taboo to allow system administrators access to client data, and the better setup is to have metrics and appropriate logging so that system administrators can debug issues without accessing sensitive data

Having a repeatable, auditable, and secure mechanism for system administrators to access control plane, and potentially application plane, resources is apart of building multi-tenant architecture, so it's a gray area...most architectures keep administration services in the control plane, but some argue that management of users happens in the context of the application and client so it should live in the application plane

#### Tenant Provisioning
So should tenant provisioning live within the control plane or the application plane

The large tradeoff revolves around encapsulation and abstraction - if you believe the structure and footprint of application infrastructure should be unknown to the control plane, then you favor tenant provisioning and administration to be in the application plane and setup by the client, but if you want to make things more "rigid" and coupled with the control plane then you would favor keeping provisioning in the control plane

The other tradeoffs come with tenant expectations, strategy and business logic changes, etc - you don't want to continuously alter the control plane if the business logic to tiering or tenancy changes

### Integrating Application and Control Plane
There are multiple ways to partition application and control planes via networking, physical resources, policies, or some other setup

This doesn't mean code or deployments need to live separately, although that's another way to separate them (typically I disagree with this), because the same repo with separate CICD can still deploy these different instances

Integration may be "loose" with generic messages that are encoded, decoded, and handled per message, or it may be more strcit with pre-defined native integrations and patterns - usually the looser message based setup means you're not defining things properly, and you don't have the agility to update these things as they change with the business, so you take on tech debt to utilize "messages" which make changes easier, but you have to crawl through code to debug and make updates 