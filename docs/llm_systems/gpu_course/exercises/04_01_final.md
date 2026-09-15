---
layout: technical
title: 4.01 - Final C++ Project
category: CUDA Course Exercises
difficulty: Advanced
description: Structured dump of GPU notes
show_back_link: true
---

## Final C++ Project
The Maxwell's Equations simulator predicts how electromagnetic waves propagate. For this assessment, you'll begin with a simple, though working, 2D Maxwell's Equations simulator. In its current CPU-only form, this application takes about 15 seconds to run on $4096^2$ cells, and 4 minutes to run on $65536^2$ cells. Your task is to GPU-accelerate the program, retaining the correctness of the simulation.
