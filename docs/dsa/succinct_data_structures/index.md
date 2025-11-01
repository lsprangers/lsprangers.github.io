---
title: Succinct Data Structures
category: Data Structures & Algorithms
difficulty: Advanced
description: Data structures for compressed data
show_back_link: true
---

## Succinct Data Structures
The whole idea of "succinct data structures" is to create data structures that allow certain ***fundamental algorithms on compressed data***

The data structures themselves allow for compressed data to be stored, and even searched over, acted on, altered, etc...

The below is mostly a regurgitation from Starifact in Reference portion

Bit array - `[0, 1, 0, 1, 1, 0, 1, 0]` is 8 bits or 1 byte long!

### Rank and Select Bit Vector
- ***Rank*** function will give the cumulative sum of 1's set up to a certain point
    - `[0, 1, 1, 2, 3, 3, 4, 4]`
    - `rank(2) = 1`
    - `rank(4) = 3`
    - `rank(7) = 4`
- ***Select*** allows an input of `[0, # of 1's]` and essentially gives us the index of that set 1
    - `select(1) = 1`
    - `select(2) = 3`
    - `select(4) = 6`

A succinct data structure allows that these 2 operations can run in $O(1)$ time, and only requires a small amount more space than storing the original bit array

A typical ***use case*** is tracking where substrings start in a large string (concatenated from multiple smaller ones). One example would be "HelloThereIAmAConcatenatedString"

Rank / Select could be tracked with another "helper" data structure

```
    s       = "HelloThereIAmAConcatenatedString"
    s_split = ["H", "e", "l", "l", "o", "T", "h", "e", "r", "e", "I", "A", "m", "A", "C", "o", "n"", c", "a"", t", "e", "n", "a"", t", "e", "d", "S", "t", "r", "i", "n", "g"] 
    helper  = ["Hello", "There", "I", "Am", "A", "Concatenated", "String"]
    rank    = [1, 1, 1, ....] # index of words for our letters
    select  = [0, 5, 10, 11, 14]
```

Then, for any letter, you can find:
- What substring it's apart of via `rank(idx)`
- Get the start of that substring, or any adjacent substrings via `select(rank(idx))`

#### Further Thoughts And Use Cases
- Finding page of data block on disk
    - This allows you to maintain unique identifiers for slices in a block of data in a compact way
- Finding substring identifer


- Q: Why is this compact? 
    - A: For normal rank/select vectors we'd use a bit vector as long as the string, with just these small constant arrays (rank and select, not `s_split`) you don't need all of this extra data
    - A common approach is to store rank samples every fixed number of bits, like every 64 bits, plus a smaller lookup table
    - For a string that's 1MB long, or $1,024 * 1,024 \approx 1,000,000$ bytes, then you would need to store 
    A common approach is to store rank samples every fixed number of bits (say, every 64 or 512 bits), plus smaller lookup tables for the bits in between.
        - For example, if you store a 32-bit integer (4 bytes) for every 256 bits (32 bytes) of the original bit vector:
        - $8,000,000$ bits / $256$ = $31,250$ samples
        - $31,250$ samples × $4$ bytes = $125,000$ bytes ≈ 122 KB
        - Add some extra for lookup tables and select structures, and you get ~128 KB.
    - This then gets into usage of sparse arrays for storage of rank / select
        - In a dense vector you store a bit for every possible other bit
        - Most of these bits are 0 (sparse)!
        - Sparse rank / select data structures only store the positions of the set bits (1's) - not the entire thing

#### Wavelet Matrix
Using Rank / Select can help us with the following

These help to generalize rank / select over arbitrary alphabets

TODO: I was too tired

#### FM Index
Using Rank / Select can help us with the following

Let's you store text in a compact way with important query operations:
- `count(pattern)` counts how many occurrences of a substring (contiguous) occur in some text
- `locate(pattern)` gives the index of each occurrence of a substring in text

#### Balanced Parentheses
Using Rank / Select can help us with the following

Programming languages and encodings typically have many hierarchies of parent / children. Here you desire to navigate tree's of these relationships in an efficient way

JSON, XML, AST's of function calls, etc... all have some relationship like this that we'd desire to query and work with

- `parent(node)`: gives the node that this node is a child of
- `first_child(node)`: gives the first child node of a node
- `next_sibling(node)`: gives the next sibling of a node (within its parent)
- `previous_sibling(node)`: gives the previous sibling of a node (within its parent)
