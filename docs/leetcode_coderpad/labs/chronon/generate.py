# python3 generate.py \
#   | docker exec -i fs-kafka /opt/kafka/bin/kafka-console-producer.sh \
#       --bootstrap-server localhost:9092 \
#       --topic purchases \
#       --property parse.key=true \
#       --property key.separator="|"

import json
import random
import time
import uuid

random.seed(42)

for _ in range(20):
    user_id = f"user_{random.randint(1, 5)}"
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": "purchase",
        "user_id": user_id,
        "event_time_ms": int(time.time() * 1000),
        "amount_cents": random.randint(500, 20000),
        "currency": "USD",
        "schema_version": 1,
    }
    print(user_id + "|" + json.dumps(event), flush=True)
    time.sleep(0.2)