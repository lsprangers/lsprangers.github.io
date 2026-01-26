---
title: prefixSum
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# prefixSum

```cpp
#include <vector>;
using namespace std;

class Solution {
public:
    vector<int> runningSum(vector<int>& nums) {
        vector<int> resp;
        resp.push_back(nums[0]);
        for(int i = 1; i < nums.size(); i++) {
            resp.push_back(nums[i] + resp[i-1]);
        }
        return(resp);
    }
};
```
