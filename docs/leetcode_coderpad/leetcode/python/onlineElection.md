---
title: onlineElection
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# onlineElection

```python
class TopVotedCandidate:

    def __init__(self, persons: List[int], times: List[int]):
        self.votes = defaultdict(int)
        self.leader = []
        currLeader = None
        
        # O(n)
        for idx in range(len(persons)):
            person = persons[idx]
            time = times[idx]
            self.votes[person] += 1
            
            if idx == 0 or self.votes[person] >= self.votes[currLeader]:
                self.leader.append((time, person))
                currLeader = person
            else:
                self.leader.append((time, currLeader))
            
        

    def q(self, t: int) -> int:
        # O(log n)
        idx = bisect.bisect_left(self.leader, t, key=lambda x: x[0])
        if idx > len(self.leader) - 1:
            return(self.leader[idx - 1][1])
        elif self.leader[idx][0] == t:
            return(self.leader[idx][1])
        else:
            return(self.leader[idx - 1][1])
        
        


# Your TopVotedCandidate object will be instantiated and called as such:
# obj = TopVotedCandidate(persons, times)
# param_1 = obj.q(t)
```