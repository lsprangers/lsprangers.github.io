---
title: Levenshtein
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Levenshtein
Levenshtein is one, and probably the most known, edit distance calculation that can calculate how many edits it would take to get from `str1` to `str2`

Edits can be:
- Insert
- Update
- Delete

Given that one transformation could affect downstream transformations, we cannot take a greedy approach and this typically spells out a 2-D [Dynamic Programming](/docs/dsa/10.%20dynamic%20programming/index.md) example

### Example
|   | 0 | s | i | t | t | i | n | g |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| k | 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| i | 2 | 2 | 1 | 2 | 3 | 4 | 5 | 6 |
| t | 3 | 3 | 2 | **1** | 2 | 3 | 4 | 5 |
| t | 4 | 4 | 3 | 2 | **1** | 2 | 3 | 4 |
| e | 5 | 5 | 4 | 3 | 2 | **2** | 3 | 4 |
| n | 6 | 6 | 5 | 4 | 3 | 3 | **2** | 3 |

### Pseudocode
The general idea of this 2D setup would be that for any specific cell we are on, we need to find the `min(adjacent)` cell and add 1 if our current cells column and row don't match, and 0 if they do

```python
dp = [[0 for i in range(len(str2) + 1)] for _ in range(len(str1) + 1)]

# fill left column
for i in range(len(str1) + 1):
    dp[i][0] = i

# fill top row
for i in range(len(str2) + 1):
    dp[0][i] = i

for row in range(1, len(str1) + 1):
    for col in range(1, len(str2) + 1):
        dp[row][col] = min(
            dp[row - 1][col - 1], 
            dp[row - 1][col],
            dp[row][col - 1]
        ) + (0 if str1[row - 1] == str2[col - 1] else 1)
        
return(dp[-1][-1])
```

Why? Why does this make sense? Step by step it might make more sense
- We fill all of the initial rows and columns with incremental sequence, this is equivalent to saying
    - "if I have the word "k" it would take 1 insert from a null string"
    - "if I have the word "ki" it would take 2 inserts",
    - etc... so these are showcasing to get to `str1` from a null word, it would take the length of that word (inserts)
- Once this is done, we're ready to go and fill in each cell
    - We pass over each row, and check a number of cases in adjacent cells
        - `[-1][-1]` would be a substitution
            - If we're on cell `[3][3]`, and we are checking `sit` vs `kit`, we could substitute anything in these two cells 
            - Since `t = t`, we don't need to add anything on, if it was `sit` vs `kid` then we can substitute something in and add an operation on which would be `dp[-1][-1] + 1`
        - `[-1][0]` would be a deletion where we would just remove the entry in the column 
            - It'd be deleting a character from `str1` to try and match `str2`
        - `[0][-1]` would be an insertion where we place a new cell in 
            - It'd be inserting a character into `str1` to match the next character in `str2`