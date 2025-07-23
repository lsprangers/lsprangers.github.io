---
layout: technical
title: A/B Testing
category: Scoring and Feedback
difficulty: Advanced
description: Discussions around Bayesian(s)
show_back_link: true
---


## A/B Testing 
- During A/B testing we will send users to, typically 2, different UI's, AI models, pricing structures, etc... and collect data to find effects

These online systems are often tied to feature flags, and use canary or rollout testing on a few random, or non-random, user groups while collecting large amounts of click data

The below sections draw on Frequentist vs Bayesian which was covered in [Bayesian Statistics](/docs/old_math_notes/probability_and_statistics/BAYESIAN.md)

### Frequentist A/B Testing
In this setup, the Frequentist approach would have:
- Null Hypothesis $H_0$​: no difference between variants
- Compute p-value: the probability of seeing the observed effect (or more extreme) under $H_0$
- If p-value < $\alpha$ (e.g., 0.05), reject $H_0$
- ***Limitations***:
    - We can't quantify how large the effects are, or how uncertain we are
    - We can simply say "yes we think there's a significant difference"

### Bayesian A/B Testing
- Assign priors to conversion rates of each group (e.g., Beta distributions)
- Use observed data to compute posterior distributions
    - For computing posterior distributions we'd need a feedback and update mechanism
    - TODO: We will create a ML Sys Design video around this
- Compute:
    - Posterior probability that variant B is better than A
    - Expected loss (e.g., how bad a wrong decision could be)
- With this approach we are able to interpret the chance that variant B is "better than" variant A
    - We can utilize [Causal Inference](#casual-inference) to understand the effects of variants on users

### Casual Inference
Correlation isn't causation - we want to directly measure what happens if we change X, or variants, on our user base

Causal Inference helps us to estimate model impact and personalization

- ***Treatment Effect***: The causal impact of a treatment (e.g., new algorithm) on an outcome
- ***Counterfactual***: What would have happened if the unit didn’t receive the treatment
- ***ATE / CATE***: Average Treatment Effect / Conditional ATE
- ***Confounding***: A variable that affects both treatment and outcome