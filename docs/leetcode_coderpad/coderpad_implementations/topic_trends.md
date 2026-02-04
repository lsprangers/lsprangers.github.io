---
title: Topic Trends
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building a system that tracks trending topics. Each topic has a name and a numeric score. You must design a structure that supports these operations:
- `add(topic: str, score: int)`
    - If topic doesn't exist, insert it with the given score
    - If it already exists, increase it's score by the given amount
- `top(k: int)` 
    - Return top k topics with the highest score, in descending order
    - If scores tie, return topics in lexicographical order
- `reset(topic: str)`
    - Reset topics score to 0
    - Topic exists, but shouldn't rank above any topics with positive score

You may assume:
- There can be up to $10^5$ operations
- Topic names are strings
- `top(k)` may be called frequently
- `add` and `reset` may interleave arbitrarily with top


### Example


### Constraints


### Initial Thoughts, Questions
- If we use priority queue, then
    - `add` is $O(\log n)$ for insert, and worst case $O(n \times log n)$ for update
        - If the score we need to update is at the "bottom", i.e. 0, we need to pop off everything before it into `helper_queue`, $O(n)$, update the score, and then add all of that back into base priority queue `base_queue`
        - After popping off each insertion into `helper_queue`, which is $O(n \ times 1)$ work at worst, inserting each of the $n$ back into `base_queue` takes $O(\log n)$ effort
    - `top` would be $O(k \times \log n)$
        - We pop off $k$ terms into `helper_queue`, inserting them back in is $k$ push of $O(\log n)$ effort
    - `reset` would be similar to updating add as we need to go find the topic, update it's score, and then push everything back to `base_queue`
- We can use a combination of priority queue and hash table here
    - For each entry, we keep track of it's current score in hash table `curr_score: Dict[str, int]`
    - Adding a net new topic means adding it to `curr_score` and pushing onto `base_queue` which would be $O(1) + O(\log n)$ time
    - Updating a topic would become 
        - $O(1)$ updating `curr_score`
        - $O(\log n)$ pushing the updated topic into `base_queue`
        - Means we need to push in `(score, topic_name)` tuple into `base_queue`
            - We may need to also hold onto some sort of version for each score `(score, topic_name, version)`
            - Hold onto curr version in `curr_score: Dict[str, (int, int)]` so that for each new update via add, we increment this version as well - this is all needed to move past items in `top k`, i.e. drain queue and invalidate, for top k calls
    - For each `top` call, we then need to continuously pop off of `base_queue` and check each item against `curr_score` dict to check if it's the latest score or not
        - Time complexity here is $O(K)$ where $K$ is number of items we pop off including invalid data points, checking against `curr_score` is $O(1)$
        - After draining, we do need to hold onto valid entries in `helper_queue` and push them back on for $O(k \times \log n)$ similar to previous time
    - `reset` is then just a specific type of update where we increment version and update score to 0
- Given that `top` may be called frequently, there's really no difference between pure priority queue and priority queue + hash map, but storing all of the operations and current state would certainly have some space effect
    - Worst case we'd store all operations in `base_queue` until it's drained, but `top` is called frequently so it'd drain frequently
    - `add` and `reset` are intermingled with `top` so it'd be ideal to not have those block nearly as much
 

### Implementation
```python



```