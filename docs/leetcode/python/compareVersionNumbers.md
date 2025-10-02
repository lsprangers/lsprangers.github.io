---
title: compareVersionNumbers
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# compareVersionNumbers

```python
class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        v1_split = version1.split(".")
        v2_split = version2.split(".")
        compareIdx = 0
        while compareIdx < len(v1_split) and compareIdx < len(v2_split):
            v1_part_cleaned = self.removeLeadingZeroes(v1_split[compareIdx])
            v2_part_cleaned = self.removeLeadingZeroes(v2_split[compareIdx])

            if v1_part_cleaned == v2_part_cleaned:
                compareIdx += 1
            elif v1_part_cleaned > v2_part_cleaned:
                return(1)
            else:
                return(-1)

        # If we're here, we've gotten to the end of at least 1 string

        # If we're at the end of both, and they're equal
        if len(v1_split) == len(v2_split) and compareIdx == len(v1_split):
            return(0)

        # If we've reached the end of 1, but not 2
        elif compareIdx == len(v1_split) and compareIdx != len(v2_split):
            # If any of the stuff left in v2 has a number, it's larger
            if any([self.removeLeadingZeroes(x) != 0 for x in v2_split[compareIdx:]]):
                return(-1)
            else:
                return(0)

        # If we've reached the end of 2, but not 1
        elif compareIdx != len(v1_split) and compareIdx == len(v2_split):
            # If any of the stuff left in v2 has a number, it's larger
            if any([self.removeLeadingZeroes(x) != 0 for x in v1_split[compareIdx:]]):
                return(1)
            else:
                return(0)
        
        # This shouldn't happen
        return(-2)

    def removeLeadingZeroes(self, s) -> int:
        idx = 0
        s_arr = [c for c in s]
        while idx < len(s_arr) and s_arr[idx] == '0':
            idx += 1
        
        resp = "".join(s_arr[idx:])
        return(int(resp) if resp != "" else 0)
```