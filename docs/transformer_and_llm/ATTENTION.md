---
layout: technical
title: Attention
category: NLP, CV, and Transformers
difficulty: Advanced
description: Discussions around the Attention mechanism in NLP, CV, and Transformers
show_back_link: true
---

## Attention
Attention is what separates static embeddings from dynamic embeddings - they allow word embeddings to be updated, aka attended to, by the contextual words surrounding them

Attention stemmed from NLP Seq2Seq Tasks like next word prediction, and translation where using the surrounding context of the word was one of the major breakthroughs in achieving better Seq2Seq results. Attention helps to fix the **bottleneck problem** in [RNN encoder (and RNN encoder-decoder) models](/docs/transformer_and_llm/EMBEDDINGS.md#encoder-decoder) - Due to their design, the encoding of the source sentence is a single vector representation $C$ (context vector). The problem is that this state must compress all information about the source sentence in a single vector and this is commonly referred to as the bottleneck problem. There was a desire to not "squish" everything into one single context vector, and instead to utilize the input embeddings dynamically when decoding, and to utilize the context on the fly - this is known as *align and translate jointly*

![Align and Translate Jointly](/img/align_and_translate_jointly.png)

The embedding for "bank" *is always the same embedding in the metric space* in static scenario's like [Word2Vec](/docs/transformer_and_llm/EMBEDDINGS.md#word2vec), but by attending to it with Attention, you can change it's position! It's as simple as that, so at the end of attending to the vector, the vector for bank in river bank may point in a completely different direction than the vector for bank in bank vault - just because of how the other words add or detract from it geometrically in its metric space. Bank + having river in sentence moves vector in matrix space closer to a sand dune, where Bank + teller in sentence moves it closer to a financial worker

How is this done? Attention mechanisms in our DNN models. There are multiple forms of Attention - most useful / used are Self Attention, Encoder-Decoder Attention, and Masked Self Attention - each of them help to attend to a current query word / position based on it's surroundings. A single head of this Attention mechanism would only update certain "relationships", or attended to geometric shifts, but mutliple different Attention mechanisms might be able to learn a dynamic range of relationships

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

It is differentiable, and its gradient never vanishes! These are very desirable properties

![Attention Image](/img/attention_image.png)

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
      - This will take the current input word, and the output of the last recurrence
      - These are bi-directional
         - $\overrightarrow{h_2} = f(x_2, h_1)$
         - $\overleftarrow{h_2} = f(x_2, h_3)$
         - $h_2 = [\overrightarrow{h_2} \frown \overleftarrow{h_2}]$
            - Concatenation!
      - It is formalized that $h_t \in \mathbb{R^{d_h}}$ is the hidden state of the encoder at time $t$
         - $d_h$ is the dimensionality of our encoder hidden state
- These $h_i = [\overrightarrow{h_i} \frown \overleftarrow{h_i}] \space \forall i \in [1, . . ., T_x]$ 
   - They live entirely in the encoder block
   - They are fixed once the input is encoded

![RNN Encoder GIF](/img/RNNEncoderSetup.gif)

#### Decoder RNN Attention
Decoder is often trained to predict the next word $\hat{y_t}$ given the context vector $c$ and all the previously predicted words $\{\hat{y_1}, ..., \hat{y_{t-1}} \}$

Our translation can be defined as $\bold{y} = (y_1, ... y_{T_n})$ which is just the sequence of words output so far!

It does this by defining a probability distribution over the translation output word $\bold{y}$ by decomposing the joint probability. 

$p(\bold{y}) = \prod_{t=1}^{T} p(y_t \mid \{y_1, \ldots, y_{t-1}\}, c)$

*Since our $\bold{y}$ is just our entire word sequence, the probability we're solving for is "the probability that this is the sequence of words given our context vector"*

So we're just choosing the next most likely word so that the probability of seeing all these words in a sequence is highest

The sequence "Hi, what's your", if you looked over all potential next words, would most likely have the highest predicted outcome of "Hi, what's your name"

Each of these conditional probabilities is typically modeled with a non-linear function $g$ such that 

So, ***at each time step $t$*** the decoder combines:
- ***Decoder hidden state formula***: $s_t = f(s_{t-1}, y_{t-1}, c_t) \in \mathbb{R^{d_s}}$  based on
   - $s_{t-1}$ the last hidden state
      - Dimension $d_s$
   - $y_{t-1}$ the last output word
   - $c_t$ the context at that state
      - $c_t = \sum_{i=1}^{T_x} \alpha_{ti}h_i$
      - Where $\alpha_{ti}$ is the weight of $h_t$ compared to each annotation $h_i$ and is a similarity metric between the two


#### Learning To Align And Translate
The rest of the architecture proposes using a bi-directional RNN as an encoder, and then a decoder that emulates searching the source sentence during translation

The "searching" is done by comparing the decoders last hidden state $\bold{s}_{t-1}$ to each encoder hidden state $h_i \space \forall i \in [1,...,T_x]$ in our alignment model, and then creating a distribution of weights (softmax) to create a context vector. This context vector, the previous hidden state, and the previous hidden word help us to compute the next word!

**P.S. the alignment model here is very similar to self-attention in the future

Since sentences aren't exactly isomoprhic (one-to-one and onto), there may be 2 words squished into 1, 1 word expanded to 2, or 2 non-adjacent words that are used in outputting 1 

***Realistically, any Seq2Seq task that isn't isomorphic would benefit from this structure***

#### Summary
- ***Encoder***
   - $h_i \in \mathbb{R^{d_h}}$ is the encoder hidden state / annotations
      - $\overrightarrow{h_2} = f(x_2, h_1)$
      - $\overleftarrow{h_2} = f(x_2, h_3)$
      - $h_2 = [\overrightarrow{h_2} \frown \overleftarrow{h_2}]$ 
         - Concatenation!  
- ***Decoder***
   - For each step $t$, you need to come up with a context vector $\bold{c}_t$
   - $e_{ti} = a(s_{t-1}, h_i)$ is an alignment model which scores similarities between decoder hidden state at $t-1$ and all encoder states, where each one is denoted at some time $i$
      - $a(\cdot)$ is a small feed-forward NN
      - $e_{ti} = {\bold{v}^T} \cdot \tanh({W_s} \bold{s}_{t-1} + {W_h}{\bold{h}_i})$
         - $W_s \in \mathbb{R^{d_a \times d_s}}$
         - $W_h \in \mathbb{R^{d_a \times d_h}}$
         - $\bold{v} \in \mathbb{R^{d_a}}$
         - What does this mean?
            - ${W_s} \bold{s}_{t-1}$ is a weighted version of our decoder hidden state at $t-1$
            - ${W_h}{\bold{h}_i}$ is a weighted version of our encoder hidden state at time $i$
            - Therefore, $\tanh(\cdot) \in [-1, 1]$ acts as an activation function which helps us to score how close the decoder hidden state at $t-1$ and our current encoder hidden state at $i$ are
   - Normalize with softmax to get attention weights $\alpha_{ti} = \frac{\exp(e_{ti})}{\sum_{k=1}^{T_x} \exp(e_{tk})}$
      - $e_{tk}$ will be the attention score of $t$ to all other states
         - If there are 5 words in the input, and we're at $t = 3$, this will score how well $s_2$ is to $h_3$ compared to all other annotations $h_{[1, 2, 4, 5]}$
         - Another blog mentioned how attention scores $e_t$ are computed by "scalarly combining the hidden states of the decoder with all of the hidden states of the encoder"
            - $e_t = [({h_d}^t)\cdot{h_e}^1, ... , ({h_d}^t)\cdot{h_e}^N]$
      - This will convert scores into a probability distribution
      - Since our attention model helps to compute scores across encoder hidden states to a decoder hidden state, taking the softmax here will then give us the ***relative weight of each encoder hidden state to a decoder hidden state***
   - Form the context vector, AKA attention output, $\bold{c}_t$ as the weighted sum of these annotations
      - $\bold{c}_t = \sum_{i=1}^{T_x} \alpha_{ti} \cdot h_i$
         - Where $\alpha_{ti}$ is the weight of $h_t$ compared to each annotation $h_i$ and is a similarity metric between the two
   - $s_t = f(s_{t-1}, y_{t-1}, c_t) \in \mathbb{R^{d_s}}$ is the decoder hidden state
      - $y_{t-1}$ is the last output word from decoder
   - To bring it all out:
      - $s_t = f(s_{t-1}, y_{t-1}, \sum_{i=1}^{T_x} (\frac{\exp(a(s_{t-1}, h_i))}{\sum_{k=1}^{T_x} \exp(a(s_{t-1}, h_k))}) \cdot h_i$ )
         - Our query is $s_{t-1}$, and our keys / values are $h_i$
         - Our attention score is based on $\alpha_{ti} = \frac{\exp(e_{ti})}{\sum_{k=1}^{T_x} \exp(e_{tk})}$ which is multiplied by $h_i$ to attend to it
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

## Transformer Attention
The above RNN discussion is useful, as it shows how you can utilize the building blocks of forward and backwards passes, and even achieve attention mechnisms using basic building blocks

***RNN's are linear, and therefore have trouble with parallel processing and fully utilizing GPU's - Transformers aimed to make this alignment fully parallelized***

RNN's also fail with long term dependencies - the sentence "he was near the large stadium with Sarah and was named Cam", you would need to keep track of every word between "he" and "Cam" to have the word "he" have any sort of effect on Cam. A direct consequence of this is the inability to train in parallel on GPU's because future hidden states cannot be computed in full before past hidden states have completed.

Attention also helps to alleviate the bottleneck problem, where all context is "shoved" into a singular vector. Attention allows all encoded infromation to help influence the context and decoding during each step, and helps to alleviate the vanishing gradient problem from long sentences that end up multiplying multiple numbers $\lt$ 1.0 throughout numerous steps. 

Attention does no more than weighted averaging, and so without neural network layer functions it's strictly weighted averaging. Transformers help change this and add in non-linear layers. That's why transformer architectures eventually use multiple layers of self-attention (parallelized), with non-linear and other activation layers (feed forward, residual connections, etc), and potential future masking strategies. All of these different choices help to ensure transformers tackle a vast set of NLP problems

The rest of the discussion is around Attention blocks in Transformer Architectures, primarily using a similar encoder-decoder structure "on steroids"

![Even Better Transformer Diagram](/img/better_transformer_arch_diagram.png)

### Key, Query, and Value Matrices
Self-Attention and K,Q,V go hand in hand - the intuition for K,Q,V can be seen from an approximate hash table:
- To lookup a value, queries are compared against keys in a table
- In the Hash Table below, there's exactly one K:V pair for any Q
   - In contrast for self attention, each K is matched to varying degrees to each Q
   - Thus a sum of values weighted by K-Q match is returned over the V's

![K,Q,V Intuition](/img/kqv_intuition.png)

This setup allows us to create a paradigm of:
- **Queries (Q)**:
   - Represents the word being attended to / comapred to
   - Used to calculate attention scores with all Keys
- **Key (K)**:
   - Represents the context words being compared to the Query
   - Used to compute the relevance of each context word to the Query
- **Value (V)**:
   - Another representation of the context words, but separate and different from Keys
      - Although the same input context words are multiplied by 2 different K, V matrices, which results in 2 different Key and Value vectors for same context word
   - It basically is a representation of each "word" so at the end, a scored `SUM()` of all words is over values!
   - Weighted by the attention scores to produce the final output

These matrices are learned during training and updated via backpropagation

### Encoding Blocks
The main layer you focus on in our Encoding blocks is Self Attention, but alongside this there are other linear layers that help to stabilize our context creation

#### Self Attention
Self Attention allows words in a single sentence / document to attend to each other to update word embeddings in itself. It's most commonly used when you want a sentence's word embeddings to be updated by other words in the same sentence, but there's nothing stopping us from using it over an entire document.

Self attention also achieves context / word interaction comparisons in $O(1)$ instead of $O(n)$ like recurrence / RNN's would - this is a significant achievement which allows for:
- Parallel processing of corpora
   - To be specific, all word representations per layer can be computed in parallel
- Bidirectional comparisons
- $O(1)$ maximum interaction distance (direct calculation)

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

#### How Self Attention Works
TLDR;
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

1. **Input Transformation**:
   - Each input embedding $ x_i $ is transformed into three vectors: **Query (Q)**, **Key (K)**, and **Value (V)**
   - These are computed by multiplying the input embedding with learned weight matrices:
     $
     q_i = x_i \cdot W_Q, \quad k_i = x_i \cdot W_K, \quad v_i = x_i \cdot W_V
     $
![QKV](/img/qkv.png)
2. **Self-Attention Calculation**:
   - **Step 1**: Compute attention scores by taking the dot product of the Query vector $ q_i $ with all Key vectors $ k_j $:
     $
     \text{Score}_{ij} = q_i \cdot k_j
     $
   - **Step 2**: Scale the scores to prevent large values:
     $
     \text{Scaled Score}_{ij} = \frac{\text{Score}_{ij}}{\sqrt{d_k}}
     $
    - Where $ d_k $ is the dimensionality of the Key vectors
    - As the size of the input embedding grows, so does the average size of the dot product that produces the weights 
        - Remember dot product is a scalar value
        - Grows by a factor of $\sqrt{d_k}$ where k = num dimensions
        - Therefore, you can counteract this by normalizing is via $\sqrt{d_k}$ as the denominator 
   - **Step 3**: Apply softmax to convert scores into probabilities:
     $
     \text{Attention Weight}_{ij} = \text{softmax}(\text{Scaled Score}_{ij})
     $
   - **Step 4**: Compute the weighted sum of Value vectors:
     $
     Z_i = \sum_j \text{Attention Weight}_{ij} \cdot V_j
     $
![Attention Calc](/img/attention_calc.png)
3. **Output**:
   - The output $ Z_i $ is a context-aware representation of the word $ i $, influenced by its relationship with other words in the sequence.


### Multi-Head Attention
- Instead of using a single set of $ Q, K, V $, Multi-Head Attention uses multiple sets to capture different types of relationships between words (e.g., syntactic vs. semantic).
- Each head computes its own attention output.
   - Outputs from all heads are concatenated and passed through a final weight matrix $ W_O $:
     $
     Z = \text{Concat}(O^{(head_1)}, O^{(head_2)}, \dots) \cdot W_O
     $
![Multi Headed Attention](/img/multi_attn.png)

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

___ 
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

#### How Encoder-Decoder Attention Works

![Encoder To Decoder Summary](/img/encoder_to_decoder.png)

1. **Encoder**:
   - The Encoder Portion is completely described by what you wrote above in [Summary of Self Attention Encoding](#summary-of-self-attention-encoding)
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
- **Architecture**:
   - Composed of multiple identical blocks (e.g., 6 blocks by default, but this is a hyperparameter)
   - Each block contains:
     - **Self Attention Layer**: Captures relationships within the input sequence
     - **Feed Forward Layer**: Processes each token independently
    - ![Encoder Block](/img/summary_self_attention_encoding.png)


2. **Decoder**:
![Encoder to Decoder Summary](/img/encoder_to_decoder.png)
   - The decoder generates the output sequence one token at a time, using both the encoder's output and its own previous outputs
   - **Input**:
      - The ***contextual embeddings*** output from the final Encoding Layer
         - These K, V contextual output embeddings are passed to each Decoder block
      - The previous Decoder block(s) output (previously generated word)
   - Each decoder block consists of:
     - **Masked Self Attention Layer**:
       - Allows each token in the output sequence to attend to previously generated tokens in the sequence (auto-regressive behavior)
       - Future tokens are masked to prevent the model from "cheating" by looking ahead
       - So self-attention only happens from words on the left, not all Keys
       - ***Query***: Current token's embedding
       - **Key** and **Values**: All already generated words to the left
         - Similar to self-attention except you ignore all to the right
     - **Encoder-Decoder Attention Layer**:
       - Attends to the encoder's output (contextual embeddings) to incorporate information from the input sequence
       - **Query**: Comes from the decoder's self-attention output
         - i.e. it's the decoder's current representation of a token after masked self-attention
       - **Key** and **Values**: Encoder's output for each input token
     - **Feed Forward Layer**:
       - Applies a fully connected feed-forward network to each token independently
- **Architecture**:
    - Composed of multiple identical blocks (e.g., 6 blocks by default).
    - Each block contains:
        - **Self Attention Layer**: Captures relationships within the output sequence
        - **Encoder-Decoder Attention Layer**: Incorporates information from the encoder's output
        - **Feed Forward Layer**: Processes each token independently
- **Example**:
   - Input sentence has 5 words in total
      - Remember, the encoder put out 5 total vectors, one for each input word
   - Let's walk through the third word in the decoder output, meaning the first two have already been generated
   - ***Decoder Self Attention***
      - **Input**: The embeddings for the first, second, and third generated tokens so far
         - The query is the input embedding (same one fed to encoder) for the 3rd word
         - K,V are the input embedding (same one fed to encoder) for the 1st and 2nd words so far
      - **Masking**: The self-attention is masked so the third position can only "see" the first, second, and third tokens (not future tokens)
      - **What happens**: The third token attends to itself and all previous tokens (but not future ones), using their embeddings as keys and values
   - ***Encoder Decoder Cross Attention***
      - **Input**: The output of the decoder’s self-attention for the third token (now a context-aware vector), and the encoder’s output for all input tokens
      - **Q, K, V**:
         - The query is the third word's attended to vector (after self-attention and residual/LayerNorm in decoder)
         - The keys and values are the encoder’s output vectors for each input token (these are fixed for the whole output sequence)
      - **What happens**: The third token’s representation attends to all positions in the input sequence, using the encoder’s outputs as keys and values  
3. **Final Decoder Output**:
   - The final decoder layer produces a vector of floats for each token, which is passed through:
     - A **linear layer** to expand the vector to the vocabulary size
     - A **softmax layer** to produce a probability distribution over the vocabulary for the next token

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