---
layout: technical
title: Transformer Training Optimizations
category: NLP, CV, and Transformers
difficulty: Advanced
description: Discussions around Loss Functions in NN's
show_back_link: true
---

## Training Optimizations
There's a few papers that come up on training, and by proxy inference, optimizations for Transformer models

The paper [A Survey Of Efficienct Transformers](/arxiv_papers/Efficient%20Transformers%20MarkedUp.pdf) talks about ways to reduce the computational and memory costs associated with Transformers

Some key reasons:
- Embedded devices are subject to strict memory and compute limits
- Accelerated compute devices (specific GPU's) may have limited memory to run models on
    - Inference and training
- Real time applications for chat-bots and other service industries

The main crux focused on is the [Self-Attention](/docs/transformer_and_llm/ATTENTION.md#self-attention) piece which is $O(n^2)$ by nature, along with some other on-device updates like FlashAttention which I'm not smart enough to even try to read

### Self Attention Optimization Methods
- ***Fixed Patterns*** are patterns with set or "rigid" changes to self attention
    - ***Blocking***: This is effectively using convolutions on top of 1-D sequences to reduce the total number of tokens compared down from $n$
        - Instead of doing the entire $n$ sequence, find a $B \st B << N$ so that the final result is $O(b^2)$ 
            - This is just running self attention on a much smaller window / block
            - Reducing the attention span!
    - ***Strided***: Similar to above, except you only attend at certain fixed length intervals
- ***Combination of Patterns***
    - This is just using multiple Fixed Patterns in different heads of Multi Headed Attention
    - 1/2 get Blocking, 1/2 get Strided
- ***Learnable Patterns***
    - This one sounds cool, but I don't fully understand it
    - Basically use another layer somewhere / some data somewhere to have model choose pattern to use
    - (Vyas et al., 2020; Wang et al., 2020b). Notably, Reformer (Kitaev et al., 2020)
    - Routing Transformer (Roy et al., 2020) employs online k-means clustering on the tokens
    - The key idea of learnable patterns is still to exploit fixed patterns (chunked patterns).
- ***Low Rank*** tries to find a fixed lower rank matrix to that approximates the $NxN$ self attention matrix into something more like $N xk$
    - ***Kernels***: Kernalization, while not explicitly tied in the paper, sounds most like a method for Low Rank
        - "Kernels allow us to use clever mathematical re-writing of the self attention formula to avoid explicitly calculating the $NxN$ matrix"
        - Kernels are a form of approximation for the self-attention matrix
- ***Recurrence*** recurrently connects the blocks from Blocking Fixed Pattern...
- ***Down Sampling*** is about reducing the resolution of sequences
- ***Sparse Models and Conditional Computation***
    - Sparse activation of a subset of parameters to generally improve FLOPs ratio

