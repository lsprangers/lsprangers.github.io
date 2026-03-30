---
title: fruitsIntoBaskets
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# fruitsIntoBaskets

```python
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        resp = 0
        left = 0
        curr_fruits = defaultdict(int)
        curr_total = 0
        for right in range(len(fruits)):
            # 0
            this_fruit = fruits[right]
            if this_fruit in curr_fruits or len(curr_fruits.keys()) < 2:
                # {1: 2, 0: 1}
                curr_fruits[this_fruit] += 1
                # 3
                curr_total += 1
            
            # [1,0,1,4,1,4,1,2,3]
            # left = 0
            # right = 3
            else:
                # {1: 1}
                # left = 1
                while len(curr_fruits.keys()) == 2:
                    curr_fruits[fruits[left]] -= 1
                    curr_total -= 1
                    if curr_fruits[fruits[left]] == 0:
                        del curr_fruits[fruits[left]]
                    left += 1
                
                curr_fruits[this_fruit] += 1
                curr_total += 1
            
            resp = max(resp, curr_total)
        
        return(resp)        
```