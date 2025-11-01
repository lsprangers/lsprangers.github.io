---
title: capacityToShipPackagesWithinDDays
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# capacityToShipPackagesWithinDDays

Review:
`check()` function here needs to run in $O(n)$ time, and does! This is basically just a rolling sum

`capacity = 10`
`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` 
`[1, 3, 6, 10]` - at next weight `current_load + weight > capacity`, and so we'll bump up required days to 2 and `curr = 6`

At end of the function just need to ensure our number of days used is less than or at the days provisioned

```
def check(self, weights: List[int], capacity: int, days: int) -> bool:
    required_days = 1
    current_load = 0

    for weight in weights:
        if current_load + weight > capacity:
            required_days += 1
            current_load = 0
        current_load += weight

    return required_days <= days
```


## Answer Space:
The rest of the `shipWithinDays` is just a classical binary search problem, but it touches almost every single edge case on the planet...

- If you start with `low = 0` instead of `low = max(weights)` then you are ***expanding the answer space*** and you'll get the wrong answer
    - The answer space, at maximum, ranges from `[max_weight, all_weight]`
    - For example, if you have `capacity = 3` and one of our weights is `4`, you will hit an edge case in the `check()` portion `current_load + weight > capacity:` and we'll get incorrect results
- Imagine weights = `[5, 8, 2]`
    - If you test capacity = 0, no weight can ever be shipped
    - If you test capacity = 4, same — it’s invalid
    - Your check() will keep returning False, and your binary search will spend time narrowing down values that can never be correct
---

## Solution
```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        low = max(weights)
        # capacity largest size would be entire list in 1 day
        high = sum(weights)
        

        while low < high:
            mid = (low + high) // 2

            # meaning this capacity is enough
            if self.check(weights, mid, days):
                # if capacity is enough, let's shrink search space to lower
                high = mid
            else:
                # if not enough raise it
                low = mid + 1
                
        return(low)

    def check(self, weights: List[int], capacity: int, days: int) -> bool:
        required_days = 1
        current_load = 0

        for weight in weights:
            if current_load + weight > capacity:
                required_days += 1
                current_load = 0
            current_load += weight

        return required_days <= days
```