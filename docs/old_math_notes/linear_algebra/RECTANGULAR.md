---
title: Rectangular Matrices and Linear Systems
description: Understanding the behavior of rectangular matrices in linear systems
tags: [linear algebra, matrices, linear systems]
layout: default
---

- If $\textit{A}$ is rectangular:
    - Tall (more equations than unknowns): a unique solution can occur only if $\textit{A}$ has full column rank and the system is consistent (i.e., $\bold{b}$ lies in the column space). But if full column rank holds and consistency holds, solution is unique; if not consistent, no solution
        - Intuitively, you would just require $\bold{b}$ to lie in the same "plane" as our column space
            - If you have a rectangular $3 \times 2$ (3 examples of 2D) matrix, the column space is a 2D plane in $\mathbb{R}^3$
            - If $\bold{b}$ is also a plane, sure you can achieve it, if it's a cube of course you can't         
    - Wide (more unknowns than equations): cannot have a unique solution unless you impose extra constraints (e.g., least-squares with regularization); otherwise either infinite or none
        - Intuitively, this means you have more "directions" to move in the solution space than you have "directions" in the constraints, leading to either multiple solutions or no solution at all