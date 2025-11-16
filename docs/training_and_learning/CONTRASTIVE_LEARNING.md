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
            - Allows for a similar style as [BERT](/docs/transformer_and_llm/BERT.md) where you train a generic model and fine tune it later on

## Self Supervised
Going into self-supervised methods, focusing on data augmentation and transformations along with model architectures helps to bring everything together

Use Cases:
- *NLP*: you can use sentence similarity, word masking, next word prediction, or any sort of augmented sentence
- *Images*: you can use cropping, flipping, color distortion, etc

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
Once input samples are projected into a lower-dimensional embedding space, you can start using the Contrastive Learning Objective itself

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
- *Logistic / Cross-Entropy* where you formalize the probability distributions as "the probability that the two positive instances belong to the same class, or different classes"

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

## Images
This section was copied from the [Resnets - Contrastive Learning in Image Modality](/docs/transformer_and_llm/RESNETS.md#contrastive-learning) that discusses how Contrastive Learning is used in ResNets

**SlimCLR** was one of the first, and most known, contrastive learning frameworks - it's simple, highly accurate, well researched, and heavily utilized. The main idea is to have two copies of a single image, and use these to train two networks that are compared. A major con is that it doubls the overall storage size of the underlying dataset, but BLOB storage is cheap (in my opinion). **Boostrap Your Own Latent** was introduced to avoid making the double sized dataset. 

### Contrastive Learning Framework
Contrastive loss is used to learn a representation by maximizing the agreement between various augmented views of the same data example. To achieve this, there are 4 significant components:
- A stochastic data augmentation module to create new augmentations of input
- A neural network base encoder to take inputs, and augmentations, and will encode into dense vector
- A small neural network projection head to take encoded vectors into projection space
- A contrastive loss function that allows comparisons between projected vectors

![Contrastive Arch](/img/contrastive_arch.png)

#### Stochastic Data Augmentation
A minibatch of $N$ examples is sampled randomly, and thee contrastive prediction task is defined on pairs of augmented examples - this results in $2N$ data points altogether

A memory bank isn't needed, as the training batch size varies from 256 to 8,192. Any given data example randomly returns two correlated views of the same example, denoted as $\bar{x_i}$ and $\bar{x_j}$ which is known as the **positive pair**. The **negative pair** are all other $2(N-1)$ pairs. It's been shown that choosing different data augmentation techniques can reduce the complexity of previous contrastive learning frameworks. Some of the common ones are:
- *Spatial geometric transformations* like cropping, resizing, roration, and cutouts
- *Appearance transformations* like color distortion, brightness, contrast, saturation, Gaussian blur, or Sorbel filtering

Models tend to improve after composing augmentaitons together too, instead of only applying one single one

#### Neural Network Base Encoder
The NN Base Encoder $f(\cdot)$ extracts multiple representation vectors from the augmented data examples - the commonly used ResNet was picked and gives $h_i = f(\bar{x_i}) = \text{ResNet}(\bar{x_i})$ where $\bold{h_i} \in \real^d$ is the output after the average pooling layer. 

#### Small Neural Network Projection Head
A small neural network projection head $g(\cdot)$ maps the representation to the space where the contrastive loss is applied. The importance of this layer was evaluated with:
- Identity mapping
- Linear projection
- Default non-linear projection with an additional hidden layer and ReLU activation

The results showed the non-linear projection is better than linear, and both are much better than no transformation (identity)

They've used an MLP with one hidden layer to obtain $z_i = g(\bold{h_i}) = W^2 \sigma(W^1(\bold{h_i}))$ where $\sigma$ is a ReLU non-linear transformation

This is useful because defining the contrastive loss on $z_i$ instead of $\bold{h_i}$ wouldn't lead to a loss of information caused by contrastive loss, and is shown to maintain and form more information

#### Contrastive Loss Function
Given a set $\{{\bar{x}_{ik}}\}$ including a positive pair of examples $\bar{x_i}$ and $\bar{x_j}$, the contrastive prediction task aims to idntify $\bar{x_i}$ in $\{{\bar{x}_{i}}\}_{k \neq i}$ for a given $\bar{x_i}$. In the case of positive esxamples, the loss function is defined as 

$\ell_{i,j} = -\log \frac{\exp\left(\frac{\mathrm{sim}(z_i, z_j)}{\tau}\right)}{\sum_{k=1}^{2N} \mathbb{I}[k \neq i] \exp\left(\frac{\mathrm{sim}(z_i, z_k)}{\tau}\right)}$

Where:

- $(\ell_{i,j})$ is the loss for the pair $(i, j)$
- $\mathrm{sim}(z_i, z_j)$ is the similarity between $z_i$ and $z_j$
    - Typically $\mathrm{sim}(u, v) = \frac{u^\top v}{|u| , |v|}$ is a dot product between $l_2$ and normalized $\bold{u}, \bold{v}$
- $\tau$ is the temperature parameter
- $\mathbb{I}[k \neq i]$ is the indicator function (1 if $(k \neq i)$, 0 otherwise)

The final loss is calculated across all positive pairs, both $(i, j)$ and $(j, i)$ in a mini-batch

This above was named **NT-Xent** as Normalized Temperature-scaled Cross Entropy. This was compared against other commonly used contrastive loss functions like logistic loss and margin loss, and NT-Xent outperformed with proper hyperparameter tuning

### SlimCLR Framework
The ultimate goal of this framework was to describe a better approach to learning visual representations without human supervision. 

SlimCLR outperforms previous work, is more straightforward, and does not require a memory banks

Significant components of the framework:
- A constrastive prediction task requires combining multiple data augmentation operations, which results in effective representations
    - Unsupervised contrastive learning benefits from more significant data augmentation
    - In english, this means applying lots of different random changes (like cropping, flipping, rotating, color changes, etc) to images. The model is trained to recognize that these different augmentations are "the same"
- The quality of learned representations can be substantially improved by introducing a learnable non-linear transformation between the representation and contrastive loss
    - Basically this means you encourage the model to make the representations (feature vectors) of different augmented views of the same image similar, while making representations of different images dissimilar
    - Contrastive loss will penalize the model if the two feature vectors of the same augmented image are far apart, and rewards them if they're similar
        - Common contrastive loss example is *NT-Xent* (Normalized Temperature-scaled Cross Entropy) loss 
- Representation learning with cross-entropy loss can be improved by normalizing embeddings and adjusting the temperature parameter appropriately
    - **Temperature** is a parameter in the contrastive loss function that controls how sharply the model distinguishes between similar and dissimilar pairs
        - A lower temperature makes the model focus more on making positive pairs very close, and negative very far apart
        - A higher temperature smooths out the differences, making the model less strict about separating pairs
    - Therefore, this equates to saying that adjusting the temperature to balance how hard the model pushes similar images together can improve the quality of the learned representations
- Contrastive learning benefits from larger batch size and extended training periods compared to supervised counterpart
    - Larger batch size helps because it allows the model to compare more positives and negatives for each sample
    - Each batch is used to create positive and negative pairs, so the more examples inside of it the more comparisons!

