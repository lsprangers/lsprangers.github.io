---
layout: technical
title: Contrastive Learning
category: Training and Learning (ML)
difficulty: Advanced
description: Discussions around Contrastive Learning in LLMs
show_back_link: true
---

## Contrastive Learning
An approach to extract meaningful representations by contrasting positive and negative pairs of instances

Similar instances should be closer in a learned embedding space - if it's framed as a discrimination task then constrastive learning allows models to capture relevant latent features and similarities in data

Supervised, and Self-Supervised
- **Supervised** is easy, you have labeled data and you can explicitly train a model to differentiate between similar and dissimilar instances
    - Training on pairs of data points, and a label describing similarity 
    - Objective is to learn an embedding space where similar instances are clustered closer together
    - [***Information Noise Contrastive Estimate (InfoNCE)***](/docs/training_and_learning/LOSS_FUNCTIONS.md#infonce-loss) Loss Function is a popular method for achieving this
        - This loss function maximizes the agreement between positive samples, and minimizes the agreement between negative samples
- **Self-Supervised** aims to do the same thing as the supervised counterpart, except there are no explicit labels of similar and dissimilar
    - In these scenarios, tricks have to be used to create similar and dissimilar pairs
        - These "tricks" are known as ***pre-text tasks***, and they're chosen carefully because they will create different embedding spaces with their outcomes
        - *Augmented views* involves creating multiple augmented versions of the same instance and treating those as positive pairs, and treating other instances / augmented views of those instances, as negative
            - This has been shown to capture higher level semantic information and generalizes well to downstream tasks
            - Allows for a similar style as [BERT](/docs/transformer_and_llm/BERT.md) where we train a generic model and fine tune it later on

## Self Supervised
Going into self-supervised methods, focusing on data augmentation and transformations along with model architectures helps to bring everything together

Use Cases:
- *NLP*: We can use sentence similarity, word masking, next word prediction, or any sort of augmented sentence
- *Images*: We can use cropping, flipping, color distortion, etc

Popular Frameworks:
- *SlimCLR*
- *MoCo*
- *SwAV*
- *Barlow Twins*

### Data Augmentation
Data augmentation involves applying various transformations and pertubations on unlabeled data to create new, unique, instances and augmentations of input data

Helps to expose model to different perspectives of the same instance. Some common ones are cropping, flipping, rotations, random crop, and color transformations

![Common Augmentations](/img/common_augmentations.png)

### Architecture
Architecture is going to be similar to an Encoder Only Transformer model, similar to [BERT](/docs/transformer_and_llm/BERT.md) which relies on components like [Attention in Encoders](/docs/transformer_and_llm/ATTENTION.md#encoding-blocks) and others to alter then input into a latent representation space

#### Encoder Network
After Data Augmentation the step would be training an encoder network 

The encoder network is typically a DNN architecture, such as a CNN for images or RNN for sequential data (text, images, time series, etc). This network's goal is then to encode high level representations from the augmented instances, which allows us to discriminate between similar and dissimilar in the future

#### Projection Network
The projection network helps us to refine the latent representation space, and typically will ***map this into a lower-dimensional embedding space***

I typically group together Encoder Network with Projection Network, since most of the pieces in [Transformers](/docs/transformer_and_llm/index.md) do this all in one go

### Training and Evaluation
Training and evaluation will focus on picking correct loss functions, and then utilizing the final model in downstream tasks like classification, detection, and segmentation

#### Learning Objective
Once input samples are projected into a lower-dimensional embedding space, we can start using the Contrastive Learning Objective itself

Maximize agreement between positive samples, minimize agreement between negative samples! Similarity can simply be Euclidean or Cosine depending on normalization of vectors

#### Loss Functions
Choice of loss function depends on specific task requirements and data characteristics. Each loss function aims to facilitate learning representations that capture meaningful similarities

So what loss functions are useful in the initial Contrastive Learning model?
- *Contrastive Loss*: Is a fundamental loss function which, as stated before, simply aims to maximize agreement between positive pairs and minimize agreement between negative
    - Typically defined as a margin-based loss, where similarity between instances is measured using a distance metric like Euclidean or Cosine
- [***Information Noise Contrastive Estimate (InfoNCE)***](/docs/training_and_learning/LOSS_FUNCTIONS.md#infonce-loss) is described elsewhere
- *Triplet Loss* aims to preserve relative distances between instances in the learned embedding space
    - In this you form triplets of instances: `[negative, anchor, positive]`
    - From this you want to ensure $(anchor - positive) \lt (anchor - negative)$ by some specified margin
- *N-Pair Loss* extends Triplet Loss to consider multiple positive and negative samples for a given anchor
- *Logistic / Cross-Entropy* where we formalize the probability distributions as "the probability that the two positive instances belong to the same class, or different classes"

#### Evaluation and Generalization
Similar to BERT, we'd extend this base model with multiple different layers on top for different purposes which is known as [Transfer Learning](/docs/transformer_and_llm/BERT.md#extending-base-models)

The ultimate measure of success in this scenario is the performance on these downstream tasks - otherwise it's all useless!

Evaluation on downstream tasks can be done using appropriate metrics like accuracy, precision, recall, F1 Score, or nuanced task-specific metrics

A higher score on these downstream tasks indicates better generalizartions and usefulness of learned representations

## Contrastive vs Cross Entropy
Contrastive learning is a framework / paradigm on creating embeddings by comparing positives to negatives, and it can have any type of loss function

Cross Entropy in language modeling is a bit nuanced, in the fact that the only positive it considers is the true next token defined in the text, in the sentence "the quick brown fox" the only acceptable positive is "jumped" - all other tokens are implicitly negatives

In Contrastive Learning, the negatives are explicitly sampled, and are typically other instances in the dataset, but they're not implied to be every other example. The objective function is still a softmax function over examples, but the interpretation is different

The interpretation difference is language modeling treats “everything except the ground truth token” as negatives, whereas contrastive setups construct positives/negatives from augmentations or paired data