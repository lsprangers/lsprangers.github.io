import asyncio
import aiohttp
import numpy as np
import tritonclient.http as httpclient
import time
from transformers import BartTokenizer
import json
from pathlib import Path
from typing import Optional, List

TRITON_URL = "localhost:8000"  # Triton HTTP endpoint
MODEL_NAME = "bart-large"


class BartModelInference:
    def __init__(self, model_name: str = "facebook/bart-large", model_dir: Optional[Path] = None)
tokenizer = BartTokenizer.from_pretrained()
texts = ["Example input 1", "Example input 2", ...]  # Your batch of texts

inputs = tokenizer(texts, padding="max_length", max_length=32, truncation=True, return_tensors="np")
data = {
    "input_ids": inputs["input_ids"].tolist(),
    "attention_mask": inputs["attention_mask"].tolist()
}
with open("tokenized_inputs.json", "w") as f:
    json.dump(data, f)
    
# Example input preparation (adjust as needed for your tokenizer/model)
def prepare_input(texts):
    # This is a placeholder. In practice, use the tokenizer for BART-large
    # and convert to numpy arrays as Triton expects.
    # Example: input_ids = tokenizer(texts, return_tensors="np").input_ids
    # For demo, just use dummy data:
    batch_size = len(texts)
    max_length = 32
    input_ids = np.random.randint(0, 50265, (batch_size, max_length), dtype=np.int32)
    attention_mask = np.ones((batch_size, max_length), dtype=np.int32)
    return input_ids, attention_mask

async def infer_single(client, text):
    input_ids, attention_mask = prepare_input([text])
    inputs = [
        httpclient.InferInput("input_ids", input_ids.shape, "INT32"),
        httpclient.InferInput("attention_mask", attention_mask.shape, "INT32")
    ]
    inputs[0].set_data_from_numpy(input_ids)
    inputs[1].set_data_from_numpy(attention_mask)
    outputs = [httpclient.InferRequestedOutput("output_ids")]
    response = await asyncio.get_event_loop().run_in_executor(
        None, lambda: client.infer(MODEL_NAME, inputs=inputs, outputs=outputs)
    )
    return response.as_numpy("output_ids")

async def main():
    client = httpclient.InferenceServerClient(url=TRITON_URL)
    texts = [f"Example input {i}" for i in range(100)]  # Simulate 100 requests
    start = time.time()
    results = await asyncio.gather(*[infer_single(client, t) for t in texts])
    print(f"Completed {len(results)} requests in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
