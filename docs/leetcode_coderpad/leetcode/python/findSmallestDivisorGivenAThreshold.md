---
title: findSmallestDivisorGivenAThreshold
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# findSmallestDivisorGivenAThreshold

```python
class Solution:
    def smallestDivisor(self, nums: List[int], threshold: int) -> int:
        # smallest integer divisor is 1
        left = 1
        # largest is max of nums
        #   it will make all other numbers a fraction (1), and the largest number 1 as well
        #   we know threshold >= nums.length, so if everything was 1 the sum
        #   would be equal to nums.length
        right = max(nums)
        
        # we're trying to find max
        while left < right:
            mid = left + (right - left) // 2
            # if our divisor is too small, and the sum is larger than threshold
            #   we should reduce search space to make divisor larger, ultimately
            #   bringing total sum downwards
            if self.check(nums, mid) > threshold:
                left = mid + 1
            # if our total sum is less than or equal to the threshold
            #   then our divisor choice was too large and we need to reduce
            #   the overall search space
            else:
                right = mid
        
        return(right)
    
    def check(self, nums, divisor) -> int:
        resp = 0
        for n in nums:
            resp += math.ceil(n / divisor)
        
        return(resp)
```