---
layout: technical
title: Queue
category: Architecture Components
difficulty: Advanced
description: Discussion around Queue's
---

## Queues
Queue's are generally used to ensure some sort of buffer between producers and consumers. They can be thought of as a place to keep messages between the two groups so that there's not overload or connectivity issues between the two sets

They also, generally, provide durability, single point connectivity, scaling, and other useful traits like priorities, acknowledgements, and retries

Queue's are useful when you have producers and consumers that have different workloads, where you might want to scale the consumers to comply with new messages coming in from producers - the most typical example I see is an API fielding requests and sending messages to workers to run complicated ML pipelines and models

![Queue, PubSub, and Kafka](/img/queue_pubsub_kafka_flowchart_freehand.png)

Example:
- Message comes in with JSON field holding a document, or an S3 URL that holds a large text based document
- API fields the request, checks priority, and sends to a queue
- To ensure timely response, consumer pool may scale to 2-3x the size of the producer pool since each request is light on producer and very heavy on consumer
    - Consumer may need to run multiple NLP pipelines such as Entity Extraction, Sentiment Analysis, and/or Categorization

## Queues In The Wild
Some examples below of queue's typically used "in the wild"

### SQS

### Redis

### RabbitMQ

### Celery
Celery is somewhere between a queue, a message broker, and a serializable function passer - ***Celery, IMO, is not actually a queue, but it's often described as one***

At it's core, Celery is probably best described as an Distributed Producer-Consumer Architecture SDK or something in that vein

Celery helps developers to write tightly coupled `producer.py` and `consumer.py` scripts, along with `celery.config` files, which allow producers to push to a backend message queue, typically Redis or RabbitMQ, which then gets pulled by consumers

Celery sits at the application plane, and it's "scaling" is done on Celery Workers which are tightly coupled to the compute / infra plane

***Celery cannot ask your infra plane to stand up more computes***, it can simply scale up more processes on each of those computes

![Celery Arch](./images/CelerySpecific.png)


#### Celery Structure
Celery has a few core components that make it work
- **Brokers** - The message queue that Celery uses to pass messages between producers and consumers - typically Redis or RabbitMQ
- **Producers** - The code that produces tasks and sends them to the broker
- **Consumers** - The code that consumes tasks from the broker
    - Consumers are the actual workers that process the tasks, and they typically run in separate processes or containers
    - You do not specifically create a `consumer.py` file, your producers call `tasks.add.delay()` and then eventually they will get a returned result
    - Therefore, our producers call a worker and then consume the output
- **Workers** - The processes (actual computes) that run the consumer code and execute the tasks
- **Tasks** - The functions that are executed by the workers (and passed between producers and consumers)

These components work together to create a distributed task queue system that allows for asynchronous task execution and scaling, BUT they are also tightly coupled in terms of repo setup, and code structure

In a typical setup, there are 3 main components

##### Tasks / App
- `tasks.py` - This file contains the Celery app configuration and the task definitions. Both producers and consumers will import this file to access the Celery app and tasks
    - This file is the "glue" that holds the producer and consumer code together, and so it tightly couples your sender (producer) and receiver (consumer)
    - A number of implementations will make this a proper separate package that both producer and consumer repos can import

The `Celery()` instance below is commonly referred to as the "Celery app"

```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

- After this, you're able to run Celery via `celery -A tasks worker --loglevel=INFO`
    - Form: `celery -A <module_name> <type> --loglevel=INFO`
    - A crap load of other CLI options for running as daemon, setting up worker pools, etc...

You can even have multiple Celery Apps and Brokers inside of a Project
```python
from celery import Celery

app1 = Celery('app1', broker='redis://localhost:6379/0')
app2 = Celery('app2', broker='amqp://guest@localhost//')

@app1.task
def task_a():
    pass

@app2.task
def task_b():
    pass
```

###### Calling The Task
Calling an actual task simply involves importing the module in `tasks.py` and running the `.delay()` method

In our `tasks` module, since there's a broker involved, what ends up happening is this task gets scheduled on our broker (queue), and the worker pool will pick it up for execution

```python
from tasks import add

result = add.delay(4, 4)
```

##### Results
The results backend stores state of tasks running

You can use Mongo, SQLAlchemy + DJango, Redis, or even use RPC to send things back to the broker to go back to the consumer / producer

From above, you can then call something like
```python
result.ready() # True or False
```

##### Configuration
From the Celery Docs: "The input must be connected to a broker, and the output can be optionally connected to a result backend."

Things are mostly this simple

Then it says "However, if you look closely at the back, there’s a lid revealing loads of sliders, dials, and buttons: this is the configuration."

Because Celery has a ton of stuff to tweak to make things actually run in parallel with proper CPU saturation - are your tasks I/O bound, or CPU bound? Are there certain datasets and volumes that need to be attached? How does everything interact with the backend results set? How are retries done?! Etc

In large scale use cases, there are entire configuration modules with routing + task definitions

`celeryconfig.py`

```python
broker_url = 'pyamqp://'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True

task_routes = {
    'tasks.add': 'low-priority',
}
task_annotations = {
    'tasks.add': {'rate_limit': '10/m'}
}
```

#### Examples

##### I/O Bound Task
Let's say you have a setup where you have an API request that comes in, like for a user registration, and the API needs to call a `handle()` function that:
- Creates a new user
- Creates their profile and setting configuration
- Queue's a welcome email in SQS
- And finally, after ensuring all of these are done, returns a response to the user

In this scenario, you can have a lightweight FastAPI in front that accepts new requests and calls a `task.handle()` function that does everything

The actual workers themselves would be I/O bound, and running on the Celery worker pool, so how does everything look?

```directory
src/
├── tasks.py
└── main.py
```

```python
# tasks.py
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def handle(user_id):
    async new_user(user_id)
    async new_profile(user_id)
    async new_settings(user_id)

@app.task
async def new_user(user_id):
    await call_database(user_id, CREATE_USER)

@app.task
async def new_profile(user_id):
    await call_database(user_id, CREATE_PROFILE)

@app.task
async def new_settings(user_id):
    await call_database(user_id, CREATE_SETTINGS)
```

```python
from tasks import handle

app = FastAPI()

@app.post("/create")
def create_add_task(user_id: int):
    result = handle.delay(user_id)
    return {"task_id": result.id}
```

From here, any API call to `/create` will enqueue a new task for processing the user creation workflow. The FastAPI application will immediately respond with the task ID, allowing the client to check the status of the task later if needed

Some people will do the following:
```python
@app.post("/create")
async def create_add_task(user_id: int):
    result = await handle.delay(user_id)
    return {"task_id": result.id}
```

Which will block until the task is finished and return the result directly to the client. This approach is generally not recommended for long-running tasks, as it defeats the purpose of using a task queue. Instead, it's better to return the task ID immediately and let the client poll for the result later.

`delay()` isn't an async function, and doesn't return an awaitable so you can't use `await` with it.

`AsyncResult.get()` is truly async call, and can be awaited - most documentation talks about not doing this because "task queue could take a long time to return a result, and you don't want to block your application while waiting for it."

While an event loop (like in FastAPI) can handle other requests while awaiting, the user’s request is still "pending" until the task is done. The main benefit of a task queue is to decouple the request/response cycle from the background work, allowing you to return immediately and let the client poll for the result

Therefore, if you're truly using Celery for I/O bound work you will most likely have to return `taskID` to the client and let them poll for the result.

```python
@app.post("/create")
async def create_add_task(user_id: int):
    result = handle.delay(user_id)
    return {"task_id": result.id}

@app.post("/result/{task_id}")
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    if result.ready():
        return {"status": "completed", "result": result.get()}
    else:
        return {"status": "pending"}
```

