---
title: Priority Queue Comparison Struct
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Priority Queue Comparison Struct
This one is very specific, and mostly just got dragged along

```cpp
    struct CompareByIndex {
        int index;

        CompareByIndex(int idx) : index(idx) {}

        bool operator()(const vector<int>& a, const vector<int>& b) const {
            return a[index] > b[index]; // Change to '<' for ascending order
        }
    };

    priority_queue<vector<int>, vector<vector<int>>, CompareByIndex> minHeap(CompareByIndex(2));
```