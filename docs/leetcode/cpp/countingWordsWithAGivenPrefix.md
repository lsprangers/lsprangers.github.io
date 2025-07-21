---
title: countingWordsWithAGivenPrefix
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# countingWordsWithAGivenPrefix

```cpp
// 2185
class Solution {
public:
    int prefixCount(vector<string>& words, string pref) {
        int resp = 0;
        for(string word : words) {
            if(hasPrefix(word, pref)) {
                resp++;
            }
        }
        return(resp);
    }
    bool hasPrefix(string word, string pref) {
        int idx = 0;
        while(idx < pref.size()) {
            if(word[idx] != pref[idx]) {
                return(false);
            }
            idx++;
        }
        return(true);     
    }
};
```
