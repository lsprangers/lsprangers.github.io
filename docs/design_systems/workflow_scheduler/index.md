---
layout: technical
title: Workflow Scheduler
category: Design Systems
difficulty: Advanced
description: Complete Workflow Scheduler Design
show_back_link: true
---

# Workflow Scheduler
A workflow scheduler will handle all scheduling, context checking, and historization of job runs. It's a further extension of Airflow which simply starts jobs based on Cron Schedules, where a scheduler must also check on execution environment state, downstream dependencies (also done by Airflow), and other services like retries and notifications. Truthfully, a lot of this can be a wrapper on top of a service like Airflow, because cron scheduling, historization, and upstream DAG checking is all completed by Airflow without us having to re-write it

## Problem Description
This problem is further focused on ML workflow scheduling, but realistically there's no difference from a "model retraining job" and "batch ETL"

- **Requirements**:
    - 1M scheduled jobs/day
    - Jobs may run from seconds to hours
    - Eventual consistency acceptable
    - Jobs must not be “lost”
    - System should survive worker/node failures
- **Support**:
    - retries
    - priorities
    - dependencies (DAGs)
    - recurring schedules
    - cron/recurring jobs
    - priority queues
    - DAG dependencies
    - retries
    - leases/heartbeats for worker failure
    - durable job state    
- **Uses**:
    - nightly feature generation
    - embedding backfills
    - model retraining jobs
    - Spark / Ray / containerized workloads
- **Assume**:
    - Workers already exist and can run Spark/Ray/container jobs.
    - Scheduler decides what should run, when, and where to enqueue it.
    - Job execution details are abstracted behind a worker API.


## High Level
The scheduler should be the control plane. Workers should be relatively dumb:
- claim job
- execute job
- heartbeat while running
- report success/failure

### High Level Numbers / Restatement:
- 1M jobs per day can be handled by a single node, and to ensure some sort of availability and fault tolerance we can ensure all job schedules, job runs, and state are written to a database. 
  - The key design of which database depends on historization and logging, and in most cases we want to keep a history so we need to keep all state stored for 3-6 months, which means 6 months * 30 days * 1M jobs = 180,000,000 job run records over 6 months. With the correct database instance with memory this could truly be handled by a single node application writing to a single node disk
- Job schedules, DAGs, requirements, and other attributes should also be stored, and these may be on the order of thousands to tens of thousands 
  - These are the main focus of the application - how to prioritize jobs to run, how to check if the environment is ready for them, and tracking downstream dependencies / state.
  - Some things to think about are 
    - Required infra metrics - are there currently enough IP's / nodes to support a jobs workload? This means we need to have a way to call on current infra metrics / monitors
    - DAGs - how to store dependencies, ID's, and ensure these can be updated and worked through? If there is a high priority jobX that's a downstream dependency of jobY that's also planned to run that night, how to schedule those?
    - Retries and control planes - ensuring jobs are done before scheduling their downstream counterparts, acting as a highly available heartbeat service for josb to report back to 
      - Being a control plane means we need to have higher availability than mentioned above, and so at this point we'd mostly wnt multiple scheduler workers with a single node database still
      - If we need to store metrics from heartbeats, we may change our database. This comes from converation

Overall, we are looking to store all job information, state, and requirements in a local database, or databases, which can most likely handle the scale of history and job information for fault tolerance. There will be 2 main splits of the scheduler which are prioritizing / scheduling jobs, and acting as a control plane for running jobs - we'll recommend to split these into 2 concrete API's / services, because only the job scheduler needs access to state, the control plane workers really just need to liaison with workers and then report back to scheduler

### Core Services / Infra:
- Scheduler
- Control Plane
- Highly available relational databsae (Postgres) or something with some large enough memory behind it

- Control Plane:
  - API's `startJob()`, `pingWorker()`, `endJob()`, `getState()`
    - These are called by scheduler / itself 
  - The control plane is typically called by the scheduler to start a job, with a certain input size, and a number of nodes to utilize. It interacts with some service to start nodes, virtualize enviornments, etc and we are considering that all solved. The control plane can essentially be told to "start JobX with 8 workers in VPC1, with a heartbeat of 1 minute", which will start the job and track heartbeats from the monitor. If the heartbeats ever fail outside of some interval, the control plane reports back to scheduler the job failed 
  - Furthermore, the control plane can be told to end a job, it can ask the current state which returns runtime total information, and can be explicitly told to ping a worker. All of this is just information held in disk on each node as a BTree or some disk based structure, and so if these nodes fail a new node can be stood up and continue the work baed on disk access 
    - We are saying to use a production grade disk based DB like RocksDB instead of a whole new control plane DB as we only need to store ephemeral information about jobs during their running, and then once a job finishes we return the sum information back to the scheduler and can delete it from local memory

- Scheduler 
  - Scheduler is broken up into multiple workers / replicas, and has a single Postgres database for storing all of the job requirements, DAG information, etc 
  - The scheduler needs some sort of priority queue of work to take on and schedule, and there are 2 main options here:
    - Hold a priority queue in a table in Postgres utilizing ordered table structures / indexes 
    - Use another service that the scheduler interacts with to prioritize calls
    - Essentially, there should be background processes on the scheduler to check what new items need to be scheduled that haven't been scheduled based on recurring jobs, or if the scheduler receives an ad-hoc "run Job X at time Y" it can post this to the priority queue / insert into table 
  - The scheduler is then responsible for draining this priority queue as each job's time comes. Priority is based on time to complete, and so jobs at the front need to run sooner than any job behind it.
    - We could schedule things by expected completion time, but there isn't clear information. At this time if there's a job scheduled at t that takes 1 minute and a job at t + 1 that takes 2 hours, we will wait to schedule the first t before finding t + 1, we can cover smarter scheduling later 
  - For each new job it receives, it needs to check on that job's requirements and DAG to ensure all upstream jobs are completed. Comlpetion of these jobs should be made clear on what timeframe it needs to have run on before this job can start - if an upstream node only has had to complete in the last month for this job to run, or if it has to have ran in the last minute, that needs to be made clear. 
    - We can query our historic database of job runs to check when each upstream job was last completed, and if all requirements are set we remove it from the queue, schedule it to the control plane, and once acked by control plane we ack the queue 
    - On job failure, we simply place the job back into the priority queue based on some retry information such as immediate, non-immediate, etc information and timelines submitted in job information 
  - If a job is set to schedule, but the infra currently isn't available for it (not enough IP's), or upstream jobs are still running, we either notify the stakeholder as a failure or we place it back into queue as a retry based on job submittal information. The action taken must be specified by stakeholder 

Postgres tables:
- Job 
  - jobId
  - dagId 
  - isCron
  - cronSchedule
  - heartbeatInterval
  - isRetry
  - retryInterval
  - stakeholderEmail
  - isPoll
  - Indexes:
    - jobId
    - 
- DAG
  - dagId
  - nodeDependencies [jobId -> jobId]
- JobHistory
  - jobSequence (monotonic increasing ID)
  - historyId [jobId + jobSequence]
  - dateTimeStart
  - dateTimeEnd
  - state
- JobFuture
  - jobId
  - toStart
  - Indexes:
    - BTree Index on toStart 

Typical Flow:
- JobFuture table is our priotity queue, it's indexed by toStart so we can always see next relevant job quickly 
  - This is saturated by a background task looping over job futures and last ran 
- Scheduler brings jobs from JobFuture into local priority queue, and once time reaches latest it pops it, ensures requireemnts, and calls Control Plane `runJob()`, places a new row in JobHistory, and then continues on
  - If job requirements fail, places back into JobFuture if `isRetry` based on interval, or simlpy emails stakeholder
- Control plane worker starts the job, and will continuously poll the job if `isPoll` based on heartbeat, otherwise it will wait for job to send it a ping 
  - If heartbeat ever out of sync or lost, ping worker, if no reply then tell Scheduler Job failed


## Implementation Details / Follow Ups

### SQL Tables
***Job Table*** - this just needs to store the actual job definitions and cron schedules

This table is updated by workflow submissions, and carries out the job metadata, upstream dependencies, job tags, etc
```sql
CREATE TABLE Job (
    job_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    cron_expr TEXT NOT NULL, -- e.g. '0 5 * * *'
    is_active BOOLEAN DEFAULT TRUE,
    last_scheduled_at TIMESTAMP, -- last time this job was scheduled
    -- other job metadata
);

CREATE INDEX idx_job_active ON Job (is_active);
```

***JobFuture Table*** is essentially acting as a priority queue, We are choosing to avoid a `dispatched` status, and instead use transactional outbox pattern. This job is created via a background process described in [saturating `JobFuture` table](#saturating-jobfuture)

```sql
CREATE TABLE JobFuture (
    job_future_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL REFERENCES Job(job_id),
    to_start TIMESTAMP NOT NULL, -- when to run
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, done, failed
    -- other fields as needed
);

CREATE INDEX idx_jobfuture_to_start ON JobFuture (to_start, status);
```

Lastly we use the [table polling transactional outbox pattern](/docs/architecture_components/messaging/index.md#transactional-outbox) so that anytime a job is popped from `JobFuture` for processing, and the transaction there commits, we can be absolutely sure it's sent to a downstream job to start before being considered "dispatched"

```sql
CREATE TABLE Outbox (
    outbox_id SERIAL PRIMARY KEY,
    job_future_id INT NOT NULL REFERENCES JobFuture(job_future_id),
    payload JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_outbox_processed ON Outbox (processed, created_at);
```

### Evaluating Cron Expressions
Polling the `Job` table and checking Cron Expressions is an $O(N)$ operation - you loop through everything and see if it's ready to go. There's a potentially better alternative where on each initial job submission you post the first `JobFuture` into the priority queue with whatever the next cron schedule would be, and then during popping from `JobFuture` you re-query the `Job` table to place the next schedule, but this means that we only have 1 instance of a job at any time in `JobFuture`. If there's ever a job that needs to run every minute or something similar, we might want to place multiple `JobFuture` into it, and in that scenario, during each `JobFuture` expression, we'd need to query the last sent `JobFuture` for that job and then evaluate the next cron expression afterwards

Altogether, the difference is "do I query the entire Job table wiht a background process" or "lazily push the next schedule during the popping of each current job in `JobFuture`"

### Saturating JobFuture
Using a [BTree](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE/index.md) as a [priority queue](/docs/dsa/5.%20heap%20&%20priority%20queue/index.md) can be entirely done via a relational database for ***low to moderate data volume*** systems where we desire strong durability and potential guarantees on transaction semantics using an [tranasction outbox](/docs/architecture_components/messaging/index.md#transactional-outbox) 

Once there are jobs pulled from `Job` table with their cron expressions materialized, we push them into the `JobFuture` table, which is indexed by `to_start, status` ensuring that the latest job `to_start` is available to quickly query. Insertion is $O(\log M)$, where $M$ is the number of jobs stored in it, since we need to update the BTree index, but that allows for querying and popping of the next job to also be $O(\log M)$

```sql
-- Insert due jobs into JobFuture (idempotent insert)
INSERT INTO JobFuture (job_id, to_start)
SELECT :job_id, :to_start
WHERE NOT EXISTS (
  SELECT 1 FROM JobFuture WHERE job_id = :job_id AND to_start = :to_start
);
```

### Saturating Outbox
Polling the `JobFuture` table to find a job is $O(\log M + K)$ where $K$ is the number of jobs to run. The job polling the `JobFuture` table and pushing into the outbox can be the [message relay](#message-relay) service below - that's completely fine

```sql
SELECT * 
FROM JobFuture
WHERE to_start <= NOW() + INTERVAL 'X minutes'
FOR UPDATE SKIP LOCKED
ORDER BY to_start 
LIMIT K;
```

When a job is pulled from `JobFuture`, a transaction is started on that `job_id`, and in that same transcation we move the job into the `Outbox` table - the actual movement should be $O(\log M)$ to pop from `JobFuture`, and $O(1)$ to push into the `Outbox` table

```sql
-- Atomically move job from JobFuture to Outbox
WITH next_job AS (
  DELETE FROM JobFuture
  WHERE job_future_id = (
    SELECT job_future_id FROM JobFuture
    WHERE status = 'pending'
    AND to_start <= NOW()
    ORDER BY to_start
    FOR UPDATE SKIP LOCKED
    LIMIT 1
  )
  RETURNING job_future_id, job_id, to_start
)
INSERT INTO Outbox (job_future_id, payload)
SELECT job_future_id, jsonb_build_object('job_id', job_id, 'to_start', to_start)
FROM next_job;
```

### Message Relay
A message relay service needs to poll the `JobFuture` table / utbox / both, etc and select unprocessed `Outbox` messages and send them to the actual control plane workers to start. We don't need a queue or anything inbetween, because if something fails or isn't acked we just have the message relay wait!

### Transaction Flow
- Cron Poller
    - Begin transaction
    - For each job that should run in the next window, insert a row into `JobFuture`
    - Update `last_scheduled_at` column in `Job` table
    - Commit
- `JobFuture` to `Outbox` 
    - Begin transaction
    - Pop the next pending job from `JobFuture` (skipping locked)
        - Set the status to `running`
    - Insert a message into `Outbox`
    - Commit
- Message Relay
    - Get
        - Begin a transaction
        - Select unprocessed `Outbox` messages (skipping locked)
        - Mark as being processed
        - Commit
    - Send
        - Send the message to the external service
        - After delivery, mark the messages as processed in a new transaction
        - ***This is where a Send Transaction can fail, and we need a background job that would clean up outbox and potentially resend the message*** - this is exactly where this architecture turns into "at least once" semantics for job deployment

## Further Optimizations
There are even more things we can do to pump up Postgres throughput and latency

### Indexing On Ready and Batching
Creating a further index on only the `status = ready` rows, and potentially in the future partitioning by time would allow a better set of these rows to be read on each call, and batching allows us to in bulk process and remove rows from `JobFuture`

```sql
CREATE INDEX job_future_ready_idx
ON job_future (run_at, priority, id)
WHERE state = 'ready';

WITH claimed AS (
  SELECT id
  FROM job_future
  WHERE state = 'ready'
    AND run_at <= now()
  ORDER BY run_at, priority, id
  LIMIT 100
  FOR UPDATE SKIP LOCKED
),
updated AS (
  UPDATE job_future jf
  SET state = 'dispatched',
      lease_expires_at = now() + interval '30 seconds'
  FROM claimed
  WHERE jf.id = claimed.id
  RETURNING jf.id, jf.job_id, jf.run_at
)
INSERT INTO outbox (job_future_id, payload)
SELECT id, jsonb_build_object('job_id', job_id, 'run_at', run_at)
FROM updated;
```

The above design removes a number of jobs from `JobFuture` and batches together workloads into `Outbox` in a single transaction

### Redis Priority Queue
In the above requirements we have strong durability and eventual consistency, so Postgres is still the right answer IMO, but if we needed to get into a "higher performance" priority queue then [Redis ZSets](/docs/architecture_components/databases%20&%20storage/Redis/ZSETS.md#min-heap) can be used to create a Min Heap style data structure, and utilizing Lua Claims helps on the outbox pattern semantics 