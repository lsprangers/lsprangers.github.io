import torch
from torch.utils.data import Dataset, DataLoader
import tiktoken

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

# cd /Users/lukesprangers/repos/lsprangers.github.io/docs/llm_systems/code

# Dummy input text
with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

torch.manual_seed(123)
vocab_size = 50257
output_dim = 256
max_length = 4
context_length = max_length

dataloader = create_dataloader_v1(
    raw_text, batch_size=8, max_length=max_length,
    stride=max_length, shuffle=False
)
# Generator that yields batches of data from the dataloader
data_iter = iter(dataloader)
inputs, targets = next(data_iter)

token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
token_embeddings = token_embedding_layer(inputs)
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
pos_embeddings = pos_embedding_layer(torch.arange(context_length))
input_embeddings = token_embeddings + pos_embeddings