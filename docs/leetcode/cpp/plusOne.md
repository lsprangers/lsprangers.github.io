---
title: plusOne
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# plusOne

```cpp
// 66
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        int nSize = digits.size() - 1;
        if(digits[nSize] != 9) {
            digits[nSize]++;
            return(digits);
        }
        for(int i = nSize; i >= 0; i--) {
            if(digits[i] == 9) {
                digits[i] = 0;
            }
            else {
                digits[i]++;
                return(digits);
            }
        }

        vector<int> tmp = {1};
        tmp.insert( tmp.end(), digits.begin(), digits.end() );
        return(tmp);
    }
};
```
