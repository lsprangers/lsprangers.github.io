---
title: longestIncreasingSubsequence (LIS)
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# longestIncreasingSubsequence (LIS)
In this dynamic programming problem, you'd start filling up the list from the back to the front, and along the way you'd just need to find the last max value where the number was greater than your current number

`[10,9,2,5,3,7,101,18]`
- At number 7 you can choose either 101 or 18, our longest subsequence is then 2
    - `dp = [1, 1, 1, 1, 1, 2, 1, 1]`
- At spot 3 you can choose 7, 101, or 18
    - Max is at spot 7
    - `dp = [1, 1, 1, 1, 3, 2, 1, 1]`
- 5 is same logic as 3
    - `dp = [1, 1, 1, 3, 3, 2, 1, 1]`
- So on and so forth until you get back to the front, and then you just find the `max(dp)` which will give us our longst subsequence

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)

        dp = [1] * n
        resp = 1

        # [10,9,2,5,3,7,101,18]
        # [1, 1,1,2,2,3,  4, 4]
        for idx in range(1, n):
            curr_largest_backwards = 0
            for backwards_idx in range(idx - 1, -1, -1):
                if nums[backwards_idx] < nums[idx]:
                    curr_largest_backwards = max(curr_largest_backwards, dp[backwards_idx])
            
            dp[idx] = 1 + curr_largest_backwards
            resp = max(resp, dp[idx])
        
        return(resp)
```

## Binary Search
There's a way to improve this with binary search, which is completely screwed up - for this you need to realize there's a way to get the increasing subsequence intelligently

`nums = [8, 1, 6, 2, 3, 10]`
- `sub = [8]`
- `sub = [1]`
    - This is where the `while num > sub[i]:` comes in
    - 1 is not greater than 8, so you replace 8 with 1
- `sub = [1, 6]`
- `sub = [1, 2]`
    - you see how this is greedy now, you will just take a smaller number for our subsequence if you can find it
- `sub = [1, 2, 3]`
    - If you kept 6, you couldn't have used 3
- `sub = [1, 2, 3, 10]`
- `resp = 4`

This will perform a linear scan through the subsequence if you cannot immediately append the number, and when doing so ***replace the first number larger than our current number***

This should be where you notice you can use binary search, instead of doing a linear scan to find the first lower bound value, you can use [Lower Bound First X Binary Search](/docs/dsa/6.%20binary%20search/index.md#lower-bound-first-valid-x)
```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = [nums[0]]
        
        # 
        for num in nums[1:]:
            # if able to be in subsequence, just append
            if num > sub[-1]:
                sub.append(num)
            else:
                # Find the first element in sub that is greater than or equal to num
                i = 0
                while num > sub[i]:
                    i += 1
                sub[i] = num

        return len(sub)
```



Binary Search implementation
- Note: `bisect_left(arr, x, lo=0, hi=len(arr))` will locate the insertion point for `x` to maintain a sorted order, this is an $O(N \dot \log(N))$ method for finding the first index to insert
- There's also a `bisect_right`, and `bisect` where `bisect` will find insertion point which comes after (to the right of) any entries of `x`

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []
        # O(n)
        for num in nums:
            #O(log n)
            i = bisect_left(sub, num)

            # If num is greater than any element in sub, just append
            if i == len(sub):
                sub.append(num)
            
            # Otherwise, replace the first element in sub greater than or equal to num
            else:
                sub[i] = num
        
        return len(sub)
```