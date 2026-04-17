---
title: Data Structures & Algorithms
layout: default
---

## DSA
This is a dump of all the DSA notes I had from school, coursework, and interviews


## Problem Families
- Prefix sum
- Sweep line / event counting
    - Meeting Rooms 2, My Calendar, Airplanes In The Sky
    - Intervals overlap, and we want to figure out the maximal merging policies
    - "What changes at each start/end event, and what active state do I maintain?"
- Frontier / interval coverage
    - Jump Game, Snow Machines, Video Stitching
    - Minimum jumps via `furthestPossible` at each layer, track a jump / machine / count as when `currIdx = endThisLayer`
        - Choices extend a reachable frontier
        - Kadane / Line Sweep are good options, and then general frontier expansion with multiple variables for counting layers
    - "Among all options currently available, which extends coverage furthest right?"
- Monotonic stack
    - Each element wants the next / previous greater / smaller thing, or we need to find maximal span where current value is min / max
    - Daily Temperatures, Next Greater Element, Largest Rectangle in Histogram, Trapping Rain Water Variants
    - Keep a stack where you continuously pop off `stack[-1]` if some condition is met 
    - Which unresolved prior elements can this new element resolve?”
- Monotonic deque / sliding optimum
    - Max / min over sliding window with direct access to both sides of window. Two pointers is a variation of this where you don't store elements
    - "How do I keep useful candidates for the current window?"
- Prefix sum + hashmap
    - Subarray condition can be written as difference between 2 cumulative states
    - Subarray Sum Is K, Contiguous Array, Binary Subarrays With Sum
    - "What earlier cumulative state would make the current one produce the target?”
- In place cyclic placement / index as hash
    - Array of numbers itself can be utilized as the proper hashmap - array positions can encode where each value belongs
        - Value `x` belongs at `idx = x-1`, swap values into correct positions, and first number where `nums[idx] != idx + 1` is the "bad number"
    - Return Sorted Array In Place, Missing Number, Missing ID
- Binary search
    - Answer is min / max threshold - `False, False, False, True, True`. That threshold ensures everything to left and right is equal
    - Koko Eating Bananas, Capacity To Ship Packages, Split Array Largest Sum
        - It doens't have to be an array, it can be on a search space of rates, packages, etc
    - "Can I write a monotone feasibility check?"
- Topological sort / DAG building
    - Directed graph where we want to build out route based on pre-requisites
        - Also able to find loops in directed DAG
    - Course Schedule, Alien Dictionary, Parallel Courses
    - "Is this a DAG problem, and do I need existence, order, or both?"
- DFS with return-vs-global split
    - Tree answer has local-through-node candiadte and a one-branch return value
        - i.e. we want to find paths, sub-tree's, etc and we can use recursion
    - Binary Tree Maximum Path Sum, Diameter Of A Binary Tree, Longest Univalue Path
    - "What information can this subtree return upwards, and what must be tracked globally?"
- Connected components
    - Grid or graph asks for groups, reachability, islands, regions, etc
        - Also useful for some graph traversals of "number or max/min of things"
        - Hardest part is setting up edges between nodes - sometimes it's impromptu definition
    - Number of Islands, Max Area Of Island, Surrounded Regions, Accounts Merge
- Backtracking with pruning
    - Need all combinations, permutations, placements, etc but constraints like size, sum, etc allow early pruning 
    - N Queens, Combination Sum, Palindrome Partitioning
    - "What partial states can never lead to a full valid answer, and what states are final answers?"
- Dynamic programming on sequences
    - Subproblems overlap, and local greedy optimum fails. States being indexes by index, prefix, position, etc allow for state tracking and memoization / tabulation
        - Bidirectional problems can also occur where combining solutions in both directions (subspaces of subspaces), can give us the answer
            - Buy and Sell Stock II, Trap Rain Water
            - These look at maximizing differences among some total number of transactions
    - Coin Change, House Robber, Decode Ways, Edit Distance
        - Word Break overlaps similar to `dp[i]` means the prefix ending at index i can be segmented validly
            - for each end position, check whether there exists a prior split `j` such that `dp[j]` is true and `s[j:i]` is a valid code
    - "What is the minimal state needed, and the recurrence relation, so future decisions only depend on this state?"
- Dynamic programming on intervals
    - Answer depends on where to split a range, usually when recursive left / right partition structure matters
    - Burst Balloons, Matrix Chain Multiplication, Palindrome Partition Variants
- Greedy with heap / online best candidate
    - Process items in order, but needs best-so-far among active candidates
    - Meeting Rooms II, Task Schedulers, IPO, Merge K Sorted Lists
    - "What candidate set do I need to pick from efficiently, and is greedy with only local knowledge sufficient?"
- Union-find
    - When components merge over time, and repeated connectivity querying matters
    - Accounts Merge, Most Stones Removed
    - "Is this really about repeated merges, or just connected components from scratch?"
- Trie
    - Many queries share prefixes, and potential prefixes are a finite set of options
    - "Can shared prefixes collapse repeated work?"
- Two heaps
    - Maintain a lower and upper half dynamically to ensure you can stay in the middle
    - Find Median From Data Stream, Sliding Window Median, IPO-ish Budget Split Variants
    - "Can I maintain a balance between two heaps with a fast rebalance?"
    
Overall:
- Need groups / reachability? DFS/BFS/Union-Find
- Need dependencies / ordering? Topo sort
- Need min/max threshold with feasibility? Binary search on answer
- Need contiguous range with monotone validity? Sliding window
- Need subarray exact count/sum relation? Prefix sum + hashmap
- Need next greater / span boundaries? Monotonic stack
- Need moving max/min? Monotonic deque
- Need minimum moves / cover target / furthest frontier? Frontier greedy
- Need local subtree answer plus global best? Tree DFS return-vs-global
- Need choose/skip with overlapping subproblems? DP


## Cheat Sheet
- Use prefix sum + hashmap for ***exact subarray sum*** questions: 
    - Count, existence, longest length, divisible/mod variants, especially when negatives may exist
    - Works for negative numbers, sliding window does not work for negative numbers
- Use sliding window for ***monotonic*** window problems based on ***at-most, or exact subarray*** questions:
    - At-most constraints, character frequency windows, and sum constraints on nonnegative arrays
    - Do not force sliding window for exact-sum problems with negatives
    - Count valid subarrays with `right - left + 1`
- Prefix-sum init: 
    - `freq = {0: 1}` for counting 
    - `first = {0: -1}` for longest length
    - `pfxSum = [0]`
    - Usually keep only a running sum, not a full prefix array
    - Sum from `[l..r] = pfxSum[r+1] - pfxSum[l]`
    - If negatives exist, standard sum-based sliding window is usually wrong; prefix sums still work
- Two pointers
    - sorted array
    - move inward
    - pair/triplet
    - remove duplicates
    - partitioning

---
- Use binary search on answer when the output is a min/max value and you can write a monotonic `check(mid)`
```python
left, right = 0, n
while left < right:
    mid = left + (right - left) // 2
    if condition(mid):
        right = mid
    else:
        left = mid + 1
return left
```
- If `check(x)` is true, then all smaller values are also true, or all larger values are also true
    - find first valid
    - or first bad
    - answer space can be values, speeds, capacities, days, sizes
    - “I’m binary searching the answer because `check(mid)` is monotonic”
- Search the answer space, not the array: 
    - capacity, speed, sweetness, threshold, minimum/maximum feasible value
- Main job is not coding binary search; it is proving the monotonicity and writing `check(mid)` correctly
- Use half-open interval: search space is `[left, right)`
- For most problems, half open will work
    - `mid = left + (right - left) // 2`
    - Initialize with `left = 0`, `right = len(arr)`
    - Loop with `while left < right`
    - `if check(mid): right = mid else: left = mid + 1`
    - return `left` as first valid position or insertion point
- For last valid X, need to switch to:
    - `mid = left + right + 1 // 2`
    - `if check(mid): left = mid + 1`
    - `else: right = mid - 1`

---
- Union Find helps in quick retrieval of connected components
- Minimum Spanning Tree's give us the smallest fully connected graph (v + e's) based on weights
    - Kruskal's is best used on list of edges where we can sort edges and pick via connected components 
    - Prim's is best for adjacency lists where we traverse over nodes based on visited set
- BFS can natively find shortest path on an unweighted graph
    - Djikstra can find it in a weighted graph with non-negative weights
        - Store weights in min heap and traverse while min heap is alive. Automatically ensures shortest path (in terms of weights) are checked before larger weights. Still traverses every edge
    - Bellman-Ford works for any graph that doesn't have a negative weight cycle (infinitely negative if we loop). Just track an update with `distances[edge_to] = min(distances[edge_to], distances[edge_from] + edge_weight)` to find if coming from another node would result in a shorter path
        - Only need to traverse $N-1$ iterations, which allows avoiding a seen set so we can potentially find a longer number of hops with a smaller overall weight





## Questions / TODO Before
- State the brute force first
- Name the pattern before coding
- Say what your variables mean
- Use half-open intervals when possible
- Talk through one example before full code
- After coding: test normal case, edge case, empty/single case
- Then questions to ask yourself
    - Is this contiguous or non-contiguous?
    - Do I need exact value, max/min, count, or existence?
    - Are negatives allowed?
    - Is the array sorted?
    - Do I need the first valid answer or all answers?
    - Is this really a graph or interval problem in disguise?
- Common edge cases
    - empty input
    - one element
    - all same values
    - duplicates
    - negatives
    - zero
    - already sorted
    - answer at start
    - answer at end
    - no valid answer

## Hashmap / Set

Use when you need:
- fast lookup
- frequency counts
- seen before
- mapping value -> index
- mapping prefix -> count or first position
- Common patterns:
    - Two Sum
    - frequency counting
    - longest streak
    - prefix sum counts



Intervals
- sort by start
    - `arr.sort(key=lambda x: (x[1], x[0]))` sorts by second then sirst
    - `arr.sort()` will sort based on greedy first, second, third, etc
    - 
- compare current interval with last merged interval
    - merge
    - insert
    - meeting rooms
    - overlap detection
    - do touching endpoints count as overlap?

Stack
- nearest greater/smaller
- undo matching pairs
- monotonic structure
- expression parsing
- histogram/temperatures
- Patterns:
    - valid parentheses
    - daily temperatures
    - next greater element
    - largest rectangle in histogram

Queue / Deque
- BFS
    - window max/min
    - order matters
- Monotonic deque:
    - keep useful candidates only
    - front is answer
    - pop worse values from back

Heap
- `[(predicate(x), x) for x in arr]` allows to insert into heap based on predicate, predicate can be `-val` for max heap
- repeatedly need smallest/largest
- top K
- merge sorted streams
- scheduling
- Patterns:
    - kth largest
    - meeting rooms II
    - task scheduling
    - merge k lists

Linked list
- dummy head `leftPtr = leftHead = ListNode(0)`. If you move `leftPtr.next = other` you can always reach left node's start via `leftHead.next`
- cycle -> Floyd
- reverse list
- merge two lists
- reorder list often means split + reverse + merge

Tree / BST
- DFS:
    - preorder: node, left, right
    - inorder: left, node, right
    - postorder: left, right, node
- BFS:
    - level order with queue
- BST facts:
    - inorder gives sorted order
    - left < node < right
- Common moves:
    - pass bounds down recursion
    - return height/depth/balance info up recursion

Graph
- BFS for shortest path in unweighted graph
- DFS for components / cycle detection
- topological sort for prerequisites
- Union Find for connectivity
- Dijkstra for weighted positive edges
- Always ask:
    - directed or undirected?
    - weighted or unweighted?
    - cyclic or acyclic?

Backtracking
- all combinations / permutations / subsets
- choose, recurse, undo
- “I make a choice, recurse, then undo the choice.”
```python
def backtrack(path, start):
    ans.append(path[:])
    for i in range(start, n):
        path.append(nums[i])
        backtrack(path, i + 1)
        path.pop()
```

Dynamic programming
- overlapping subproblems
- brute force repeats work
- asks min/max/count/ways/possible
- How to think:
    - define state clearly
    - define transition
    - define base cases
    - decide table or memoization
- Common 1D:
    - climbing stairs
    - house robber
    - coin change
    - LIS
- Common 2D:
    - unique paths
    - edit distance
        - `dp[i][j] = min edits to turn word1[:i] into word2[:j]`
        - current characters `word1[i-1]` and `word2[j-1]`
            - If curr chars equal, `dp[i][j] = dp[i-1][j-1]`
            - Else min of neighbors
    - LCS
    - interleaving string
        - `dp[i][j] = can s1[:i] and s2[:j] form s3[:i+j]`
        - third index is automatic: `k = i + j`
        - from top if `s1[i-1] == s3[i+j-1]`
        - from left if `s2[j-1] == s3[i+j-1]`
- “dp[state] means the answer for this smaller version of the problem.”