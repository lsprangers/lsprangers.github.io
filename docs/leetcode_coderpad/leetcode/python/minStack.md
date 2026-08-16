---
title: minStack
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# minStack

Cheating with a heap
```python
class MinStack:

    def __init__(self):
        self.minHeap = []
        self.stack = []

    def push(self, value: int) -> None:
        self.stack.append(value)
        heapq.heappush(self.minHeap, value)
        return
        
    def pop(self) -> None:
        curr = self.stack.pop()
        self.minHeap.remove(curr)
        heapq.heapify(self.minHeap)
        return

    def top(self) -> int:
        return(self.stack[-1])

    def getMin(self) -> int:
        return(self.minHeap[0])
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(value)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```


```python
class MinStack:

    def __init__(self):
        self.stack = []

    def push(self, value: int) -> None:
        if not self.stack:
            self.stack.append((value, value))
            return

        currMin = self.stack[-1][1]
        self.stack.append((value, min(currMin, value)))

    def pop(self) -> None:
        self.stack.pop()
        
    def top(self) -> int:
        return(
            self.stack[-1][0]
        )

    def getMin(self) -> int:
        return(
            self.stack[-1][1]
        )        
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(value)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```