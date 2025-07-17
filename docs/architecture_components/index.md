---
title: Architecture Components
layout: default
---

# Architecture Components
Components are reusable building blocks - typically you stitch a few together, with specific configurations, to achieve some sort of system

A lot of the times the Components we refer to here are going to be abstract infrastructure pieces, and you'd write your own application level code that utilizes these components

AWS is the most famous example of platforming in this way, and a large majority of their solutions are resuable components that they deploy to be highly available, durable, and scalable

# [Typical Components](/docs/architecture_components/typical_reusable_resources/)
These are going to be examples that we build out from scratch - such as the architecture to build out a queue from scratch using only "up" VM's in a VPC

This will not be an exhaustive exercise, but it's helpful to see how all of this works because it allows you to understand configurations of cloud resources much better. A great example is marking a message as "seen" in a distributed queue, and how that relates to exactly once, at most once, or at least once semantics, and how that can be built into a typical queue system

# The Rest
Outside of [Typical Components](/docs/architecture_components/typical_reusable_resources/) we simply discuss a large number of Components as they're seen "in the wild", and how we can reuse these

In everyday product building you'd never build your own distributed queue from scratch - you'd just use SQS, Celery, or Redis because they have proven themselves

In these sections we discuss all of the different component types such as Databases & Storage, Messaging, and Data Warehousing

These sections are not exhaustive, and they are not disjoint! Redis can be used as a cache, queue, and in-memory database