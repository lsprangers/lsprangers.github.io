---
layout: technical
title: 6. Binary Search
category: Data Structures & Algorithms
difficulty: Advanced
description: Binary Search
show_back_link: true
---

## Binary Search

$O(\log n)$ lookup on sorted search space!

The entirety of binary search is around being able to find something in $O(\log n)$ time because our data structure is sorted in some way - whether it's a Tree, a List, or a generic search space like the number line (rate of X, number of Y, etc... are just integers that are sorted)

At each step of the way you shrink the search space by half because you know the data structure is sorted in some way - if you were looking for a word in the dictionary that starts with D and you randomly flipped to the letters N, we'd look to the left

If you have some search space, lets say an array `arr` and there's an element `x`, then you can find the index `idx` of `x` in `arr` in $O(\log n)$ time and $O(1)$ space. Most of the time, searching via binary search is faster because it will beat out $O(n)$

Why is it $\log(n)$? Mostly because if there are $n$ elements, and you are constantly splitting it in half, then you'll do at most $\log(n)$ searches:
$\log(n) = x \rarr 2^x = n$

I guess that's just repeating the same thing twice - here's a photo:
![Binary Search](/img/bsearch.png)

### Templates
There are two common templates:
- Inclusive `[left, right]` which utilizes `<=`
- Exclusive open interval `[left, right)` which utilizes `<`

Setting these means the developer decides what the search space means - if you utilize `len(arr)` you know that it can't actually be apart of the search space - that'd lead to an indexing error. So you're actively choosing to have a search space of `[left, right)`. Left is a candidate, right is not. `[left, right)` is *non-empty exactly when `left < right`*, and if the dumb developer utilizes `left <= right`, they're allowing for `len(arr)` to creep in which is wrong. If `left == right`, `left < right` is empty and nothing happens

Same argument for `[left, right]` then

Going to try and utilize the below template as much as possible throughout the doc. This template is 1:1 with [`bisect_left` python implementation, which is a standard function we can also use](https://github.com/python/cpython/blob/main/Lib/bisect.py#L93)

```python
def bs(nums, target):
    left = 0
    right = len(arr)

    while left < right:
        mid = left + (right - left) // 2

        # if our number is less
        if nums[mid] < x:
            left = mid + 1
        
        # greater than or equal to - keep mid for equal to
        else:
            right = mid
    
    return(left)
```

There are some cases where `left` and `right` updates differ, and it's all dependent on what `check()` looks for and returns. Sometimes we want to keep items in the search space, other times we `+1` and `-1` to remove them from the search space when there's absolutely no reason for them

#### Open Interval Template
Utilizing the open interval template is usually the best for a large majority of problems:
- `[left, right)`, where the `right` indexes are no longer apart of the search space
    - This ***does not mean they're out of the answer space***
- `while left < right` ensures we never have `mid` never equal to `right` during an update
    - If `left = right - 1` (i.e. we're in an interval where left and right are right next to each other), then the update happens below: 
    ```python
    mid = (right - 1) + (right - (right - 1)) // 2
    = (right - 1) + 1 // 2
    = (right - 1) + 0
    = right - 1
    ```
    - So we will always have `left <= mid < right`

This allows us to utilize the `right = mid` and `left = mid + 1` update logic for most of the typical, and some atypical, cases below

Altogether:
- In `[left, right)`, `right` is outside the current search space
- `mid` is always inside the current search space, with `left <= mid < right`
- The interval shrinks until `left == right`
- For boundary-finding problems like first valid item, that final boundary is the answer, so returning left is correct

### Intuition
If you have a sorted `arr`, and you have it's start and end indexes `left, right` you can continuously check the middle `mid = left + right // 2`, and based on `mid` relation to your target you can shrink the search space in half. If `mid > target`, that means you want to focus to the left and you'll change `right = mid - 1`, and if `mid < target`, that means you want to focus to the right and you'll change `left = mid + 1`

In Java or Cpp you'd use `left + (right - left) / 2` so that, in case `right = INT_MAX`, you don't store something larger than it which would overflow

The template in Python pretty much does just that, but this one is looking for an exact match we expect to be in the array:
```python
def binary_search(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if check(mid, arr, target):
            # do something
            return
        
        # mid for sure isn't in it, so close search space
        #   based on [left, mid) interval
        if arr[mid] > target:
            right = mid
        else:
            # the search space is now surely [mid + 1, right)
            left = mid + 1
    
    # target is not in arr, but left is at the insertion point
    return left

def check(idx, arr, target):
    return(
        arr[idx] == target
    )
```

Using `len(arr) - 1` means your last valid index is included, and your valid search interval is `[left, right]`

Using `len(arr)` means your last valid index is excluded, and your valid search interval is `[left, right)`. The update procedure is `high = mid` in this scenario if `arr[mid] > target` because we want to keep the left side in tact. `high = mid` ***still removes mid from the search space***, because our interval is `[left, right)`

The main difference is what you return, and how you update your search space:
- If you want to return the exact index you can do that, or you can return an insertion point of where something new should be placed
- You can update your search space based on finding any match, the unique exact match, the first match of some kind, or the last match of some kind

### Typical Problem Statements
Some will outright say "find this value in a sorted list" which makes things easy, most won't
Other ways to describe it"
- Theres an array of times each train takes
- Array of times it takes to eat a meal
- Given a threshold k, what’s the minimum time each train / meal would take to finish
- Find an element in an array that's been sorted, and then rotated
- Capacity to ship packages within $D$ days (f' this one)
    - [Solution](/docs/leetcode_coderpad/leetcode/python/capacityToShipPackagesWithinDDays.md)

Most of these solutions will involve a `check()` function, where you will propose some item in the search space, like an index or other value, and then quickly check if that value works

For the capacity to ship packages problem, the `check()` function revolves around checking if the weight capacity can cover the shipping requirements - the `check()` funciton itself runs in $O(n)$ time so it seems slow, but ultimately it's still fast compared to other routes
- In the above classic case, `check()` is just comparing the element at `arr[idx]` to `target`

The reason this is "fast" is that in $O(\log(n))$ time you can propose capacity values, and then for each of them it takes $O(n)$ time to check so the overall solution is $O(n \cdot \log(n))$. This is faster than iterating from 1 to 2 to 3... capacity which would result in $O(n^2)$

### Typical Patterns And Pitfalls
There are some typical patterns pitfalls that annoyingly come up in almost every review

The main questions to ask:
- What is the search space?
- What does `check(mid)` mean?
- What is the goal (min valid, max valid, exact match)?
    - This will alter the return
- When is mid good/bad? Adjust left/right accordingly
    - This will alter our `left = ` and `right =` updates
- Do you return left, right, or mid?

### Duplicates
If an input array has duplicates, then you need to tweak the `check()` function to try and find the first or last position of the desired target

If you have `arr = [3, 4, 5, 5, 6, 7]`
- `left = 0`
- `right = 5`
- `mid = 2`, therefore, `mid` points to the leftmost 5

Need to now change `check()` to use `arr[mid] >= target` - If we want to find the left most value, i.e. the "first occurrence", and we find a `mid` that matches our target, what do we need to do? We need to move our search space to maximum mid, and keep searching the leftern side for move values - i.e. `right = mid`

```python
def binary_search(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2

        # In the check here, if this "works", we still keep mid involved in the search space
        if check(mid, arr, target):
            right = mid
        
        # if it absolutely doesn't work, there's no need to keep mid in search space
        else:
            left = mid + 1

    return left

def check(idx, arr, target):
    return(
        arr[idx] >= target
    )
```

Using `len(arr)` means your right boundary is past the last valid index, and your valid search interval is `[left, right)`. In this you check `left < right`


### Insertion Vs Index And Bisect Functions
If we are looking to find the insertion index, there's a slight tweak versus finding a specific index and it mostly comes down to how you alter the `check()` function...as usual...and then the pointer that's returned

A very easy way to do this in python is via the `bisect.bisect_left(arr, target)` method - the below problem statement and python code shows it

"Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order. You must write an algorithm with `O(log n)` runtime complexity."
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        return(bisect.bisect_left(nums, target))
```

The bisect modules figure out where an element should be inserted to ensure the ordering of the list stays true, while having different semantics for arrays with repeated elements:
- Inserting at a position moves the item in that position **to the right**
- The `bisect_left(a, x, ...)` function takes a sorted list a and a value x and returns an index i such that after insertion:
    - All elements to the left of the index (`a[:i]`) are less than x
    - All elements to the right of and at the index (`a[i:]`) are greater than or equal to x
- `bisect_right` on the other hand will return an index i such that after insertion:
    - All elements to the left of the index (`a[:i]`) are less than or equal to x
    - All elements to the right of the index (`a[:i]`) are greater than x
- So they mostly differ on how they handle equal to, and exact insertion point
- If there was an array `arr = [1, 5, 6, 8]`
    - `bisect_left(arr, 7)` would return 3 as the 2nd index has a value less than it's target
    - `bisect_left(arr, 6)` would return 2 as it's the target, so less than or equal to
    - `bisect_right(arr, 7)` would return 3 as the 2nd index has a value less than it's target
    - `bisect_right(arr, 6)` would return 3 as all elements to the left must be less than or equal to 6

Looking at the [bisect_left source code](https://github.com/python/cpython/blob/3.14/Lib/bisect.py#L74), it's exactly our template, except with many more error handling and good coding practices
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        
        return(left)
```

The [Longest Subsequence With Prefix Sum Problem](/docs/leetcode_coderpad/leetcode/python/longestSubsequenceWithLimitedSum.md) utilizes `bisect_right` to find the length of the longest subsequence that's less than or equal to a certain query
- After calculating the prefix sum, the length of longest subsequence is equal to the last index of the prefix sum where we could insert the query 
- If the pfx sum has `[1, 4, 7, 8]`, and our query is 6 or 7, we'd want to return 2

The intuition for pointer updates can be shown at the end of the [minimize K section](#minimize--first-acceptable-x)

### Solution Spaces
Binary Search can also be used outside of arrays - generically it can be used on any solution space such as integers, some capacity, or anything else. A typical scenario of this is a problem asking "what is the min/max something can be done"

Ultimately, the only true criteria that need to be met for binary search are:
1. You can quickly, in $O(n)$ or better time, verify if the task if possible for a given input `x`
2. If the task if possible for an input `x`, and you are looking for:
    - A maximum, then it's also possible for all inputs less than `x`
    - A minimum, then it's also possible for all inputs greater than `x`
3. If the task is not possible for an input `x`, and you are looking for:
    - A maximum, then it's also impossible for all inputs greater than `x`
    - A minimum, then it's also impossible for all inputs less than `x`

Statement 1. references the ability to quickly do things, as the `check()` function needs to be fast enough that we can do better than $O(n^2)$, and statements 2. and 3. revolve around the search space being able to be "shrunk" via mid updates - if we can't shrink the search space automatically because something's unsorted, or it doesn't make sense, then we cannot do binary search (i.e. we can't cut out that portion of solution space)

![BSearch Zones](/img/bsearch_zones.png)

Problems finding a min / max are actually searching for this magic threshold that separates possible from impossible, and that magic threshold is what we're trying to obtain as our output of binary search

Establishing the solution space is typically the hardest part - if you're looking for a min/max rate, how can you decide what "max" is? 
- In [Koko Eating Bananas](/docs/leetcode_coderpad/leetcode/python/kokoEatingBananas.md) Koko only eats a pile at a time maximum, and so the maximum rate can only be the maximum of the piles `max(piles)`
- In [Capacity Planning](/docs/leetcode_coderpad/leetcode/python/capacityToShipPackagesWithinDDays.md) you can ship as many packages as possible with a specific rate, but the most weight you could process in a single day is the entire weight, so the maximum rate is `sum(weights)`

The solution space can be defined by $k$ which represents the range of the solution space - sometimes it's $[0, k]$, sometimes it's $[\text{min}, \text{max}]$ where $k = \text{max} - \text{min}$, etc...

Once you have the $k$ figured out, ***the binary search time complexity becomes $O(n \log{k})$***
- $n$ revolves around the time taken for a check function to run - typically a greedy function that could exhaust the entire input list
- $\log{k}$ revolves around traversing the search space, where for each traversal we need to run the $O(n)$ `check()` function

## ATypical
There are some weird ones thrown in as well, especially rotating lists, a weird search space, or "guessing" at a condition
The important alternate patterns are:
- first / last acceptable value
- minimize or maximize `k` subject to a condition
- searching over an answer space instead of array values
- special structures like rotated arrays, duplicates, and peak finding

### Minimize / First Acceptable X
This still must hold the binary search criteria of "if valid for X, then is valid for all `y > x` - meaning the underlying search space must be ***monotonic***
Typical examples:
- first bad version
- search insert position / lower bound
- minimum feasible speed / capacity / threshold
- integer square root as “first too large,” then return one less

The main idea is to search for the boundary, where we go from `False` to `True`. In these scenario's there can be multiple `mid` that satisfy the result, but you want to find the first / last one so you keep shrinking / dragging search space based on `check(mid)`:
- If `check(mid)` is `True`, then `mid` may be the already valid answer, and we know the structure is monotonic, so everything above `mid` is also `True`
    - Can shrink space via `right = mid` so that our search space turns into `[left, right)`
- If `check(mid)` is `False`, we know that for sure `mid` isn't used in our search space. `mid + 1` might be, it's the least thing we could update to, and our left interval is closed so we update `left = mid + 1` to `[mid + 1, right)`

The above is still the standard half open template!

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n
        
        while left < right:
            mid = left + (right - left) // 2
            
            # mid is definitely bad, so we want to keep it
            #   in search space
            # we are looking for first valid X though, so 
            #   want to bring left up as much as possible
            # "all versions after a bad version are bad"
            if isBadVersion(mid):
                right = mid
            # if it's not a bad version, we know 
            else:
                left = mid + 1
        
        return(left)

# [good, good, bad, bad, bad]
# 0, 2, 5
# update right = 2
# 0, 1, 2
# update left = 2

# [good, bad, bad, bad, bad]
# 0, 2, 5
# update right = 2
# 0, 1, 2
# update right = 1
# left = 1
```

In these solutions the open interval concept `[left, right)` still holds, but there's a chance that when we set `right = mid` and have `[left, mid)` that `mid` is actually the true last valid version. That's fine - if `right` is truly the last valid bound, then:
- `left < right` will continue happening and `left = mid + 1` will eventually occur
    - If `left < right`, does that guarantee that `mid` is never equal to right via `mid = left + (right - left) // 2`? It would be bad if `mid = right` in some scenario and we do `left = mid + 1 = right + 1 = answer + 1` and we return a version above the answer

This is slightly different from the typical exact search semantics where `if arr[mid] > target` then `mid` is definitely not involved. We still set `right = mid` here, but in exact search the search space is equivalent to the answer space, and so in that update we would be removing `mid` from the answer space. In the minimize scenario's, `if check(mid)` is `True` `mid` may still be the answer, but we can still do `right = mid` which removes it from the search space but keeps it in the answer space

At the end we do `return(left)` which is valid, `left == right` means that's where the search collapsed on the boundary index between `[.., False, True, ...]`

This is the exact intuition for ***first-valid / lower bound / insertion-point*** style problems

### Maximize / Last Acceptable X
This is the opposite of the template above where if `check(mid)` is `True`, then `check(smaller)` is also `True`. We're looking for the threshold of `[True, True, True, False, False]` where `True` turns into `False`. In this case if we come across some `True`, then `mid` may be the correct answer so we want to keep it in `[left, right)`

This does lead to a potential infinite loop where `mid == left` via `left + (right - left) // 2` because we aren't forcing `left = mid - 1`, and so the `mid` calculation logic needs to change to `left + right + 1 // 2` which will guarantee that `left < mid <= right`

```python
left = 4
right = 5
mid = left + (right - left) // 2 = 4 + (1) // 2 = 4

check(4) # --> True, left = 4 would result in an infinite look
left = mid + 1 # --> 
```

### Search On Answer
Search On Answer problems usually mean changing the search space, and then finding the [Lower Bound](#lower-bound-first-valid-x) or [Upper Bound](#upper-bound-last-valid-x) based on problem statement

```python
left = max(weights)
right = sum(weights)

while left < right:
    mid = (left + right) // 2
    if can_ship_in_days(mid):
        right = mid
    else:
        left = mid + 1
return left
```

### Rotating Lists
Problem Statement:
Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array `nums = [0,1,2,4,5,6,7]` might become:

    `[4,5,6,7,0,1,2]` if it was rotated 4 times.
    `[0,1,2,4,5,6,7]` if it was rotated 7 times.

Notice that rotating an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`

If an array isn't rotated, then you know for sure last element at end $\geq$ first element at 0. However, if an array is rotated, then the last element would be smaller than the first element - seeing this pattern you can realize there's a place, an ***inflection point*** where you can figure out where the real start was

![Inflection Point](/img/inflection_point.png)

`arr = [4, 5, 6, 7, 0, 1, 2, 3]`
Our inflection point above is 4 - this means we have 2 arrays:
- `arr[inflection: ]` which is `[0, 1, 2, 3]`
- `arr[0: inflection]` which is `[4, 5, 6, 7]`
- Both of these are sorted arrays! We can run regular ol' binary search on these 2 arrays, but we need to figure out:
    - Where the inflection point is
    - If our target is in the left `arr[0: inflection]` array, or the right `arr[inflection: ]`
    - Looping over array to find the inflection point is $O(n)$, and so problems that say "You must write an algorithm with $O(log n)$ runtime complexity." make this a bit trickier

***We can find the inflection point in $O(log n)$!***
```python
left = 0
right = len(arr)
...
mid = left + right // 2
if check(mid):
    return(mid)
elif mid > first element of array:
    search to the right
else:
    search to the left
```
because if you find the number 6, which is above the first element 4, you know our inflection point is still to the right of us, but if you find `0, 1, 2, 3`, we know it's to the left

***So in total there are 2 binary searches in these types of problems***:
- Finding the inflection point
- Splitting up the array based on inflection point and target, and running a typical binary search there

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums) < 2:
            return(0 if nums[0] == target else -1)
        
        # find inflection point
        left = 0
        right = len(nums)

        # [4, 5, 6, 7, 0, 1, 2, 3]
        while left < right:
            mid = left + (right - left) // 2
            
            # we know inflection is to the right
            # left being mid could still be the right one though
            if nums[mid] >= nums[0]:
                left = mid + 1         # [mid, right)
            
            # inflection point to the left
            else:
                right = mid
            
        inf_point = left if left < len(nums) else 0
        
        if inf_point != 0 and target < nums[0]:
            left, right = inf_point, len(nums)
        else:
            left, right = 0, inf_point if inf_point != 0 else len(nums)
        
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return(mid)
            elif nums[mid] > target:
                right = mid
            else:
                left = mid + 1
        
        return(-1)
```

#### Rotating List Without Initial Pivot Search
There is an actual way to run binary search on a rotated array without initially finding the pivot and splitting

In the rotated array problems there are 3 indices we need to utilize at every step:
- `left`
- `mid`
- `right`

We need all 3 of these to be real and index-able, because we are using them in comparisons to find a specific number. These usually aren't boundary problems, so you can do safe updates like `mid - 1` and `mid + 1` as well. Therefore, it's usually more beneficial to utilize a closed interval template so that all of the indexes exist, and we are fully able to make greedy updates to the search space

```python
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1   # closed interval [left, right]

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            # left half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1

            # right half is sorted
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

### Peaks
Finding peak elements can be seen as a form of binary search where you are looking for some bounday `[inc, inc inc, dec]` where on the left there's an increasing sequence, and on the right there's a decreasing sequence - you could have an array similar to `[1,2,3,4,3,5,6,7]` where `4` is a peak, but you can't necessarily tell unless you're exactly at that index

There's a nuance to most of these problems in the stated assumptions - "You may imagine that `nums[-1] = nums[n] = -inf`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array."

Therefore, the update logic would need to be based on if we're currently in an index in an increasing sequence or not:
- If a certain index `mid` is sitting in a descending sequence of numbers, i.e. a local falling slope, it means the peak will always lie to the left of this element
- Therefore, we can reduce the search space to the left of this element via `right = mid`
- If `mid` lies in an ascending sequence of numbers, it implies the peak element lies towards the right of this element, with our typical `left = mid + 1` update

```python
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return(0)
        
        left = 0
        right = len(nums)
        
        while left < right:
            mid = left + (right - left) // 2
            
            # if we can safely check both indexes around us
            if 0 < mid < len(nums) - 1:
                if nums[mid - 1] < nums[mid] > nums[mid + 1]:
                    return(mid)
                # means we're in an increasing sequence
                elif nums[mid - 1] < nums[mid]:
                    left = mid + 1
                # we're in decreasing
                else:
                    right = mid
            
            # we're at one of the ends - logic here is screwy with short arrays like [1,2], and [2,1]
            elif mid == 0:
                if nums[mid] > nums[mid + 1]:
                    return(mid)
                else:
                    left = mid + 1
            else:
                if nums[mid - 1] < nums[mid]:
                    return(mid)
                else:
                    right = mid - 1
        
        return(left)
```


### Find A Rate
There are some specific problems like [KoKo Eating Bananas](/docs/leetcode_coderpad/leetcode/python/kokoEatingBananas.md) and Elves on Package Line where you basically need to find a rate of something, and then check if that rate suffices

Koko's eating rate, maybe it's 3 bananas-per-hour, and if that works then we'd look if a higher rate would suffice like 10-per-hour, etc...

Usually this would mean the rate finding is $O(\log R)$ where $R$ is the rate search space, and then there'd be an input array of size $N$ that you must check through. The check function is typically $O(N)$ so in total it's $(O\log R \cdot N)$ versus $O(R \cdot N)$

Otherwise, you just continuously check the rate instead of "smart searching" using binary search

## Structures
Lists and Tree's are typically the data structures that you see with Binary Search

### Lists
There's some gotchas for list, mostly around defining right and left, and different $\le$ vs $\leq$, but altogether the pseudocode is pretty easy
Pseudocode for list:
```python
# list of 10 nums
nums = sorted(list)
val_to_find = get_num()

left = 0
right = len(nums)

while left <= right:
    # 0 + (10 - 0) // 2 = 5 // 2 = 2
    mid = left + (right - left) // 2
    if check(val):
        left = mid + 1 # or left = mid
    else:
        right = mid - 1 # or right = mid
        

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