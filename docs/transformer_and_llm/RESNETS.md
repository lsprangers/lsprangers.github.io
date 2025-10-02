---
layout: technical
title: ResNets
category: NLP, CV, and Transformers
difficulty: Advanced
description: Discussions around GPT LLMs
show_back_link: true
---

## ResNets
ResNets were presented as an answer to "can stacking more layers enable the network to learn better" - the obstacle up to that point was vanishing / ***exploding gradients***, and they were primarily solved for by ***normalized initialization and intermediate normalization layers*** which enabled networks with tens of layers to start converging for [stochastic gradient descent](/docs/training_and_learning/TRAINING_OPTIMIZATIONS.md#stochastic-gradient-descent-sgd) with backprop. Degredation also proved to be an issue, where as network depth increased there was a saturation, and then rapid decrease, in accuracy. Adding more layers to a suitably deep model led to higher training error, and overfitting was not caused by this degredation. A shallower architecture was suggested, and using auxiliary layers consisting of identity mappings and others shallow model layers, but in practice this didn't help. Later on Deep Residual Learning took the charge.

### ResNet Theory / Background
### ResNet Architecture

## Deep Residual Learning
Deep Residual Learning is useful in the ResNet sense because it allows very deep networks to be trained by reformulating the layers as learning residual functions with reference to the layer inputs, rather than directly learning unreferenced functions. This helps address the vanishing gradient problem and enables effective training of much deeper architectures

There was a huge issue of exploding / vanishing gradients, along with overall degredation of accuracy in these models, that were solved by utilizing normalization layers and residuals - ResNets usage of residual skip conncetions specifically addresses the degredation problems

The degredation problem ultimately motivated the usage of residual learning 
- In theory, if you add more layers to a NN the network should be able to at least match the performance of a shallower network, simply by learning the identity function
    - i.e. the extra layers don't actually do anything
- In practice, deep networks often perform worse (measured by a higher training error) as more layers were added - this is the ***degredation problem***
- The reason for this problem is that it's surprisingly hard for standard (non-residual) deep networks to learn the identity mapping using many non-linear layers. Ultimately the optimization process just can't find this solution
- Residual learning re-formulates the problem
    - Instead of learning $H(x)$, some full mapping 
    - It aims to learn the residual $F(x) = H(x) - x$ 
    - So $H(x) = F(x) + x$
- Why?
    - If the best thing for the extra layers to do is nothing (identity function of shallow network), the residual $F(x)$ can just go to zero, which is easier for an optimizer to find
    - If the optimal function is not an identity function, it's often closer to identity thatn zero, so learning a small "perturbation" from identity is easier for the optimization to learn instead of doing it from scratch
        - If the optimal function starts to converge to a non-zero solution, then the middle mapping layers can be considered worthwhile, as they add some sort of new information
- Altogether, Residual connections make it easier for deep networks to learn functions that are closer to identity mappings, which help to avoid the degredation problem and make optimization easier

This entire thought process created the problem statement for residual learning frameworks / layers inside deep NN's. 

### Residual Learning
The idea of residual learning is to replace the approximation of an underlying latent mapping $H(x)$, which is approximated by a few stacked layers, with an approximation of residual functions $F(x) := H(x) - x$ where $x$ denotes the inputs to the first of these few stacked layers - therefore $ H(x) \approx F(x) + x$