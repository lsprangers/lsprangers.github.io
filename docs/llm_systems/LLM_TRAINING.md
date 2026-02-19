---
layout: technical
title: LLM Training
category: LLM Systems, Hardware, and Code
difficulty: Advanced
description: Discussions around NN's, Transformers, LLMs, and other topics
show_back_link: true
---

## LLM Training

Various training datasets are used, mostly around sourced web content from social media, online encyclopedias, and structured curated text
![LLM Training Dataset Sources](/img/llm_training_dataset_sources.png)

LLM pipelines still rely heavily on [tokenization models](/docs/transformer_and_llm/TRANSFORMERS.md#tokenization), [embeddings](/docs/transformer_and_llm/EMBEDDINGS.md), [attention mechanisms](/docs/transformer_and_llm/TRANSFORMERS.md#attention), encoder-decoder interactions (or encoder / decoder only), and some regularization, dropout, and residual layers to ensure models are trained appropriately. Outside of that model evaluation utilizing BLEU scores

![LLM Training Pipeline](/img/high_level_llm_training_pipeline.png)

## General Pipeline
Each of the architectures, encoder-decocer or only one or the other, have a fair amount of overlap given they all stem from [transformers](/docs/transformer_and_llm/TRANSFORMERS.md):
- (Pre)training steps are used to prep the models dataset, setup the model architecture, and decide on further layers and training tasks to ensure a model is able to achieve it's desired convergence. Afterwards, the actual training loop relies heavily on distributed compute, advanced hardware, and multiple evaluation rounds to check it's current convergence limits. Finally weights are stored, experiments logged, and the model is marked as a foundational ready model to run transfer learning on for any specific downstream task that's needed like classification, sentiment analysis, translation, etc
- (Pre)Training
    - Data preparation and sampling
    - Attention
    - Further layers
- Foundational Model
    - Training loop 
    - Evaluation
    - Storage
- Distribution
    - Model registries
    - Transfer learning

### Data Preparation And Sampling
Data preparation involves sourcing, storing, and cleaning input data which comprises of massive datasets from the web, and then sending that data through initial model architectures so that it can be used by a transformer architecture

Datasets first need to be [tokenized](/docs/transformer_and_llm/TRANSFORMERS.md#tokenization), which is essentially a compaction and extension process that allows the input dataset to be refined as a set of tokens that cover the entire span of potential future vocabulary. The general thought is, instead of creating embeddings for both `rocking`, `rock`, `rocket`, `sock`, `socket`, and `socking`, we might as well reuse a number of these sub-words as tokens instead. Some architectures use character-level tokens, but that means we only really have ~100 static embeddings, and it's difficult to glean any actual information about what these characters represent. Most modern day models utilize sub-word embeddings, and these are based on frequency counts and compaction procedures which are a sort of greedy algorithm. It is described further in the [transformer subdocument](/docs/transformer_and_llm/TRANSFORMERS.md#tokenization), but it will produce tokens like `rock`, `##ing`, `sock`, `##et` which can then be concatendated / aggregated when 2 tokens are needed to combine to create a word like `rocket`. These models require their own complete training loop (which mostly means a few loops of greedy algorithms until convergence, not actual loss based ML models), and afterwards create a vocabulary of size $V$ for us to use. This hypothetically can extend to all future words, even ones we haven't seen yet (out-of-vocabulary) like `yoloing`, where the absolute furthest fall back is individual characters like `[y, o, l, o, ##ing]`. This means we don't have to constantly retrain the tokenization model for viral words or new phrases. The vocabulary itself will just have integers assigned to each of the tokens, and so for each token in future sequences we will look to find exact matches of those tokens, and worst case fall back to individual characters, and the ultimate output of this tokenization will be some way to lookup individual integers or embeddings for each token
- During training there will be batching performed, and so actual sequences may be of different sizes, and the shorter ones all need to have extra padding via `[PAD]` tokens, and longer ones may be shrunk down to some specific size
    - Then, every input sequence is of the same size and can be sent through in a batch
- There are other special tokens used like `[BOS]`, `[EOS]`, and `[CLS]` for marking beginning of sentences, ends, and places to classify or predict words

![Tokenizer](/img/gpt_tokenizer.png)

Character / token level ascii characters can't be used very well in neural networks, and so most actual computations are done on [embeddings](/docs/transformer_and_llm/EMBEDDINGS.md). The most well documented and "Hello World" version of this is [Word2Vec](/docs/transformer_and_llm/EMBEDDINGS.md#word2vec), which creates static embeddings for each token in the input vocabulary by utilizing a bag-of-words or skip-gram architecture for predicting context words / missing single words in the training dataset to come up with a compressed representation of size $E_d$ for each of the input tokens. Typically this is size 128, 256, 512, or 1024. These embeddings are static, and so `the river bank` and `the bank teller`, both `bank` instances here have the same underlying embedding representation. Most LLM systems come up with their own embeddings during training, and don't reuse foundational vocabularies like those in Word2Vec. A key point on the examples below is most of them are pulling integer values for the tokens, which are actually just used as lookups to actual embedding vectors, so the input to the model is actually a sequence of embedding vectors of size $E_d$ for each token in the input sequence, and these are then sent through the rest of the model architecture. The embedding layer is essentially a lookup table that takes in the integer token IDs and outputs their corresponding embedding vectors, which are then fed into the subsequent layers of the model

![Embedding Lookup](/img/embedding_lookup.png)

At this point the first ~2 layers of any LLM are usually covered, there are some other layers such as [positional encodings](/docs/transformer_and_llm/TRANSFORMERS.md#positional-encoding) that are used to encode the position of the token in the sequence

![Input Layers](/img/llm_input_layers.png)

During training next token prediction is the usual task, along with next sentence prediction, masked language modeling, and other similar tasks. The loss function is usually some form of cross-entropy loss, and the model is trained to minimize this loss across the training dataset. ***Sliding window sampling*** is the method used to create each of these pairs of input and output sequences, where we take a window of size $N$ and slide it across the input sequence to create multiple training examples. For example, if we have a sequence of tokens `[the, cat, sat, on, the, mat]` and a window size of 3, we would create training examples like:
- Input: `[the, cat, sat]`, Output: `on`
- Input: `[cat, sat, on]`, Output: `the`
- Input: `[sat, on, the]`, Output: `mat`

The main parameters in sliding window are:
- Window size: The number of tokens in the input sequence (e.g., 3 in the example)
- Stride: The number of tokens to move the window each time (e.g., 1 in the example, which means we move the window one token at a time)


![Sliding Window Sampling](/img/sliding_window_sampling.png)

![Stride](/img/sliding_window_stride.png)

<!-- Collapsible Python snippet -->
<details>
  <summary>TikToken Tokenizer + Sampling</summary>

```python
from tiktoken import TikTokenizer
tokenizer = TikTokenizer()
text = (
    "Hello, do you like tea? <|endoftext|> In the sunlit terraces"
     "of someunknownPlace."
)
encoded = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
print(encoded)
# [15496, 11, 466, 345, 588, 8887, 30, 220, 50256, 554, 262, 4252, 18250,
#   8812, 2114, 286, 617, 34680, 27271, 13]

strings = tokenizer.decode(encoded)
print(strings)

# Hello, do you like tea? <|endoftext|> In the sunlit terraces of
#   someunknownPlace.

# Sliding Window
context_size = 4         #1
x = encoded[:context_size]
y = encoded[1:context_size+1]
print(f"x: {x}")
print(f"y:      {y}")

for i in range(1, context_size+1):
    context = enc_sample[:i]
    desired = enc_sample[i]
    print(context, "---->", desired)

# [290] ----> 4920
# [290, 4920] ----> 2241
# [290, 4920, 2241] ----> 287
# [290, 4920, 2241, 287] ----> 257
#  and ---->  established
#  and established ---->  himself
#  and established himself ---->  in
#  and established himself in ---->  a

```
</details>

This is all great theory, but the actual training of models requires large scale iterators ran over distributed compute. The actual training pipeline should use a distributed training framework like PyTorch's Distributed Data Parallel (DDP) or TensorFlow's `MirroredStrategy` to parallelize the training across multiple GPUs or even multiple machines. These allow us to write some general pipeline code, and then `MirroredStrategy` will take care of the distribution and synchronization of gradients across the different devices. The training loop itself will involve iterating over the training dataset, computing the loss, and updating the model weights using an optimizer like Adam or SGD. Writing synchronization code across potentially failing hardware during training loop runs would take months of work, testing, and planning. Instead of doing that, just reuse the community tested and used frameworks!

These frameworks utilize autoloaders and iterators to handle data loading and batching. Under the hood most of the iterators run as generators which yield batches of data to the training loop, and these batches are then sent to the appropriate devices for training. The frameworks also handle the synchronization of gradients across devices, which is crucial for ensuring that the model converges properly during training

<!-- Collapsible Python snippet -->
<details>
  <summary>Torch Data Loader</summary>

```python
import torch
from torch.utils.data import Dataset, DataLoader
class GPTDatasetV1(Dataset):
    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []

        # Tokenize the actual text
        token_ids = tokenizer.encode(txt)

        # Use a sliding window to chunk the 
        #  sequence into overlapping sequences of max_length
        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    # Get total n rows
    def __len__(self):
        return len(self.input_ids)

    # Get a single row from the dataset
    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]

def create_dataloader_v1(txt, batch_size=4, max_length=256,
                         stride=128, shuffle=True, drop_last=True,
                         num_workers=0):
    # Initialize tokenizer and dataset
    tokenizer = tiktoken.get_encoding("gpt2")
    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        # drop_last=True drops the last batch if it is shorter than the 
        #   specified batch_size to prevent loss spikes during training
        drop_last=drop_last, 
        # The number of 
        #   CPU processes to use for preprocessing       
        num_workers=num_workers
    )

    return dataloader

# Dummy input text
with open("file.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

dataloader = create_dataloader_v1(
    raw_text, batch_size=1, max_length=4, stride=1, shuffle=False)

# Generator that yields batches of data from the dataloader
data_iter = iter(dataloader)
first_batch = next(data_iter)
print(first_batch)
```
</details>

For each of the batches for our sliding window, we can setup window size, stride, and batch size as needed. After this, each of the batches can be padded to the same length, and sent through the model for training. A batch size of 32 will result in 32 sequences of $E_d$ dimensional embeddings with 32 corresponding target sequences / labels

Finally, most of the embeddings also require [positional encodings](/docs/transformer_and_llm/TRANSFORMERS.md#positional-encoding), which are added to the token embeddings to give the model information about the position of each token in the sequence. This is crucial for the model to understand the order of the tokens, which is important for tasks like language modeling and translation. The positional encodings can be either learned or fixed, and they are typically added to the token embeddings before being fed into the transformer layers. Positional encoding structure and in depth choices are discussed more in that Transformers sub-document

So overall, the final preparation, tokenization, and embedding layers will result in a number of input layers below, and during training there's sliding, window size, and generation considerations for us to produce the actual input and training labels
    - LLMs require textual data to be converted into numerical vectors, known as embeddings, since they can’t process raw text. Embeddings transform discrete data (like words or images) into continuous vector spaces, making them compatible with neural network operations
    - As the first step, raw text is broken into tokens, which can be words or characters. Then, the tokens are converted into integer representations, termed token IDs
    - Special tokens, such as <|unk|> and <|endoftext|>, can be added to enhance the model’s understanding and handle various contexts, such as unknown words or marking the boundary between unrelated texts
    - The byte pair encoding (BPE) tokenizer used for LLMs like GPT-2 and GPT-3 can efficiently handle unknown words by breaking them down into subword units or individual characters
    - We use a sliding window approach on tokenized data to generate input–target pairs for LLM training
    - Embedding layers in PyTorch function as a lookup operation, retrieving vectors corresponding to token IDs. The resulting embedding vectors provide continuous representations of tokens, which is crucial for training deep learning models like LLMs
    - While token embeddings provide consistent vector representations for each token, they lack a sense of the token’s position in a sequence. To rectify this, two main types of positional embeddings exist: absolute and relative. OpenAI’s GPT models utilize absolute positional embeddings, which are added to the token embedding vectors and are optimized during the model training

![Final Embedding Layers](/img/final_training_embedding_layers.png)


## Architectures
Multiple architectures, all used for diff things and probably covered elsewhere

### Encoder Only
Encoder only models like [BERT are trained for masked language modeling](/docs/transformer_and_llm/BERT.md#training). Actual BERT training information is stored in that page, but will go more in depth here

TODO

### Encoder Decoder

### Decoder Only
Decoder only models like [GPT-3](/docs/transformer_and_llm/GPT.md) only use the decoder portion, and are trained on massive datasets using solely a next word prediction task

They still focus on auto-regressive decoder-only architecture, and ultimately utilizing the next word / sentence prediction means the 400 billion token input dataset can be re-used almost infinitely