---
layout: technical
title: Bayesian Learning
category: Probability and Statistics
difficulty: Advanced
description: Discussions around Bayesian(s)
show_back_link: true
---

## Bayesian vs Frequentist
Bayesian vs Frequentist - the main difference is in interpreting "probability" and uncertainty

### Frequentist Approach
In Frequentist, AKA classical stats, the probability is simply the long run frequency of things

It's the rate of event over rate of seen (among many frequent trials)

$ P(Event) \over P(All)$

***Characteristics***:
- Parameters, $\theta$, are fixed and unknown
- Data is random, and uncertainty strictly stems from sampling variability
    - i.e. we choose data randomly in samples, so any uncertainty is simply because we're randomly choosing data points
- There are no *prior beliefs*; We only know what we know from what we see
- Hypothesis testing is done via *p-values* and *confidence intervals*
    - ***p-values*** are a way to interpret a hypothesis that was decided on before
        - Something similar to "we believe these two groups of patients are significantly different after one takes a drug and one doesn't"
        - For p-values you must ***assume the null hypothesis is true***, and then the p-value tells you the probability of seeing that observed data $O$
        - The p-value is the probability of observing data as extreme as (or more extreme than) what you saw, given the null hypothesis
        - Therefore $P(O | \theta) = p$ is the likelihood of the observed data under the assumed parameters
            - So if the p-value is small, that means the probability of observing that data is small, and that we can reject the null hypothesis
            - If it's large we do not accept the null, but we fail to reject it

***Example***:
- Testing a new drug, and wanting to check it's effectiveness
- Null hypothesis: There is no effect (no statistical significance between observed and population)
    - Alternative hypothesis: There is statistical significance (doesn't specify direction or cause)
- Observed data: $O$
- P-Value: `0.035`, with threshold `0.05`
    - The threshold and significance values measure how close a hypothesis is to a dataset
    - To be clearest - it actually means "The threshold (significance level, e.g., 0.05) is the cutoff for how unlikely the observed data must be under the null hypothesis before we reject it."
        - This just means we choose some level of unlikeliness, and if the observed data is under that level of unlikeliness then we can reject null
        - This means the higher the significance, the more "wiggle room" we're giving
- Test: typically done with `t-test`, or some other one of the hundreds of different tests
    - Each test is valid only under certain conditions of population and observed datasets
    - Get p-value from these tests
- At this point the p-value is less than the threshold, and so you can reject the null

### Bayesian Approach
In Bayesian statistics there's a ***degree of belief, and unknown*** in all of the probability calculations

This belief can be updated when new data comes in, and is constantly changing

***Characteristics***:
- All parameters, $\theta$ are treated as ***random variables*** with ***prior distributions***
    - Prior distributions are *our belief of knowledge of a parameter before observing any data*
    - It's a distribution that allows us to express uncertainty about the parameter of interest
    - It's typically known as $P(\theta)$ where $\theta$ is the specific parameter of interest, for this we'll denote it as $\theta_{i}$
- These parameters, with their uncertain prior distributions, are updated as new data comes in
- [Bayes Theorem](#bayes-theorem) allows us to update the parameters prior beliefs with new data, resulting in ***posterior distributions***
- Inference at the end is based on the probability of hypothesis, not accepting or rejecting
    - Here we can say "there's a 95% chance the treatment effect is > 0"

***Example***:
- Testing a new drug, and wanting to check it's effectiveness
- Start with a prior that the drug has a small effect
    - How do you choose a prior? It's the subjcet of large debate
        - [Duke Stats 732 Paper on Choosing Priors](https://www2.stat.duke.edu/courses/Spring13/sta732.01/priors.pdf)
        - ***Subjective Priors*** are priors based on *subjective* beliefs, typically we try to do this in lens of an "expert"
        - ***Default / Low-Informative / Uniform*** prior is an alternative that reflects a lack of strong and precisely quantified prior information
            - AKA ***Objective Prior***, because we try to base this on non-subjective information of one person
    - Without diving too far into this, basically, you choose some prior
- After running trial(s) and observing data, you update your belief to get the posterior
    - You must run a large number of trials to update the posterior closer and closer to it's true value
    - If you only run one experiment, then it may not be that close to the true value
    - The expected difference from your outcome to the true value is known as ...?
- Finally, with this outcome, you can use your parameters and observed data to directly answer the effects question

### Bayesian
Now we can discuss how Bayesian is used in ML and Analytics

The intuitive description is that we can update parameters that we created in / update parameters while running, our backpropogation algorithms

Ultimately, if we have an online system that runs $f(\theta, U_i) = \theta \cdot U_i$ of running these matrix parameters against a user input, we can update these parameters after seeing new data (feedback loop) of the user - this is the essence of ***Bayesian Updating***

#### Bayes Theorem
$P(\theta \mid O) = { {P(O \mid \theta) \cdot P(\theta)} \over P(O)}$

- Parameters $\theta$
- Observed Data $O$
- $P(\theta)$: prior belief about parameters
- $P(O \mid \theta) \cdot P(\theta)$: likelihood (how likely the data is given parameters)
- $P(\theta \mid O)$: posterior (updated belief after seeing data)