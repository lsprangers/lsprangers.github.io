from collections import defaultdict
from typing import Dict, Tuple
import heapq

# We can DRY some things out with add and update, but I didn't want to go down that
#   rabbit hole during this imlpementation - there's definitely a good case for that though

class trendingTopics:
    def __init__(self):
        # intentionally don't use defaultdict, check everywhere
        #   topic --> (score, curr_version)
        self.curr_records: Dict[str, (int, int)] = {}
        self.prio_q = []
    
            
    def add(self, topic: str, score: int) -> None:
        if topic not in self.curr_records.keys():
            self.curr_records[topic] = (score, 0)
            heapq.heappush(self.prio_q, (-score, topic, 0))
            return
        
        curr_score = self.curr_records[topic][0]
        curr_version = self.curr_records[topic][1]
        new_score = curr_score + score
        new_version = curr_version + 1
        
        self.curr_records[topic] = (new_score, new_version)
        
        # in future, we can check curr_version + 1 against curr_records to
        #   ensure it's latest value
        # if we only use (new_score, topic), and the scores are the same, then 
        #   it may be a bad edge case
        # max queue so negative ONLY FOR PRIO Q
        heapq.heappush(self.prio_q, (-new_score, topic, new_version))
        return
    
    def top(self, k: int) -> None:
        if len(self.curr_records) < k:
            raise ValueError(f"We don't have {k} topics")

        resp = []
        helper_q = []
        while self.prio_q and len(resp) < k:
            curr = heapq.heappop(self.prio_q)
            # check versions
            curr_neg_score = curr[0]
            curr_topic = curr[1]
            curr_version = curr[2]
            # if is valid latest, drain
            if curr_version == self.curr_records[curr_topic][1]:
                resp.append(curr_topic)
                helper_q.append((curr_neg_score, curr_topic, curr_version))

        # regardless of errors or not, push valid ones back
        while helper_q:
            heapq.heappush(self.prio_q, helper_q.pop())
            
        if len(resp) < k:
            raise ValueError(f"We don't have {k} current topics")
        
        return(resp)
    
    def reset(self, topic: str) -> None:
        if topic not in self.curr_records.keys():
            raise ValueError(f"{topic} not in current records can't reset")
        
        curr_score = self.curr_records[topic][0]
        curr_version = self.curr_records[topic][1]
        new_score = 0
        new_version = curr_version + 1
        
        self.curr_records[topic] = (new_score, new_version)
        
        # in future, we can check curr_version + 1 against curr_records to
        #   ensure it's latest value
        # if we only use (new_score, topic), and the scores are the same, then 
        #   it may be a bad edge case
        heapq.heappush(self.prio_q, (-new_score, topic, new_version))    
        return
    