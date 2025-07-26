---
layout: technical
title: 6. Binary Search
category: Data Structures & Algorithms
difficulty: Advanced
description: Binary Search
show_back_link: true
---

## Binary Search

$O(\log n)$ lookup on sorted array!

The entirety of binary search is around being able to find something in $O(\log n)$ time because our data structure is sorted in some way - whether it's a Tree, a List, or the number line (integers)

At each step of the way we shrink the search space by half because we know the data structure is sorted in some way - if we were looking for a word in the dictionary that starts with D and we randomly flipped to the letters N, we'd look to the left

Most of the time, BSearch is "faster" because it will beat out $O(n^2)$

Why is it $\log(n)$? Mostly because if there are $n$ elements, and we are constantly splitting it in half, we'll do at most $\log(n)$ searches
$\log(n) = x \rarr 2^x = n$ 

I guess that's just repeating the same thing twice - here's a photo:
![Binary Search](/img/bsearch.png)

### Typical Problem Statements
Some will outright say "find this value in a sorted list" which makes things easy, most won't
Other ways to describe it"
- Theres an array of times each train takes
- Array of times it takes to eat a meal
- Given a threshold k, what’s the minimum time each train / meal would take to finish
- Find an element in an array that's been sorted, and then rotated
- Capacity to ship packages within $D$ days (f' this one)
    - [Solution](/docs/leetcode/python/capacityToShipPackagesWithinDDays.md)

Most of these solutions will involve a `check()` function, where you will propose some item in the search space, like an index or other value, and then quickly check if that value works

For the capacity to ship packages problem, the `check()` function revolves around checking if the weight capacity can cover the shipping requirements - the `check()` funciton itself runs in $O(n)$ time so it seems slow, but ultimately it's still fast compared to other routes

The reason this is "fast" is that in $O(\log(n))$ time we can propose capacity values, and then for each of them it takes $O(n)$ time to check so the overall solution is $O(n \cdot \log(n))$. This is faster than iterating from 1 to 2 to 3... capacity which would result in $O(n^2)$

## Typical Patterns And Pitfalls
There are some typical patterns pitfalls that annoyingly come up in almost every review, and using them correctly is very important!

| Goal / Pattern                              | `low` Update    | `high` Update    | Loop Condition      | Return              | Notes                            |
| ------------------------------------------- | --------------- | ---------------- | ------------------- | ------------------- | -------------------------------- |
| **Search on value / exact match**           | `low = mid + 1` | `high = mid - 1` | `while low <= high` | index or -1         | Classic binary search            |
| **Find first `x` such that condition(x)** | `high = mid`    |                  | `while low < high`  | `low`               | Lower bound                      |
| **Find last `x` such that condition(x)**  | `low = mid + 1` |                  | `while low < high`  | `low - 1`           | Upper bound (post-process `-1`)  |
| **Minimize the smallest valid value**       | `high = mid`    |                  | `while low < high`  | `low`               | e.g., Ship packages, Split array |
| **Maximize the largest valid value**        | `low = mid + 1` |                  | `while low < high`  | `high` or `low - 1` | Depends on what `check()` means  |


***Classic Binary Search***
```python
while low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1
```

***Lower Bound (First Valid X)***
```python
while low < high:
    mid = (low + high) // 2
    if condition(mid):  # go left
        high = mid
    else:               # go right
        low = mid + 1
return low
```

***Upper Bound (Last Valid X)***
```python
while low < high:
    mid = (low + high + 1) // 2  # Bias right
    if condition(mid):  # go right
        low = mid
    else:               # go left
        high = mid - 1
return low
```

***Search On Answer***
```python
low = max(weights)
high = sum(weights)

while low < high:
    mid = (low + high) // 2
    if can_ship_in_days(mid):
        high = mid
    else:
        low = mid + 1
return low
```


### What To Define
For any BS problem:
- What is the search space?
- What does check(mid) mean?
- What is the goal (min valid, max valid, exact match)?
- When is mid good/bad? Adjust low/high accordingly.
- Do you return low, high, or mid?

### Answer Space
The discussion in [Capacity To Ship Packages](/docs/leetcode/python/capacityToShipPackagesWithinDDays.md) showcases the need to rigorously define answer spaces in the correct way

If we are checking potential answers outside of this space, they may return false positives / negatives that would ruin our entire check!

## Structures
Lists and Tree's are typically the data structures that we see with Binary Search

### Lists
There's some gotchas for list, mostly around defining high and low, and different $\le$ vs $\leq$, but altogether the pseudocode is pretty easy
Pseudocode for list:
```python
# list of 10 nums
nums = sorted(list)
val_to_find = get_num()

low = 0
high = len(nums)

while low <= high:
    # 0 + (10 - 0) // 2 = 5 // 2 = 2
    mid = low + (high - low) // 2
    if check(val):
        low = mid + 1 # or low = mid
    else:
        high = mid - 1 # or high = mid
        

return(-1)
```

### Tree
In a binary search tree, there's some special properties where, for any Vertex V, it's right child is greater than it's value, and its left child is less than it's value

Ultimately it's just a way to restructure a Linked List so that search is in $O(\log n)$ time - this entire concept is the idea of [Self-Balancing Binary Search Trees](/docs/dsa/6.%20binary%20search/SELF_BALANCING.md) such as [B-Tree's](/docs/architecture_components/databases%20&%20storage/Disk%20Based/BTREE.md). Self balancing tree's have less efficient writes (since they need to find where to place nodes and do some restructuring), but the idea is that reads are much more efficient

A Binary Search Tree has similar code structure to Lists

```python
def search_bst(root, target):
    while root is not None:
        if root.val == target:
            return True
        elif target < root.val:
            root = root.left
        else:
            root = root.right
    return False
```