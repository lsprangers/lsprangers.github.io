---
title: slidingWindowMaximum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# slidingWindowMaximum

Summary:
- We use a monotonic decreasing deque, which implies that the first element is the maximum.
- Once the maximum element is too far to stay in the window we remove it from the deque, and the next greatest element moves to position 0.
- To maintain the decreasing order, we remove elements from the deque that are smaller than the elements being added.


```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if len(nums) < 1:
            return(nums)
        if len(nums) < k:
            return([max(nums)])
        
        resp = []
        # tried using max(window) but got a TLE

        # need to notice that if we ever encounter a number to the right larger
        #   than something on the left, we can completely ignore the left
        dec_stack = deque([])

        # setup for initial window
        for right in range(k):
            while dec_stack and nums[right] >= nums[dec_stack[-1]]:
                dec_stack.pop()
            
            dec_stack.append(right)
        
        resp.append(nums[dec_stack[0]])

        # sliding window with monotonic deque
        for right in range(k, len(nums)):
            # while outisde of window range
            # an index of 1 should not be included if 
            #   we're at index 4 with size 3
            #   it should be 4, 3, 2
            while dec_stack and right - k >= dec_stack[0]:
                dec_stack.popleft()

            while dec_stack and nums[right] >= nums[dec_stack[-1]]:
                dec_stack.pop()
            
            dec_stack.append(right)
            
            resp.append(nums[dec_stack[0]])
        
        return(resp)
```