---
layout: technical
title: GPT(s)
category: NLP, CV, and Transformers
difficulty: Advanced
description: Discussions around GPT LLMs
show_back_link: true
---

## GPTs
The GPT models are a decoder only (no cross encoder-decoder attention, no encoder hidden states) [transformers](/docs/transformer_and_llm/TRANSFORMERS.md). Their use in language modeling was created from the same overall desires of [BERT](/docs/transformer_and_llm/BERT.md) and Transformers, where we want to use "web scale" data in an unsupervised fashion to gain an edge over supervised tasks that require curated datasets
- [GPT 1 - Improving Language Understanding by Generative Pre-Training](/arxiv_papers/GPT1.pdf) introduced the idea of *generative pre-training* followed by *discriminative fine-tuning*. Unsupervised pre-training is used for general language modeling, similar to the pre-training desires in BERT, however only a decoder is used. Afterwards, the model is then saved and utilized for supervised fine tuning tasks, and those tasks need to be altered to fit into the pre-training generative architecture
    - Classification is simply "generate a single word text description of the input"
    - Named Entity Recognition is simply "generate a CSV list of named entities in the input"
    - Similarity is outputting two results and comparing their similarity (this is still weird)
    - etc
- [GPT 2 - Language Models are Unsupervised Multitask Learners](/arxiv_papers/GPT2.pdf) is mostly a larger extension of GPT 1, and furthers the idea of unsupervised learning taking over. It does this by essentially throwing out the downstream supervised fine tuning, and hypothesizing "all downstream fine tuning tasks can be modeled as next token generative output with enough data". In doing so, **zero-shot** prompting emerges where we give the model some example in the prompt for it to output the correct sequence
    - "zero-shot task performance emerged from simply conditioning the language model with text, reducing the need for task-specific fine-tuning"
- [GPT 3]

These families introduced training and alignment objectives to further the zero-shot abilities. Web scale data is great, but the actual structure of generative output needed some structure
- [Instruct GPT](/arxiv_papers/IntstructGPT.pdf) 


GPT models are ***decoder only***, meaning they immediately start to output text in an auto-regressive fashion after receiving input. This input (prompt, sentence, etc) still goes through GPT during inference in the same format - it runs multi-headed self attention over the inputs (which it sees as auto-regressive even though it's not) to ultimately produce an output. ***The only major difference in the supervised fine tuning tasks is the auto-regressive output may be singular!***

![GPT, BERT, and Others](/img/gpt_bert_others.png)

![BERT vs GPT](/img/bert_vs_gpt.png)


### GPT 1
GPT 1 was modeled as a modified [decoder only transformer](/docs/transformer_and_llm/TRANSFORMERS.md#decoder). If the input to a GPT is of size $T_y$, it needs to run multi headed, and multi layered, self attention over these inputs, along with the typical residual blocks, layer norm, dropouts layers, etc. After this is done, there is a softmax function at the end to predict the next word $\hat{y} \in V$ from the vocabulary set

#### Unsupervised Pre Training
During unsupervised training, this will continuously run as an auto-regressive unsupervised modeling framework. Similar to BERT it has a context window of size $k$, but it only uses the self-attention parts of a decoder to output words until it predicts an `[EOS]` token and then stops. Loss during this is predicted over each predicted output, simply as a language model does!

$$ L_{1}(U) = \sum_{i} \text{log} P(u_{i} | u_{i - k}, u_{i - k - 1}, ..., u_{i - 1}; \theta)$$

$k$ is the context window, and the conditional probability $P$ is modeled with some parameters $\theta$, updated via backpropogation over the many decoder only layers. The general architecture utilizes parameters:
- $k$ is context size
- $d$ the general size of vectors in the embedding matrix $E$, and the hidden state vector sizes
- $U = (u_{-k}, ..., u_{-1})$ is the context vector of tokens, each being $u_i \in \real^{d}$
- $W_e$ is the token embedding matrix, producing vectors of size $d$
- $W_p$ is the position embedding matrix


$$h_{0} = UW_e + W_p$$
$$h_{l} = \text{transformer block}(h_{l-1}) \forall i \in [1, n]$$
$$P(u) = \text{softmax}(h_{n} W_{e}^T)$$

The end result from softmax is basically choosing a vector from the token embedding matrix $W_e$

This will train a generalized language model over web scale data!

#### Supervised Fine Tuning
This is generally the "meat" of the paper, *which hypothesizes that the final layer $h_l$ can simply be fed into an additional linear output layer with a new parameter set $W_y$ to predict a label $y$*

This is important because it generalizes a labeled dataset $C$ with:
- Sequence of input tokens $x^1, ..., x^m$
- A label $y$

The above is an extremely vague dataset! This is on purpose, and is the desired feature of this model. Even if $y$ is not in our token embedding matrix $W_e$, we only need to ensure the new parameter set $W_y$ includes it, along with all of the seen vocabulary words from unsupervised pre-training. 

$$P(y | x^1, x^2, ..., x^m) = \text{softmax}(h_m W_y)$$

Which leads to a loss over all the generated outputs $y$ that make up the actual required output label. The *softmax at the end produces a distribution over the task specific outputs $W_y$*

$$ L_{2}(c) = \sum_{(x, y)} P(y | x^1, x^2, ..., x^m)$$

The authors also include language modeling as an auxilary objective, outside of just predicting the output sequence $y$

$$L_{3}(C) = L_{2}(C) + \lambda \cdot L_{1}(C)$$

#### The Meat of GPT 1
***We can use the unsupervised pre-trained language model to produce $h_m$ without any changes to it!*** All we have to do is create a new mapping / output parameter set $W_y$, and we can use the underlying language model to predict any sequence of output tokens. Even if the correct output is multiple values long, we can generate any sequence of outputs given the generative nature! 

This is where "classification is only outputting a single word" and "named entity recognition is just outputting a CSV list of named entities" - since the objective is just to output a sequence of tokens, GPT 1 can generalize to a humongous set of fine-tuning tasks

***The only extra parameters we require during fine tuning are $W_y$***

Some online documents mention supervised fine tuning only creates a singular classification style output, others mention is allows for generative sequence creation, and the loss $L_{2}$ is the same as $L_{1}$ over all of the predicted tokens in the sequence, but ultimately who cares. The major meat is that the unsupervised pre-training allows for many downstream tasks!

#### Task Specific Transformations
Modeling the tasks to just be sequence outputs required some tweaking, but it's very easy to see. Hell, even regression can be considered an output if it just produced a string representing "12.4"!

![GPT Supervised Fine Tuning Tasks](/img/gpt_supervised_fine_tuning_tasks.png)

The harder to notice portion is representing the input and outputs appropriately:
- Text classification is simple, you just output a single class (maybe multiple words)
- Question Answering means structuring the input as a question, and the output as a sentence answer
- Textual Entailment (using a set of defined rules to reason) means we need a triplet of `(inputs, documents, answers)` where the documents are used in reasoning

The actual creation of all of these for each task was a large body of work described in the papers

### GPT 2
GPT 2 TLDR is very simple:
- Beef up unsupervised pre-training. More parameters, larger model, more data
- Remove task-specific supervised fine tuning, and frame downstream tasks as textual conditioning + completion with zero shot prompting
    - Essentially, similar to entailment, you give the input a set of rules / structure of output and it can use that information to predict an output sequence
    - This output sequence + zero shot prompting gets rid of anything task specific! ***The task itself is specified through the prompt / context rather than a specific head***


It is nice that the GPT models mostly just get bigger. More power. And otherwise just become more generic by saying "what is a task? It's just a sequence" and modeling almost every possible task into a sequence with a nice loss function. The loss function is important, because the loss of summarization is slightly different than the loss for named entity recognition - summarization loss is actually quite hard to pin down, and NER has a set of values you could use cross-entropy loss in a classical setting. That being said, **GPT 2 only does the unsupervised pre-training** portion, so it's loss is still just:

$$ L_{1}(U) = \sum_{i} \text{log} P(u_{i} | u_{i - k}, u_{i - k - 1}, ..., u_{i - 1}; \theta)$$

#### GPT 2 Validation and Experiments
Most GPT 2 experiments utilize language modeling datasets, and so summarization, question answering, etc are all easy to validate with simple loss functions. They actually made their life much easier in terms of dropping the task specific heads and just generalizing to the language modeling loss

GPT 2 experiments include:
- Translation - BLEU score
- Question answering - Exact match
- Summarization - ROUGE
- Reading comprehension - Exact match / related metrics
- etc

Therefore, GPT 2 just needs to output the sequence in the same way it would during unsupervised pre-training, and all of these datasets have validation metrics to utilize to compare the output sequence to the desired one. *Zero shot means during these experiments / validations, no weights are updated!*

#### New Definitions and Vocabulary
In GPT 2 a few new vocabulary words come out:

Zero shot means without any parameter or architecture modification. It's just useful to explain *models don't have to update parameters*
- Each of the downstream "tasks" is now zero-shot meaning they send in a set of instructions in the input, and there's no update to parameters needed

The conditional probabilities utilized in GPT 1 for generating the next word now go beyond just the input sequence $\bold{x} = (x^1, x^2, ..., x^m)$

$$P(y | \bold{x}) \text{ turns into } P(y | \bold{x} ; \text{task})$$

[*Byte Pair Encoding*](/docs/transformer_and_llm/TRANSFORMERS.md#tokenization) is used to reduce the total size of the vocabulary and embedding matrix $W_e$. Because our output is a generic sequence, we don't have to store "read", "reading", "reader", "creep", "creeping", and "creeper" - we can just store "read", "creep", "##ing", and "##er". It even goes a bit further to split words based on common middle parts too, but ultimately ***this allows any output sequence to be modeled at a sequence of common bytes*** which drastically reduces the memory of the models vocabulary and lookup times
