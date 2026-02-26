---
title: Median Finder
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
Simply a class to find the median!

Requirements:
- $O(log n)$ insertion
- $O(1)$ median retrieval

### Initial Thoughts, Questions
- $O(1)$ median retrieval means it must not be dependent on size of underlying data structure
- $O(\log n)$ insertion means inserting at correct position inside of data structure
    - If we utilize an array it would be $O(n)$ to insert new objects given array resizing, and so we need another solution
- The main idea is we need to keep 2 ordered structures, where one contains "left" and one contains "right", on the left we need to keep track of everything to left of median up to largest element (max heap), and on the right we'd need to keep track of everything on the other side with smallest element above median (min heap)
    - On insertion, we see if `val` greater than or less than median, and then insert that into either left or right based on those differences
    - Also need to track the sizes of both left and right
        - If there are odd total elements, then left and right should be of equal size and median is last one in middle
        - If there's an even number of total elements we should store 2 heaps, and just take average of both roots to find median


### Implementation
```python
import heapq

class MedianFinder:
    def __init__(self):
        # max heap, will utilize negatives
        self.left = []
        self.right = []
    def addNum(self, num: int) -> None:
        # left
        if not self.left or num < -self.left[0]:
            heapq.heappush(self.left, -num)
        # right
        else:
            heapq.heappush(self.right, num)
        # ensure len
        if abs(len(self.left) - len(self.right)) > 1:
            if len(self.left) > len(self.right):
                heapq.heappush(self.right, -heapq.heappop(self.left))
            else:
                heapq.heappush(self.left, -heapq.heappop(self.right))
        # ensure ordering, idk when this occurs, but it can
        if right and -left[0] > right[0]:
            tmp_left = -heapq.heappop(self.left)
            tmp_right = heapq.heappop(self.right)
            heapq.heappush(self.left, -tmp_right)
            heapq.heappush(self.right, tmp_left)
    def findMedian(self) -> float:
        # left = [1, 2, 3]
        # right = [4, 5]
        # median should be 3, not 3 + 4 / 2
        # left = [1, 2, 3]
        # right = [4, 5, 6]
        # median should be 3 + 4 / 2
        if len(self.left) == len(self.right):
            resp = (-self.left[0] + self.right[0]) / 2
        else:
            resp = -self.left[0] if len(self.left) > len(self.right) else self.right[0]
        return resp

f = MedianFinder()
f.addNum(10)
# left = [10]
# right = []

f.addNum(1)
# left = [1, 10]
# right = []
# abs(lens) > 1
# left = [1]
# right = [10]
```

## Systems Design


### High Level requirements


#### API Surface

#### Clarifying Questions
Questions around implementations, strict vs approximate, and anything that would kill any choices made in future

#### System Constraints
Summarize system constraints in your own words
- QPS 
- latency SLO    
- consistency requirements
- failure tolerance

#### Identify Core Challenges
What makes this problem hard in distributed manner (MOST IMPORTANT PART)
- Distributed correctness (no double allow)
- Routing / management
- Data structure
- Scale + latency
- Failure behavior
- single-writer vs linearizable store
- availability vs consistency
- data plane vs control plane

#### Starter Architecture
Distributed compatible, but high level components and algorithms, focus on partitioning and scaling, not frontend or anything. Some data structure information is OK, specifically ones that relate to the core problem.

Components + Flow + network, partition, and some data structures

#### Real Architecture
Now you make in depth choices on literally everything, and draw the entire thing out

#### Component Deep Dive
Usually one or two, picked by interviewer or you know to dive into them

Potentially pseucode or pseudo architecture
