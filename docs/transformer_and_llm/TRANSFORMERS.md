---
layout: technical
title: Transformers and Attention
category: NLP, CV, and Transformers
difficulty: Advanced
description: Discussions around the Attention mechanism in NLP, CV, and Transformers
show_back_link: true
---

## Attention
[Seq2Seq Models](/docs/transformer_and_llm/SEQ2SEQ.md) with encoder-decoder architectures looked to encode the entire context into a singular vector $c_t$ that got passed to each decoder step, which led to bottlenecks, inefficiencies, etc

Attention, as an embedding concept, is what separates static embeddings from dynamic embeddings - they allow word embeddings to be updated, aka attended to, by the contextual words surrounding them

Transformers as an architecture helped to make attention a parallelizable function, ultimately allowing for context to spread in a way that no longer bottlenecked infromation into a context vector, and allowed for large scale SIMD type of parallel processing

![Seq2Seq VS Transformer](/img/seq2seq_vs_transformer.png)

NLP Seq2Seq Tasks like next word prediction, and translation where using the surrounding context of the word was one of the major breakthroughs in achieving better Seq2Seq results. Attention helps to fix the **bottleneck problem** in [RNN encoder (and RNN encoder-decoder) models](/docs/transformer_and_llm/EMBEDDINGS.md#encoder-decoder) - Due to their design, the encoding of the source sentence is a single vector representation $C_t$ (context vector). The problem is that this state must compress all information about the source sentence in a single vector and this is commonly referred to as the bottleneck problem. There was a desire to not "squish" everything into one single context vector, and instead to utilize the input embeddings dynamically when decoding, and to utilize the context on the fly - this is known as *align and translate jointly*

![Align and Translate Jointly](/img/align_and_translate_jointly.png)

The embedding for "bank" *is always the same embedding in the metric space* in static scenario's like [Word2Vec](/docs/transformer_and_llm/EMBEDDINGS.md#word2vec), but by attending to it with Attention, you can change it's position! It's as simple as that, so at the end of attending to the vector, the vector for bank in river bank may point in a completely different direction than the vector for bank in bank vault - just because of how the other words add or detract from it geometrically in its metric space. Bank + having river in sentence moves vector in matrix space closer to a sand dune, where Bank + teller in sentence moves it closer to a financial worker

How is this done? Attention mechanisms in our DNN models. There are multiple forms of Attention - most useful / used are Self Attention, Encoder-Decoder Attention, and Masked Self Attention - each of them help to attend to a current query word / position based on it's surroundings. A single head of this Attention mechanism would only update certain "relationships", or attended to geometric shifts, but mutliple different Attention mechanisms might be able to learn a dynamic range of relationships

![Attention High Level Zoom In](/img/attention_high_level_with_zoom_in.png)

In the days before Attention, there would be Encoders that take input sentence and write it to a fixed size embedding layer, and then a separately trained Decoder that would take the embedding and output a new sentence - this architecture for Seq2Seq tasks is fine for short sequences, but degrades with longer sequences you try to "stuff into" a fixed size embedding layer 

Therefore, Attention helps us to remove this fixed size constraint between encoders and decoders, but attention does no more than weighted averaging, and so without neural network layer functions it's strictly weighted averaging. Transformers help change this and add in non-linear layers

All of these Attention mechanisms are tunable matrices of weights - they are learned and updated through the model training process, and it's why you need to "bring along the model" during inference...otherwise you can't use the Attention!

Below shows an example of how an embedding like creature would change based on surrounding context

![Fluffy Blue Attention](/img/fluffy_blue_creature.png)

Or showcasing how adjective / adverb positions are different between languages

![Adjective Positions](/img/adjective_positions.png)

### Keys, Queries, and Values Intuition
Lots of the excerpts here are from the [D2L AI Blog on Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html)

Consider a K:V database, it may have tuples such as `('Luke', 'Sprangers'), ('Donald', 'Duck'), ('Jeff', 'Bezos'), ..., ('Puke', 'Skywalker')` with first and last names - if you wanted to ***query*** the database, we'd simply query based on a key like `Database.get('Luke')` and it would return `Sprangers`

If you allow for approximate matches, you might get `['Sprangers', 'Skywalker']` 

Therefore, our Queries and our Keys have a relationship! They can be exact, or they can be similar (Luke and Puke are similar), and based on those similarities, you may or may not want to return a Value. Thinking of self-attention as an approximate hash table eases understanding its intuition. To look up a value, queries are compared against keys in a table. In a hash table, which is shown on the left side of image below, there is exactly one key-value pair for each query (hash). In contrast, in self-attention, each key is matched to varying degrees by each query. Thus, a sum of values weighted by the query-key match is returned

![Q, K, V Hash Table](/img/q_k_v_hash_table.png)

What if you wanted to return a portion of the Value, based on how similar our Query was to our Key? Luke and Luke are 1:1, so you fully return Sprangers, but Luke and Puke are slightly different, so what if you returned something like `intersect / total` * Value, or 75% of the Value?

Luke and Puke have $3/4$ letters as the same, so you can return $3/4$ of Skywalker!

This is the exact idea of Attention - $Attention(\bold{q}, D) = \sum_{i = 1}^{m} \alpha(\bold{q}, \bold{k_i}) \cdot \bold{v_i}$

This attention can be read as "for every key / value pair $i$, compare the key and the value with $\alpha$, and based on how similar they are return that much of the value. The total sum of all those values is the value you will return"

Therefore, you can mimic an exact lookup if you define our $\alpha$ as a Kronecker Delta:
$
\delta_{ij} = \begin{cases}
1, & \text{if } q = k_i,\\
0, & \text{if } q \neq k_i
\end{cases}
$

This means we'll return the list of all values that match `Luke`, which is just 1

Another example would be if 
```
D = [
   ([1, 0], 4), 
   ([1, 1], 6), 
   ([0, 1], 6)
]
```

And our Query is `[0.5, 0]` - if you compare that to all of our Keys, we'd see `distance([0.5, 0] - [1, 0]) = 0.5` and `distance([0.5, 0] - [1, 1]) = - 0.5` so you would have `0.5 * 4 + -0.5 * 6 = -1` would be our answer!

So these comparisons of Queries and Keys results in some weight, and typically you will compare our Query to every Key, and the resulting set you will stuff through a Softmax function to get weights that sum to 1

$
\alpha(\bold{q}, \bold{k_i}) = {a(\bold{q}, \bold{k_i}) \over \sum_{j}a(\bold{q}, \bold{k_j})}
$

To ensure weights are non-negative, you can use exponentiation

$\alpha(\bold{q}, \bold{k_i}) = \frac{\exp(a(\bold{q}, \bold{k_i}))}{\sum_{j=1}\exp(a(\bold{q}, \bold{k_j}))}$

This is exactly what will come through in most attention calculations!

![Attention Image](/img/attention_image.png)

### Parameters
In discussions below, we'll use these parameters to talk through time and memory complexities, along with architectures and layers

The input is usually a sequence of size $S$, which has a number of tokens $t_i$, and each of these tokens will go through a static embedding layer to create input embeddings of size $E$ (typically 128). After this, the $S$ embeddings of size $E$ will all go through multiple layers of normalization, dropout, and self-attention to produce output hidden states. These output hidden states are of size $H$ (typically 512), and there would still be $s$ final states, one for each input. These final hidden states are labeled $T_i$

- Parameters:
    - $L$ layers / encoder blocks
    - $H$ is the size of the hidden states
         - 256 is typical size of hidden state dimension
         - $d_h$ is the encoder hidden size
         - $d_s$ is the decoder hidden size
         - $d_a$ is the alignment MLP hidden size
    - $A$ attention heads per layer
        - Typically 6 attention heads
    - $E$ represents the input embedding dimension
        - 128 is typical embedding dimension
    - $C \in \real^H$ represents the final hidden vector (of size $H$) of our `[CLS]` token (i.e. our "final" hidden layer for our sentence)
    - $T_i \in \real^H$ as the final hidden state for a specific input token $w_i$
    - $P_i$ is our positional encoding which represents the learned positional embedding for our token in it's specific sentence of any size
    - $X_i$ is our segment encoding which represents the learned positional embedding for our token in either segment sentence A or B
        - In our inference time examples for embeddings most people just fill it with `0's` or `1's` depending on which sentence it's apart of

### Bahdanau RNN Attention
Things first started off with Bahdanau Style RNN Attention via [Neural Machine Translation by Jointly Learning to Align and Translate (2014)](https://arxiv.org/abs/1409.0473)

This paper discusses how most architectures of the time have a 2 pronged setup:
- An encoder to take the source sentence into a fixed length vector
   - In most scenario's there's an encoder-per-language
- A decoder to take that fixed length vector, and output a translated sentence
   - There's also typically a decoder-per-language as well
- Therefore, for every language there's an encoder-decoder pair which is jointly trained to maximize the probability of correct translation
---

- Why is this bad?
   - Requires every translation problem to be "squished" into the same fixed-length vector
   - Examples cited of how the performance of this encoder-decoder architecture deteriorates rapidly as the length of input sentence increases
---
- Proposal in this paper:
   - "you introduce an extension of the encoder-decoder model which learns to align and translate jointly"
      - This means it sets up (aligns) and decodes (translates) on the fly over the entire sentence, and not just all at once
   - "Each time the proposed model generates a word in a translation, it (soft-)searches for a set of positions in a source sentence where the most relevant information is concentrated
      - This means it uses some sort of comparison (later seen as attention) to figure out what words are most relevant in the translation
   - The model then predicts a target word based on the context vectors associated with these source positions and all previously generated target words
      - The model predicst the next word based on attention of this word and input sentence + previously generated words
      - This was a breakthrough in attention, but apparently was proposed here earlier!
- Altogether, this architecture looks to break away from encoding the entire input into one single vector by encoding the input into a sequence of vectors which it uses adaptively while decoding

![RNN Attention](/img/rnn_attention.png)

- The bottom portion is an encoder which receives source sentence as input
- The top part is a decoder, which outputs the translated sentence

#### Encoder RNN Attention
- ***Input***: A sequence of vectors $\bold{x} = (x_1, ..., x_n)$
   - ***Encoder Hidden States***: $h_t = f(x_t, h_{t-1})$
      - $f$ is some non-linear function
      - This will take the current input embedding, and the output of the last recurrence
      - These are bi-directional
         - $\overrightarrow{h_2} = f(x_2, h_1)$
         - $\overleftarrow{h_2} = f(x_2, h_3)$
         - $h_2 = [\overrightarrow{h_2} \frown \overleftarrow{h_2}]$
            - Concatenation!
      - It is formalized that $h_t \in \mathbb{R^{d_h}}$ is the hidden state of the encoder at time $t$
- These $h_i = [\overrightarrow{h_i} \frown \overleftarrow{h_i}] \space \forall i \in \{1, ..., T_x\}$ 
   - They live entirely in the encoder block
   - They are fixed once the input is encoded

![RNN Encoder GIF](/img/RNNEncoderSetup.gif)

#### Decoder RNN Attention
Decoder is often trained to predict the next word $\hat{y_t}$ given the context vector $c_t$ and all the previously predicted words $\{\hat{y_1}, ..., \hat{y_{t-1}} \}$

Our translation can be defined as $\bold{y} = (y_1, ... y_{T_n})$ which is just the sequence of words output so far!

It does this by defining a probability distribution over the translation output word $\bold{y}$ by decomposing the joint probability. 

$p(\bold{y}) = \prod_{t=1}^{T} p(y_t \mid \{y_1, \ldots, y_{t-1}\}, c_t)$

*Since our $\bold{y}$ is just our entire word sequence, the probability we're solving for is "the probability that this is the sequence of words given our context vector $c_t$"*

So we're just choosing the next most likely word so that the probability of seeing all these words in a sequence is highest

The sequence "Hi, what's your", if you looked over all potential next words, would most likely have the highest predicted outcome of "Hi, what's your name"

Each of these conditional probabilities is typically modeled with a non-linear function $g$ such that 

So, ***at each time step $t$*** the decoder combines:
- ***Decoder hidden state formula***: $g_t = f(g_{t-1}, y_{t-1}, c_t) \in \mathbb{R^{d_s}}$  based on
   - $g_{t-1}$ the last hidden state
      - Dimension $d_s$
   - $y_{t-1}$ the last output word
   - $c_t$ the context at that state
      - $c_t = \sum_{i=1}^{T_x} \alpha_{ti}h_i$
      - Where $\alpha_{ti}$ is the weight applied to $h_i$ based on the comparison similarity between the last decoder hidden state $g_{t-1}$ to each encoder hidden state (annotation) $h_i$ 


#### Learning To Align And Translate
The rest of the architecture proposes using a bi-directional RNN as an encoder, and then a decoder that emulates searching the source sentence during translation

The "searching" is done by comparing the decoders last hidden state $g_{t-1}$ to each encoder hidden state $h_i \space \forall i \in [1,...,T_x]$ in our alignment model, and then creating a distribution of weights (softmax) to create a context vector. This context vector, the previous hidden state, and the previous hidden word help us to compute the next word!

**P.S. the alignment model here is very similar to self-attention in the future

Since sentences aren't exactly isomoprhic (one-to-one and onto), there may be 2 words squished into 1, 1 word expanded to 2, or 2 non-adjacent words that are used in outputting 1 

***Realistically, any Seq2Seq task that isn't isomorphic would benefit from this structure***

#### Summary
- ***Encoder***
   - $h_t \in \mathbb{R^{d_h}}$ is the encoder hidden state / annotations
      - $\overrightarrow{h_2} = f(x_2, h_1)$
      - $\overleftarrow{h_2} = f(x_2, h_3)$
      - $h_2 = [\overrightarrow{h_2} \frown \overleftarrow{h_2}]$ 
         - Concatenation!  
- ***Decoder***
   - For each step $t$, you need to come up with a context vector $\bold{c}_t$
   - $e_{ti} = a(g_{t-1}, h_i)$ is an alignment model which scores similarities between decoder hidden state at $t-1$ and ***all encoder states***, where each one is denoted at some time $i$
      - $a(\cdot)$ is a small feed-forward NN defined below
      - $e_{ti} = {\bold{v}^T} \cdot \tanh({W_s} \bold{g_{t-1}} + {W_h}{\bold{h}_i})$
         - $e_{ti}$ is the alignment score
         - $W_s \in \mathbb{R^{d_a \times d_s}}$
         - $W_h \in \mathbb{R^{d_a \times d_h}}$
         - $\bold{v} \in \mathbb{R^{d_a}}$
            - $\bold{v}$ is a learned vector that helps compute the scalar alignment score
         - What does this mean?
            - ${W_s} \bold{g_{t-1}}$ is a weighted version of our decoder hidden state at $t-1$
            - ${W_h}{\bold{h}_i}$ is a weighted version of our encoder hidden state at time $i$
            - Therefore, $\tanh(\cdot) \in [-1, 1]$ acts as an activation function which helps us to score how close the decoder hidden state at $t-1$ and our current encoder hidden state at $i$ are
   - Normalize with softmax to get attention weights $\alpha_{ti} = \frac{\exp(e_{ti})}{\sum_{k=1}^{T_x} \exp(e_{tk})}$
      - $e_{tk}$ will be the attention score of $t$ to all other states
         - If there are 5 words in the input, and we're at $t = 3$, this will score how well $g_2$ is to $h_3$ compared to all other annotations $h_{[1, 2, 4, 5]}$
         - Another blog mentioned how attention scores $e_t$ are computed by "scalarly combining the hidden states of the decoder with all of the hidden states of the encoder"
            - ***The below is Luong Style Attention, not Bahdanau***
            - $e_t = [(g^t)\cdot{h}^1, ... , (g^t)\cdot{h}^n]$
      - This will convert scores into a probability distribution
      - Since our attention model helps to compute scores across encoder hidden states to a decoder hidden state, taking the softmax here will then give us the ***relative weight of each encoder hidden state to a decoder hidden state***
   - Form the context vector, AKA attention output, $\bold{c}_t$ as the weighted sum of these annotations
      - $\bold{c}_t = \sum_{i=1}^{T_x} \alpha_{ti} \cdot h_i$
         - Where $\alpha_{ti}$ is the weight of $g_{t-1}$ compared to each annotation $h_i$ and is a similarity metric between the two
   - $g_t = f(g_{t-1}, y_{t-1}, c_t) \in \mathbb{R^{d_s}}$ is the decoder hidden state
      - $y_{t-1}$ is the last output word from decoder
   - To bring it all out:
      - $g_t = f(g_{t-1}, y_{t-1}, \sum_{i=1}^{T_x} (\frac{\exp(a(g_{t-1}, h_i))}{\sum_{k=1}^{T_x} \exp(a(g_{t-1}, h_k))}) \cdot h_i$ )
         - Our query is $g_{t-1}$, and our keys / values are $h_i$
         - Our attention score is based on $\alpha_{ti} = \frac{\exp(e_{ti})}{\sum_{k=1}^{T_x} \exp(e_{tk})}$ which is multiplied by $h_i$ to attend to it
   - $g_t$ will typically combine the vectors of it's inputs via addition, concatenation, etc and pass them through a nonlinear function $f$
      - GRU, LSTM, etc
   - All of this will be the basis of [Self-Attention](#self-attention) in the future, and for this you can just read this as the context vector $c_i$ is based on the similarity of an input annotation with the rest of the annotations

[D2L AI Code Implementation In PyTorch](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)

![RNN Decoder GIF](/img/RNNDecoderSetup.gif)
---

Intuition
- In the paper they even mention *"this implements a mechanism of attention in the decoder"*
- In the encoder, the only major trick is doing bi-directional hidden states and then concatenating them
   - This productes the annotations themselves
   - $h_i = [\overrightarrow{h_i}, \overleftarrow{h_i}]$
   - These annotations are then fed through the alignment, alpha weight, and context vectors before being used in the decoder with the last output word and hidden state
      - This context vector allows us to "attend to" the last output word and last hidden state
      - What's missing from transformers? you decide to drag along this hidden weight the entire time, and in Transformers you just re-compute context vector for each vector

$\text{max}_{\theta} {1 \over N} \sum_{n = 1}^{N} \log p_{\theta}(y_n | x_n)$

Where the best probability is usually found using beam search - at each step of the decoder you keep track of the $k$ most probable partial translations (hypotheses)

![RNN Loss Objective](/img/rnn_loss_objective.png)

![RNN Attention](/img/rnn_attention.png)

#### Bahdanau Attention Time Complexities
To recap:
- $T_x$ = encoder length (meaning the number of hidden states in encoder output, i.e. number of embeddings we encoded)
- $T_y$ = decoder length (the length of the output we eventually reach) 
   - It is not necessary that $x = y$, and in fact is a feature that they aren't equal
- $d_h$ = encoder hidden size (the dimension of a single hidden state)
- $d_s$ = decoder hidden size
- $d_a$ = alignment MLP hidden size (the dimension of the MLP that maps alignment scores)
- $B$ = batch size input

Ultimately ***Bahdanau Attention*** scales linearly with the encoder length per decoder step, because during alignment $e_{ti}$ we are comparing the decoder hidden state $d_s$ to each encoder hidden state $d_h$ for all $i \in \{1, ..., T_x\}$ - this is exactly what we see in $O(T_x \cdot T_y)$ dominating the overall attention mechanism. Each decoder must score against all encoder hidden states! However, there's no $T_x^2$ term like there will be in self-attention

- Encoder recurrence is $O(T_x(d^2_h + E d_h))$ which showcases how each input embedding flows through and is multiplied by hidden states
- Decoder recurrence is similarly $O(T_y(d^2_s + E d_s))$
- At each decoder step there's some alignment (attention) between the decoder and every encoder $O(T_y(d_a d_s + T_x d_a d_h + T_x d_h))$

The sequence length interaction terms $O(T_x T_y)$ are present everywhere, and then the alignment and hidden dimension matrix multiplication steps are also present with all of the $d$ multiplications

The overall time complexity of the entire encoder-decoder is:
$$O(T_x (d^2_h + E d_h) + T_y (d^2_s + E d_s + T_x d_a d_h))$$

##### Bahdanau Encoder Complexity
The encoder is sequential over $T_x$. It's a recurrent NN, so it must be sequential, since word $t$ needs to know the previous hidden state of $t-1$, so there's no possible way to parallelize across time

The encoder recurrence is 
$$h_t = f(x_t, h_{t-1})$$

So for a GRU / LSTM style cell, it would have time complexity per timestep of $O(d^2_h + E d_h)$ from multiplying input vector by input-to-hidden weights

So therefore, the ***total encoder time complexity*** is:
$$O(B \cdot T_x \cdot (d^2_h + E d_h))$$

We have to store a hidden state for each word, so the ***total encoder space complexity*** is:
$$O(T_x \cdot d_h)$$

##### Bahdanau Alignment + Attention Complexity
Alignment score is 
$$e_{ti} = {v^T} \cdot \tanh({W_s} g_{t-1} + {W_h}{h_i})$$

For each encoder position $i$, with hidden state $h_i$:
- ${W_s} g_{t-1}$ has time complexity $O(d_a \cdot d_s)$
   - $d_a$ is the MLP alignment embedding size
   - $d_s$ is the decoder hidden state, $g_{t-1}$ size
   - ***This is computed once***
- ${W_h}{h_i}$ has time complexity $O(d_a \cdot d_h)$
   - This is computed per $i$
- Adding together, and dotting with $v^T$ is time complexity $O(d_a)$

So:
- Per single encoder token 
   - $i \in \{1, ..., T_x\}$, it's $O(d_a \cdot d_h)$
   - Across all $T_x$ it would be $O(T_x \cdot d_a \cdot d_h)$
   - If $d_a \approx d_h$ then $O(T_x \cdot d^2_h)$
- The single decoder hidden state of $O(d_a d_s)$
- Softmax + context sum $O(T_x d_h)$
   - $c_t = \sum_{i=1}^{T_x} \alpha_{ti} \cdot h_i$
   - $\alpha_{ti}$ is typically a scalar resulting in softmax operation over attention scores, it's different from the $a(\cdot)$ alignment model!
   - Per single encoder token $i \in \{1, ..., T_x\}$, it's $O(T_x \cdot d_h)$

$$O(d_a d_s + T_x d_a d_h + T_x d_h)$$

##### Bahdanau Decoder Time Complexity
$$g_t = f(g_{t-1}, y_{t-1}, c_t)$$

The decoder here is just producing a new hidden state, but inside of a GRU / LSTM both $g_t$ and $h_i$ (which is apart of $c_t$) are multiplied by different weight matrices

Therefore the entire operation is $O(d^2_s + E d_s)$ for each decoder step, and there are $T_y$ decoder steps

$$O(T_y \cdot (d^2_s + E d_s))$$

## Transformer Attention
The above RNN discussion is useful, as it shows how you can utilize the building blocks of forward and backwards passes, and even achieve attention mechnisms using basic building blocks

***RNN's are sequential, and therefore have trouble with parallel processing and fully utilizing GPU's - Transformers aim to parallelize and remove recurrence relations***

RNN's also fail with long term dependencies - the sentence "he was near the large stadium with Sarah and was named Cam", you would need to keep track of every word between "he" and "Cam" to have the word "he" have any sort of effect on Cam. A direct consequence of this is the inability to train in parallel on GPU's because future hidden states cannot be computed in full before past hidden states have completed.

Attention also helps to alleviate the bottleneck problem, where all context is "shoved" into a singular vector. Attention allows all encoded infromation to help influence the context and decoding during each step, and helps to alleviate the vanishing gradient problem from long sentences that end up multiplying multiple numbers $\lt$ 1.0 throughout numerous steps. 

Attention does no more than weighted averaging, and so without neural network layer functions it's strictly weighted averaging. Transformers help change this and add in non-linear layers. Transformers use each of the Q,K,V vectors to bring about more expressive traits, which furthers attention from being simple weighted averaging to be able to learn similarity metrics, different feature subspaces, and overall increase representational flexibility. That's why transformer architectures eventually use multiple layers of projected self-attention (parallelized), with further non-linear and other activation layers (feed forward, residual connections, etc), and potential future masking strategies. All of these different choices help to ensure transformers tackle a vast set of NLP problems

The rest of the discussion is around Attention blocks in Transformer Architectures, primarily using a similar encoder-decoder structure "on steroids"

![Even Better Transformer Diagram](/img/better_transformer_arch_diagram.png)

### Transformer Extra Parameters
- Input $x_i \in \real^d$
- $S$ = Sequence length
- $d$ = Model dimension
- $h$ = # of heads
- $d_k$ = $d$ / $h$
- Projection matrices $W_Q$, $W_K$, $W_V \in \real^{d \times d}$

![Transformers High Level](/img/transformers_high_level.png)

### Key, Query, and Value Matrices
Self-Attention and K,Q,V go hand in hand - the intuition for K,Q,V can be seen from an approximate hash table:
- To lookup a value, queries are compared against keys in a table
- In the Hash Table below, there's exactly one K:V pair for any Q
   - In contrast for self attention, each Query is measured against all Keys, and the amount of that overlap is assigned to the Values
   - Thus attention is a sum of values weighted by K-Q match is returned over the V's

![K,Q,V Intuition](/img/kqv_intuition.png)

This setup allows us to create a paradigm of:
- **Queries (Q)**:
   - Represents the word being attended to / compared to
   - Used to calculate attention scores with all Keys
- **Key (K)**:
   - Represents all other words (context words) being compared to the Query
   - Used to compute the relevance of each context word to the Query
- **Value (V)**:
   - Another representation of the context words, but separate and different from Keys
      - Although the same input context words are multiplied by 2 different K, V matrices, which results in 2 different Key and Value vectors for same context word
   - It basically is a representation of each "word" so at the end, a scored `SUM()` of all words is over values!
   - Weighted by the attention scores to produce the final output

These matrices are learned during training and updated via backpropagation

#### K Q V Complexities
In [Bahdanau Attention - each decoder is compared to all encoder states](#bahdanau-attention-time-complexities)

In Transformer self-attention, we ***compare all tokens to all tokens simultaneously***

$$QK^T \text{ with shape } (S \times d_k) \cdot (d_k \times S) = S \times S$$

Which is now a quadratic term, which is where GPU behavior gets interesting

### Tokenization
Tokenization is actually a fairly large part that gets looked over for Transformers - authors and creators of most models have utilized ***Sub-Word Tokenization*** to reduce overall vocabulary size and ensure out-of-vocabulary tokens are handled well. Instead of replcaing with `[UNK]` or something else, splitting up the entire vocabulary into different character chunks allows for reusability between `##ing` for `dining` and `banking`

***Byte Pair Encoding*** is also utilized as a compression technique which iteratively replaces the most frequent pair of bytes in a sequence with a single, unused byte. Instead of merging together frequent pairs of bbytes, the tokenization algorithms will merge together characters or sub-word character sequences that are frequent. That's how the model learns to pull out `##ing` as a sub-word, because it's quite frequent!

#### Training
This model needs actual training to be done on it to learn these frequency word pairings. The algorithm needs to build merge tables and vocabulary of tokens that ultimately will be updated across epochs to create an optimized set of sub-words to tokenize in the future

Training here isn't really on probabilistic modeling, it's actually a greedy approach based on heuristics and counts in the data, but ***a new tokenizer would be needed for an inherently unique document set***. Doctor shorthand wouldn't be tokenized properly compared to APA structured student essays

The initial vocabulary consists of characters and an empty merge table, at this exact intro step each word is segmented as a sequence of characters, and then the algorithm below is continuously ran:
- Count pairs of symbols - how many times does each pair occur together in the training data
- Find the most frequent pair of symbols
- Merge that pair together in the merge table, and add the new token to the vocabulary

The main parameter to set is the maximum number of merges desired in output merge table, as it ensures you don't over-do merging and lose out on information

![Building Merge Table GIF](/img/build_merge_table.gif)

The above shows how a vocabulary of cats, mats, mate, ate, etc get turned into merged words separated by the `@@` symbols which represent concatenation. In most tokenizers today the separator is `##`

#### Inferece
After learning BPE rules, the merge table is the main artifact output that is reused across inference. The algorithm will segment new words into sequence of characters, and after that iteratively runs over the word running below steps until no other merge is possible:
- Among all possible merges, find highest in merge table
- Run that merge
- Stop if no new merge is able to be found

So inference is just constantly replacing merges over time, and hypothetically could replace an entire word with a compressed single token in some cases

### Encoding Blocks
Once we have tokenized inputs relating to some sort of static embedding, we focus on encoding 

The main layer you focus on in our Encoding blocks is Self Attention, but alongside this there are other linear layers that help to stabilize our context creation

#### Self Attention
Self Attention allows words in a single sentence / document to attend to each other to update word embeddings in itself. It's most commonly used when you want a sentence's word embeddings to be updated by other words in the same sentence, but there's nothing stopping us from using it over an entire document.

It was born out of the example of desiring a different embedding outcome of the word bank in:
- The river bank was dirty
- I went to the bank to deposit money

Via Self Attention, the word "bank" in the two sentences above would be different, because the other words in the sentence "attended to" it

Self Attention is a mechanism that uses context words (**Keys**) to update the embedding of a current word (**Query**). It allows embeddings to dynamically adjust based on their surrounding context.

Lastly, there are still limitations to Attention, and Attention is not "all you need" at the end of the day!
- It is simply a weighted average, so non-linearities are impossible without further non-linear activation functions inside of neural net
- Bidirectionality may not always be desired (this is covered more in [Masked Self Attention](#masked-self-attention))
- Self Attention by itself does not keep word position, and so it's essentially a bag-of-words once again

All of the above are solved via the Transformer Architecture itself outside of Self Attention! This is why transformer encoder and decoder architecture consists of multiple layers of self attention with a feed forward network and positional encodings!
- Residual connections pass "raw" embeddings directly through next layers which helps to prevent forgetting or misrepresenting information
- Layer normalization helps to relieve parameters of given layer shifting because of layers beneath it
   - This ultimately reduces uninformative variation and normalizes each layer to mean zero and standard deviation of one
- Scaling down the dot product helps to stop the dot product from taking on extreme, unbounded values because of this variance scaling

Consider the phrase "fluffy blue creature." The embedding for "creature" is updated by attending to "fluffy" and "blue," which contribute the most to its contextual meaning

![Fluffy Blue Attention](/img/fluffy_blue_creature.png)

[Self Attentions Complexity](#single-head-self-attention-complexities) is dominated by the $S$ sequence length term, and results in $\approx O(S^2)$ because all tokens attend to all other tokens in the sequence

#### How Self Attention Works
- The Query vector $Q_i$ represents the current word
- The Key vector is an embedding representing every other word $K_j \forall  \left\{j \neq i\right\} $
    - Multiply the Query by every Key to find out how "similar", or "attended to" each Query should be by each Key $Q_i \cdot K_j$
- Then you softmax it to find the percentage each Key should have on the Query
- Finally you multiply that softmaxed representation by the Value vector, which is the input embedding multipled by Value matrix, and ultimately allow each Key context word to attend to our Query by some percentage
- At the end, you sum together all of the resulting value vectors, and ***this resulting SUM of weighted value vectors is our attended to output embedding***

- In the below example:
   - The dark blue vector from the left is the Query
   - The light blue vector on top are the Keys
   - you multiple them together + softmax
   - Multiply the result of that by each Value vector on the bottom

![SelfAttention](/img/self_attention.png)

In depth mathematical explanation below

1. Input Transformation:
   - Each input embedding $ x_i $ is transformed into three vectors: **Query (Q)**, **Key (K)**, and **Value (V)**
   - These are computed by multiplying the input embedding with learned weight matrices:
     $
     q_i = x_i \cdot W_Q, \quad k_i = x_i \cdot W_K, \quad v_i = x_i \cdot W_V
     $
![QKV](/img/qkv.png)
2. Self-Attention Calculation:
   - Compute attention scores by taking the dot product of the Query vector $ q_i $ with all Key vectors $ k_j $:
     $
     \text{Score}_{ij} = q_i \cdot k_j
     $
   - Scale the scores to prevent large values:
     $
     \text{Scaled Score}_{ij} = \frac{\text{Score}_{ij}}{\sqrt{d_k}}
     $
    - Where $ d_k $ is the dimensionality of the Key vectors
    - As the size of the input embedding grows, so does the average size of the dot product that produces the weights 
        - Remember dot product is a scalar value
        - Grows by a factor of $\sqrt{d_k}$ where $k$ = num dimensions
        - Therefore, you can counteract this by normalizing is via $\sqrt{d_k}$ as the denominator
   - Apply softmax to convert scores into probabilities:
     $
     \text{Attention Weight}_{ij} = \text{softmax}(\text{Scaled Score}_{ij})
     $
   - Compute the weighted sum of Value vectors:
     $
     Z_i = \sum_j \text{Attention Weight}_{ij} \cdot V_j
     $
![Attention Calc](/img/attention_calc.png)
3. Output
   - The output $ Z_i $ is a context-aware representation of the token $ i $, influenced by its relationship with other words in the sequence

#### Single Head Self Attention Complexities
RNN's were sequential over $S$, but they only had an $O(d^2)$ compute cost per step. Each decoder hidden state would multiply itself by every encoder hidden state, which was size $T_x$, roughly relating to $S$. So the ***path length***, referring to the number of sequential steps, was $O(S)$, and at each step there was $O(d^2)$ work done

In self-attention, the path length is reduced to $O(1)$ as all of the comparisons are done in parallel, there's nothing sequential! However, at each step (there's only 1 large matrix step) there's $O(S^2)$ work done as we multiply every query by all keys

- RNN:
   - Path length $O(S)$
   - Compute per step $O(d^2)$
- Self attention:
   - Path length $O(1)$
   - Compute per step $O(S^2)$

Overall, single head time complexity will resolve to
$$O(Sd^2 + S^2d)$$

So when
- Sequence length dominates projection size $S \gg d$, the quadratic $S^2$ term dominatesd
- When the projection size dominates sequence length $d \gg S$, the projection term dominates

Storage is usually the ultimate bottleneck in processing, and the memory complexity of a single head is
$$O(S^2)$$

##### Single Head Projection Complexities
Each token
$$x_i \in \real^d$$

Is multiplied by projection matrices
$$W_Q, W_K, W_V \in \real^{d \times d}$$

The total cost per projection, defined as all inputs in sequence of size $d$ multiplied by a single matrix of size $d$, is
$$O(S \cdot d^2)$$

Since there are 3 matrices total
$$O(3S \cdot d^2) \approx O(S \cdot d^2)$$

##### Single Head Attention Score Complexities
First we need to compare all queries to keys
$$QK^T$$

- $Q \in \real ^{S \times d_k}$
- $K \in \real ^{S \times d_k}$
- So $QK$ is $(S \times d_k)(d_k \times S)$
   - Second one transposed

So the $QK$ operation has time complexity
$$O(S^2d_k)$$

After that, we softmax over the $S^2$ matrix
$$O(S^2)$$ 

And finally perform weighted value aggregation $W_{ij} \cdot V_j$, which is $(S \times S)(S \times d_k)$
$$O(S^2 d_k)$$

Therefore, the entirety of a single-headed self attention time complexity is
$$O(Sd^2 + S^2d_k)$$

Where we assume $d_k = d / h$ and $d_k \approx d$

The ***path length*** is still $O(1)$ because all tokens attend to each other in parallel

#### Single Head Memory Complexities
The attention matrix itself is an $S \times S$ matrix, and so memory ultimately is 
$$O(S^2)$$

This is often the true bottleneck in most transformer architectures when $S$ becomes large (this is the ***large context length problem***). Attention is often memory bound at large $S$ due to O(S^2)$ attention matrix, even if compute utilization appears high

The bottleneck is:
- Storing $S \times S$ attention matrix
- Moving it through HBM
- Reading and writing intermediate tensors

This becomes critical for optimizing later on with things like:
- FlashAttention
- KV Caching
- etc

For example, long-context models begin to show signs of degredation when their GPU utilization is $\gt$ 90% but their FLOPS are stagnant at an unoptimal place like $\approx$ 50%. At this point the GPU is busy working through memory buffers and bringing data into main memory, and it's not able to truly run things in parallel.

### Multi-Head Attention
- Instead of using a single set of $ Q, K, V $, Multi-Head Attention uses multiple sets to capture different types of relationships between words (e.g., syntactic vs. semantic).
- Each head computes its own attention output.
   - Outputs from all heads are concatenated and passed through a final weight matrix $ W_O $:
     $
     Z = \text{Concat}(O^{(head_1)}, O^{(head_2)}, \dots) \cdot W_O
     $
![Multi Headed Attention](/img/multi_attn.png)

#### Multi Head Complexity
Single head was
$$O(Sd^2 + S^2d)$$

With $h$ heads, we now have $h \cdot O(S^2 d_k)$ for each head becuase $hd_k = d$

Therefore, multi-head attention has the same time complexities as single headed

#### Pruning
There's an entire section in some Transformer papers talking about pruning of heads. Ultiamtely this is because not every head is needed, and some generally won't have any useful features in some datasets

Pruning allows the model to run faster, perform less computations, and potentially do this without any loss of quality! Most of the time it's a pruning + speed / accuracy tradeoff where you can prune up to certain elbow thresholds where the return on pruning starts to decrease compared to decrease on accuracy

The model needs to be trained with all possible heads being updated, but afterwards pruning is a typical optimization step for production models

### Other Layers
Other layers outside of attention based layers in transformers help to extend the problems to a wider set of real world scenario's:
- Non-linearity (feed forward + residual layers)
- Gradient issues (Normalization)
- Distribution shift (normalization, skip layers)
- etc..

Below blurb helps to showcase some of the reasons why all of these layers and architectures are added into the "attention only" architectures (i.e. attention isn't all you need, and below explains why)

<div style={{
  margin: "2em auto",
  maxWidth: 600,
  background: "#f5f7fa",
  borderLeft: "4px solid #4f8cff",
  padding: "1.5em 2em",
  borderRadius: 8,
  textAlign: "left"
}}>
  <em>
One of them is to pass the "raw" embeddings directly to the next layer, which prevents forgetting or misrepresent important information as it is passed through many layers. This process is called residual connections and is also believed to smoothen the loss landscape. Additionally, it is problematic to train the parameters of a given layer when its inputs keep shifting because of layers beneath. Reducing uninformative variation by normalizing within each layer to mean zero and standard deviation to one weakens this effect. Another challenge is caused by the dot product tending to take on extreme values because of the variance scaling with increasing dimensionality $d_k$. It is solved by Scaled Dot Product Attention, which consists of computing the dot products of the query with its keys, dividing them by the dimension of keys, and applying the softmax function next to receive the weights of the values.

Attention learns where to search for relevant information. Surely, attending to different types of information in a sentence at once delivers even more promising results. To implement this, the idea is to have multiple attention heads per layer. While one attention head might learn to attend to tense information, another might learn to attend to relevant topics. s
  </em>
</div>

![Freehand Transformer Arch](/img/freehand_transformer_arch.png)


#### Positional Encoding

- Since Self Attention does not inherently consider word order, **Positional Encoding** is added to input embeddings to encode word positions
- Positional encodings are vectors added to each input embedding, allowing the model to distinguish between words based on their positions in the sequence
- **Why is ***sinusoidal*** relevant and useful?**
   - Allows Transformer to learn relative positions via linear functions (e.g., $\text PE_{pos+k}$​ can be derived from $\text PE_{pos}$)
   - you all know neural nets like linear functions! So it's helpful in ensuring a relationship that's understandable 
![Positional Encoding](/img/positional_encoding.png)

#### Residual Connections and Normalization

- Each encoder layer includes a **residual connection** and **normalization layers** to stabilize training and improve gradient flow
- This happens after both Self Attention Layer and Feed Forward Layer in the "Add and Normalize" bubble
- Add the residual (the original input for that sublayer) to the output of the sublayer
   - In the case of Self Attention layer, you add the output of Self Attention to the original input word (non-attended to word)
- Apply LayerNorm to the result
   - This just means normalize all actual numeric values over the words embedding
- **If the diagram shows a block over the whole sentence, it just means the operation is applied to all words, but always independently for each word
- **Why is any of this useful**:
   - Helps with gradient vanishing and exploding, and also ensures input stability

![Self Attention Encoding](/img/summary_self_attention_encoding.png)

#### Summary of Self Attention Encoding

1. **Input Embedings**:
   - you take our input words, process them, and retrieve static embeddings
   - This only happens in the first encoding layer

2. **Positional Encoding**:
   - Add positional information to embeddings to account for word order

3. **Self Attention**:
   3.1 **Input Transformation**:
      - Positionally encoded embeddings are transformed into $ Q, K, V $ using learned weight matrices.

   3.2 **Self Attention Calculation**:
      - Compute attention scores using dot products of $ Q $ and $ K $, scale them, and apply softmax.

   3.3 **Weighted Sum**:
      - Use the attention weights to compute a weighted sum of $ V $, and add that onto the input word, producing the output.

   3.4 **Residual + Normalization**:
      - [LayerNorm](/docs/training_and_learning/LAYER_NORM.md#layer-normalization) add together input and self-attended to matrices

   3.5 **Feed Forward Layer**:
      - Each position’s output from the self-attention layer is passed through a fully connected feed-forward neural network (the same network is applied independently to each position)
      - Essentially just gives model another chance to find and model more transformations / features, while also potentially allowing different dimensionalities to be stacked together
         - If you have 10 words in our input, you want to ensure the final output is the same dimensionality as the input
         - I don't know if this is exactly necessary

4 **Multi-Head Attention**:
   - Use multiple sets of $ Q, K, V $ to capture diverse relationships, then concatenate the results.

This diagram below shows one single encoding block using Self Attention

![Self Attention Encoding](/img/summary_self_attention_encoding.png)

#### Masked Self Attention
- In Masked Self Attention, it's the same process as Self Attention except you mask a certain number of words so that the $ Q \cdot K $ results in 0 effectively removing it from attention scoring
    - In BERT training you mask a number of words inside of the sentence
    - In GPT2 training you mask all future words (right hand of sentence from any word)
   
![Masked Self Attention](/img/masked_self_attention.png)

#### Context Size and Scaling Challenges

- The size of the $ Q \cdot K $ matrix grows quadratically with the context size ($ n^2 $), making it computationally expensive for long sequences.
- To address this, masking is used to prevent future words from influencing current words during training (e.g., in autoregressive tasks).
- Context size
    - Size of Q * K matrix at the end is the square of the context size, since you need to use all of the Q * K vectors, and…it’s a matrix! So it’s n*n = n^2 so it’s very hard to scale
    - It does help that you mask ½ the examples because you don’t want future words to alter our current word and have it cheat
        - Since for an entire sentence during training for each word you try to predict the next, so if there are 5 words there’s 1, 2, 3, 4, 5 training examples and not just 1
        - Don’t want 4 and 5 to interfere with training 1, 2, 3
 
### Encoder-Decoder Attention

Encoder-Decoder Attention is a mechanism used in **Seq2Seq tasks** (e.g., translation, summarization) to transform an input sequence into an output sequence. It combines **Self Attention** within the encoder and decoder blocks each, and then **cross-attention** between the encoder and decoder

![Encoder To Decoder Summary](/img/encoder_to_decoder.png)

#### Encoder

**Encoder**:
- The Encoder Portion is completely described in [Summary of Self Attention Encoding](#summary-of-self-attention-encoding)
- TLDR;
   - The encoder processes the input sequence and generates a sequence of **hidden states** that represent the context of the input
   - Each encoder block consists of:
      - **Input Embedding**:
         - *The first encoding layer* typically uses positional encoding + static embeddings from Word2Vec or GLoVE
      - **Self Attention Layer**:
         - Allows each token in the input sequence to attend to other tokens in the sequence
         - This captures relationships between tokens in the input
         - **Feed Forward Layer**:
            - Applies a fully connected feed-forward network to each token independently
            - Typically two linear transformations with a ReLU/GeLU in between: `FFN(x) = max(0, xW₁ + b₁)W₂ + b₂`
      - **Residual Connection + LayerNorm**
         - Add input / output of layer, and then normalize across vector
   - The output of each encoder block is passed to the next encoder block as input, and the final encoder block produces the **contextual embeddings** for the entire input sequence
      - These are further transformed into K, V contextual output embeddings
   - This confused me at first, but basically the output of an encoder block is same dimensionality as word embedding input, so it can flow through
   - This is usually known as `d_model`
- This allows us to stack encoder blocks arbitrarily
- Architecture:
   - Composed of multiple identical blocks (e.g., 6 blocks by default, but this is a hyperparameter)
   - Each block contains:
     - Self Attention Layer: Captures relationships within the input sequence
     - Feed Forward Layer: Processes each token independently
    - ![Encoder Block](/img/summary_self_attention_encoding.png)

##### Encoder Complexity
Encoder complexities here are the same as [self attention complexity](#single-head-self-attention-complexities)

$$O(Sd^2 + S^2 d)$$

It's based on the $S$ sequence length, and projection dimensions $d$

#### Decoder
![Encoder to Decoder Summary](/img/encoder_to_decoder.png)

Parameters:
- $S$ = encoder length
- $T$ = decoder length
- $d$ = model dimension
- $h$ = # of heads
- $d_k = d / h$

So inside of the masked self attention layer:
- $Q_{\text{dec}} \in \real^{T \times d_k}$
- $K_{\text{dec}} \in \real^{T \times d_k}$
- $V_{\text{dec}} \in \real^{T \times d_k}$

Inside cross-attention layer:
- $Q_{\text{cross}} \in \real^{T \times d_k}$
- $K_{\text{enc}} \in \real^{S \times d_k}$
- $V_{\text{enc}} \in \real^{S \times d_k}$


The decoder generates the output sequence one token at a time, using both the encoder's output and its own previous outputs. Each encoder, and specifically the last one, outputs a hidden state matrix $H \in \real^{S \times d}$ that's the size of the sequence $S$ and the projected attended to embeddings (i.e. for each input in $S$, we have a vector of size $d$). Afterwards, each decoder block will apply masked self-attention over the encoder input and the previous decoder outputs, which allows it to auto-regressively focus on it's past output words to predict the next word

- Input:
   - The ***contextual embeddings*** output from the final Encoding Layer
      - These K, V contextual output embeddings are passed to each Decoder block
      - For cross-attention, the decoder applies it's own learned $W_K, W_V$ to that encoder output
      - ***Keys and Values are re-projected in each decoder layer***
   - The previous Decoder block(s) output (previously generated word)
- Each decoder block consists of:
   - Masked Self Attention Layer:
      - Allows each token in the output sequence to attend to previously generated tokens in the sequence (auto-regressive behavior)
      - Future tokens are masked to prevent the model from "cheating" by looking ahead
      - So self-attention only happens from words on the left, not all Keys
      - Query: Current token's embedding
         - For the first layer this is the embedding $E x_i$ from our actual input 
         - For deeper decoder layers, this is from the decoders previous output
      - Key and Values: All already generated words to the left
      - Similar to self-attention except you ignore all to the right
   - Encoder-Decoder Attention Layer:
      - Attends to the encoder's output (contextual embeddings) to incorporate information from the input sequence
      - Query: Comes from the decoder's self-attention output
      - i.e. it's the decoder's current representation of a token after masked self-attention
      - Key and Values: Encoder's output for each input token
   - Feed Forward Layer:
      - Applies a fully connected feed-forward network to each token independently
- Architecture:
    - Composed of multiple identical blocks (e.g., 6 blocks by default).
    - Each block contains:
        - Self Attention Layer: Captures relationships within the output sequence
        - Encoder-Decoder Attention Layer: Incorporates information from the encoder's output
        - Feed Forward Layer: Processes each token independently
- Example:
   - Input sentence has 5 words in total
      - Remember, the encoder put out 5 total vectors, one for each input word
   - Let's walk through the third word in the decoder output, meaning the first two have already been generated
   - Decoder Self Attention
      - Input: The embeddings for the first, second, and third generated tokens so far
         - The query is the input embedding (same one fed to encoder) for the 3rd word
         - K,V are the input embedding (same one fed to encoder) for the 1st and 2nd words so far
      - Masking: The self-attention is masked so the third position can only "see" the first, second, and third tokens (not future tokens)
      - What happens: The third token attends to itself and all previous tokens (but not future ones), using their embeddings as keys and values
   - Encoder Decoder Cross Attention
      - Input: The output of the decoder’s self-attention for the third token (now a context-aware vector), and the encoder’s output for all input tokens
      - Q, K, V:
         - The query is the third word's attended to vector (after self-attention and residual/LayerNorm in decoder)
         - The keys and values are the encoder’s output vectors for each input token (these are fixed for the whole output sequence)
      - What happens The third token’s representation attends to all positions in the input sequence, using the encoder’s outputs as keys and values  
3. Final Decoder Output:
   - The final decoder layer produces a vector of floats for each token, which is passed through:
     - A linear layer to expand the vector to the vocabulary size
     - A softmax layer to produce a probability distribution over the vocabulary for the next token

##### Decoder Complexity
The decoder is more complicated than the encoder!

$T$ is the current decoders output so far, and so at each decoder step we utilize these previous outputs and relate them to the input sequence $S$, and the current output $T$

###### Decoder Training
The decoder has 2 attention blocks:
- Masked self-attention $O(T^2 d)$
- Cross-attention $O(TSd)$

So the total per decoder layer comes to
$$O(T^2 d + TSd + Td^2)$$

In this section the sequence length $S \approx T$ is roughly equivalent to the decoder sentence length. So in total, the time complexity per decoder step is dominated by the sequence size
$$O(T^2d)$$

###### Decoder Inference
For long-context LLM inference, $T$ will grow auto-regressively while it has to continue keeping the full sequence in memory

Masked Self-Attention will reduce to $O(Td)$ per token if utilizing ***KV Caching***, which is a GPU inference optimization method

Cross attention per token then becomes $O(Sd)$

So the total per generated token is
$$O((T+S)d)$$

#### Visual Representation

1. **Encoder Block**:
   - Self Attention → Feed Forward → Output to next encoder block.

2. **Decoder Block**:
   - Self Attention → Encoder-Decoder Attention → Feed Forward → Output to next decoder block.

3. **Final Decoder Output**:
   - The final decoder output is passed through a linear layer and softmax to produce the next token.
![Encoder Decoder Step](/img/encoder_decoder_step.png)

#### Summary of Encoder-Decoder Attention

1. **Encoder**:
   - Processes the input sequence and generates contextual embeddings using self-attention.

2. **Decoder**:
   - Generates the output sequence token by token using:
     - Self Attention: Captures relationships within the output sequence.
     - Encoder-Decoder Attention: Incorporates information from the input sequence.
     - Auto-Regressive Decoder: Tokens are predicted auto-regressively, meaning words can only condition on leftward context while generating

3. **Final Output**:
   - The decoder's output is passed through a linear layer and softmax to produce the next token.

4. **Training**:
   - The model is trained using [cross-entropy loss](/docs/training_and_learning/LOSS_FUNCTIONS.md#cross-entropy) and [KL divergence](/docs/training_and_learning/LOSS_FUNCTIONS.md#kl-divergence), with each token in the output sequence contributing to the loss.
![EncoderDecoder Output](/img/encoder_decoder_output.png)

### Transformer Optimizations
There's a number of optimizations in this architecture that a lot of production systems use to speed up inference, saturate GPU utilization, and reduce overall size and runtime of the models after training has been completed
- [Pruning](#pruning) was already covered where you remove some of the heads in multi-head attention, and this can be done after training with an evaluation set to see if a majority of variance is covered in distinct heads (removing heads 1 and 4 in a set of 12)
- [KV Caching](#kv-caching) is an inference only optimization that caches the results from $KV$ multiplication during the auto-regressive phase in decoding inference, ultimately allowing to skip all historic $KV$ calculations for already output words for all future words
- Quantization reduces the overall precision of the data types from `float32` to lesser numbers like `float16` or `float8`. The rationale is that during training the extra precision helps with gradient stability, accuracy, and convergence - especially since we are multiplying thousands of numbers in such small ranges (potentially all between `[0.00, 1.00]`) the extra precision helps to ensure there's no loss of information. Once training is done, and the numbers have converged to allow for latent features, some architectures are able to reduce these data points total size and keep a majority of features and variance preserved  
   - Mixed Precision Training is another "flavor" of this where you use lower precision for most computations while keeping critical parameters as higher precision
- Gradient Clipping caps the gradient to prevent exploding gradients during training - most transformers try and tackle this with residual layer, normalization layer, identity layers, dropouts, etc and gradient clipping is another common tool if gradients start to explode
- [Sparse Attention](#sparse-attention) reduces the quadratic complexity of self-attention by attending to only a subset of tokens 
   - Go from $O(n^2)$ comparisons to $O(n \cdot k)$ where $k$ is the length of the subset of tokens we are performing self-attention on
   - Architectures will use local tokens, stored global tokens, random sampling, sliding windows, and skip-token self-attention layers to reduce memory and hopefully preserve context needed for self-attention variance
- [Flash Attention](#flash-attention) implements memory-efficient attention by computing attention in chunks to reduce memory overhead instead of putting the entire $O(n^2)$ matrix into memory. Should ultimately help GPU utilization and reduce memory bottlenecks for sequences because the context doesn't grow with generation
   - Similar to [Sparse Attention](#sparse-attention) where you focus on a local context of tokens

#### KV Caching
KV Caching comes up in a lot of areas, and interviews, especially around "The GPU is at 90% utilization, but it's FLOPS utilization is stagnant around 30%, what is the first potential cause of this?" where you should dive into memory overheads on GPU's and try and see if there's redundant memory bottlnecks on a GPU that's causing too much shuffle and not allowing SIMD operations to run. One way to alleviate this issue is with KV Caching, where you reuse a number of the $KV$ operations computed in the auto-regressive decoder inference portion of LLM modeling

As a sentence moves forward, the input is `[prompt]`, and over time more and more output words are computed - `[prompt] + y_1`,  `[prompt] + y_1 + y_2`, ... so on. Each of the new output tokens `y_1, y_2` will continuously be involved in both cross-attention and self-attention $KV$ operations, and so during this phase we can cache these results over each inference period in GPU cache and reuse them until we are complete with a round of inference

![KV Cache](/img/kv_cache.png)

This will utilize GPU Buffers, which are essentially dedicated blocks of memory used for storing WORM based vectors - sometimes they are write-once, other times they can be overwritten, but typically in caching you don't want to be continuously writing to them. If they aren't present, simply store them on the fly and continue

<!-- Collapsible Python snippet -->
<details>
  <summary>Show Python Script</summary>

```python
def forward(self, x, use_cache=False):
    b, num_tokens, d_in = x.shape
​
    keys_new = self.W_key(x)  # Shape: (b, num_tokens, d_out)
    values_new = self.W_value(x)
    queries = self.W_query(x)
    #...
​
    if use_cache:
        if self.cache_k is None:
            self.cache_k, self.cache_v = keys_new, values_new
        else:
            self.cache_k = torch.cat([self.cache_k, keys_new], dim=1)
            self.cache_v = torch.cat([self.cache_v, values_new], dim=1)
        keys, values = self.cache_k, self.cache_v
    else:
        keys, values = keys_new, values_new
```

</details>

#### Sparse Attention
TODO:

#### Flash Attention
TODO:

## Vision Transformers (ViT)
In using transformers for vision, the overall architecture is largely the same - flattening structure out and using augmention for new examples and then doing self-supervised "fill in the blank" for training

All changes are relatively minor:
- ***Input***:
   - *Text*: Input is a sequence of tokens
   - *Vision*: Input is an image split into fixed size patches `16x16` 
      - Each patch gets flattened and linearly projected to form a "patch embedding" similar to static word embeddings
      - `[CLS]` token used for classification tasks
- ***Positional Encoding***:
   - *Text*: Added to token embeddings to encode word order
   - *Vision*: Added to patch embeddings to encode spatial information of each patch in the image
- ***Objective***:
   - *Text*: Predict the next word (causal), fill in the blank, or generate a sequence (translation / summarization)
   - *Vision*: Usually image classification, or can also be segmentation, detection, or masked patch prediction (fill in the blank) 
- ***Architecture***: Basically the same without any major overhauls
- ***Self Supervision***:
   - *Text*: Fill in the blank, next sentence prediction
   - *Vision*: Fill in the blank (patch), or pixel reconstruction which aims to recreate the original image from corrupted or downsampled versions