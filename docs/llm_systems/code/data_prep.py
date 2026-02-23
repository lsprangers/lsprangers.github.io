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

# >>> inputs.size(), targets.size()
# (torch.Size([8, 4]), torch.Size([8, 4]))
inputs, targets = next(data_iter)

# >>> print(inputs, targets)
# tensor([[   40,   367,  2885,  1464],
#         [ 1807,  3619,   402,   271],
#         [10899,  2138,   257,  7026],
#         [15632,   438,  2016,   257],
#         [  922,  5891,  1576,   438],
#         [  568,   340,   373,   645],
#         [ 1049,  5975,   284,   502],
#         [  284,  3285,   326,    11]]) 
# tensor([[  367,  2885,  1464,  1807],
#         [ 3619,   402,   271, 10899],
#         [ 2138,   257,  7026, 15632],
#         [  438,  2016,   257,   922],
#         [ 5891,  1576,   438,   568],
#         [  340,   373,   645,  1049],
#         [ 5975,   284,   502,   284],
#         [ 3285,   326,    11,   287]])
# >>> token_embedding_layer
# Embedding(50257, 256)
token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
# >>> token_embeddings.size()
# torch.Size([8, 4, 256])
token_embeddings = token_embedding_layer(inputs)

# tensor([[-1.4150, -0.3142,  0.2827,  ...,  0.8155, -0.1085, -1.1927],
#         [-1.9800,  0.0610, -0.0494,  ..., -0.6422,  0.5716, -1.1329],
#         [ 1.0052,  1.7802,  1.2652,  ..., -1.1619, -0.1109,  1.0411],
#         [ 0.3760, -0.3758, -0.0484,  ...,  0.1080,  0.3852,  1.0876]],
#        grad_fn=<EmbeddingBackward0>)
# >>> print(pos_embeddings.size())
# torch.Size([4, 256])
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
# torch.arange() method in PyTorch returns a 1-dimensional tensor with 
#   values from a specified interval [start, end), 
#   using a common difference step
# torch.arange(context_length)
# tensor([0, 1, 2, 3])
# >>> pos_embeddings.size()
# torch.Size([4, 256])
pos_embeddings = pos_embedding_layer(torch.arange(context_length))
input_embeddings = token_embeddings + pos_embeddings

# These position indices are wrong!
# - I do think this is incorrect, on purpose, because if our positional embeddings are created via `torch.arange()` and come out to `[0, 1, 2, 3, 4]`, our inputs are
#     - tokens at `[0, 1, 2, 3, 4]` with targets `[1, 2, 3, 4, 5]`
#     - ***but the next rows have stride***
#     - The next row in batch is `[0+stride, 1+stride, 2+stride, 3+stride]`, with targets `[1+stride, 2+stride, 3+stride, 4+stride]`, and so adding the static positional embeddings here would be incorrect
#     - ***Need to update positional embeddings to include stride***

# position_indices = torch.arange(max_length).unsqueeze(0) + torch.arange(max_length).unsqueeze(1) * 4
# >>> position_indices
# tensor([[ 0,  1,  2,  3],
#         [ 4,  5,  6,  7],
#         [ 8,  9, 10, 11],
#         [12, 13, 14, 15]])

# >>> input_embeddings.size()
# torch.Size([8, 4, 256])
# >>> input_embeddings
# tensor([[[-1.3080, -0.4570, -0.0187,  ..., -1.5083, -0.0307, -0.5237],
#          [-0.9927,  0.1774, -0.6220,  ..., -0.3200,  1.7776, -0.9121],
#          [-0.2581,  1.4565,  2.0810,  ..., -1.0276,  0.7567, -1.4643],
#          [-0.2765, -0.9566,  1.0705,  ...,  0.2612, -0.7349,  0.5785]],

#         [[-2.6367,  1.5577,  1.7478,  ..., -0.5983,  0.1394,  0.3386],
#          [-0.8915, -0.3899,  0.0893,  ...,  0.0802,  0.7632, -1.0324],
#          [ 2.2274,  1.7110,  2.0338,  ..., -1.0126,  1.3322,  1.5231],
#          [-0.9140, -0.8064,  0.3478,  ...,  0.4810, -0.2518,  1.4475]],

#         [[-1.2779, -0.2667,  0.8431,  ...,  1.5746,  1.0428, -1.0772],
#          [-1.9595, -0.1261, -0.3843,  ..., -2.3072,  2.4937, -1.9248],
#          [ 0.0746,  1.8754, -0.0708,  ..., -2.5317, -1.5784,  0.9713],
#          [ 0.6891, -0.0913,  0.5818,  ..., -1.0321, -1.0600,  2.4763]],

#         ...,

#         [[-1.7172, -0.2438, -0.9338,  ...,  1.1428,  0.0320,  0.5412],
#          [-2.6241, -2.2694,  0.2846,  ..., -2.0332, -0.7378,  0.2111],
#          [ 3.7448,  2.5806,  1.9771,  ..., -0.2014,  0.3627,  1.8011],
#          [ 1.4523,  1.8036,  0.9495,  ..., -0.2169, -2.1250,  1.5692]],

#         [[-0.4155,  0.5793,  0.2631,  ...,  1.5524, -0.0322, -1.1776],
#          [-1.9848, -0.4031, -1.6609,  ...,  0.2679, -0.2796, -2.7857],
#          [ 2.7567,  1.1848,  2.1343,  ...,  1.0998, -0.5136,  1.4549],
#          [-0.3326,  1.7206, -1.6837,  ..., -0.3171,  1.3379,  2.5444]],

#         [[ 0.3365, -0.9096,  1.1519,  ...,  3.0772, -0.5112, -0.7789],
#          [-2.2273, -0.3134,  0.6421,  ..., -1.2942,  0.7259, -0.9337],
#          [ 0.8002,  3.4395,  0.9191,  ..., -1.4590,  0.8257,  0.2433],
#          [ 0.5343, -0.3691, -0.1222,  ..., -0.2099, -0.7576,  0.9645]]],
#        grad_fn=<AddBackward0>)