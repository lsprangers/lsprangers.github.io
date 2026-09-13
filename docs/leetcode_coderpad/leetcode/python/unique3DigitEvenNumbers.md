---
title: unique3DigitEvenNumbers
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# unique3DigitEvenNumbers

```python
class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        seen = set()

        for idx1 in range(len(digits)):
            for idx2 in range(len(digits)):
                for idx3 in range(len(digits)):
                    if idx1 == idx2 or idx1 == idx3 or idx2 == idx3 or digits[idx3] % 2 == 1:
                        continue

                    num = (digits[idx1] * 100) + (digits[idx2] * 10) + digits[idx3]
                    if num < 100:
                        continue
                    
                    seen.add(num)           
        
        return(len(seen))
```