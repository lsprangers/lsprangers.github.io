---
layout: technical
title: 3. Stacks & Queues
category: Data Structures & Algorithms
difficulty: Advanced
description: Stacks & Queues
show_back_link: true
---

# Stacks and Queues

## Stacks
Stacks are Last In First Out (LIFO) data structures, whose elements are only accessed and appended from last physical location - similar to a stack of plates in the kitchen!

Typical Operations:
- ***Push***: Add an element to the end
- ***Pop***: Access, and remove, element at the end
- ***Peek***: Look at / access element at the end

Most of the time we will use them in paired matching problems such as:
- [Valid Parenthesis](/docs/leetcode/python/validParenthesis.md)
- [Asteroid Collision](/docs/leetcode/python/asteroidCollision.md)

You can usually tell which problems require a stack, because it'd require you to move pointers forward and backwards based on matching conditions to new items

Other typical problems include matching elements together, querying some property such as "how far is the next largest element", evaluating a mathematical equation given as a string, just comparing elements against each other, or any other abstract interaction

Stacks and Recursion are highly linked, because Recursion is actually done using a Stack!

If we are at A below, and we do `A.left` and `A.right`, that's equivalent to `[A, B, C]` - we have `[A]`, then when we call `A.left` we go to `[A, B]`, and then our current scope and callstack are at `B`

We can continue down the chain and get to a callstack, repeatedly calling `node.left`, of `[A, B, D, F]` and once `F` returns our callstack is `[A, B, D]`
```
    A
B       C
D
F
```

### Implementation
Most stacks are implemented via[Doubly LinkedLists](/docs/dsa/4.%20linked%20lists/index.md) or Dynamic Arrays, so that we can have $O(1)$ implementations of Push, Pop, and Peek

With Dynamic Arrays, Push and Pop are amortized $O(1)$ because if there's a forced resize it would be $O(n)$, but these rarely happen in practice

```python
class DoublyLinkedListNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class Stack:
    def __init__(self):
        self.head = DoublyLinkedListNode()
        self.tail = DoublyLinkedListNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def push(self, val):
        new = DoublyLinkedListNode(val)

        # always use self.tail.prev b/c we want to push to empty stack
        prev = self.tail.prev 
        prev.next = new
        new.prev = prev
        new.next = self.tail        
        self.tail.prev = new
        return
    
    def peek(self):
        if self.tail.prev == self.head:
            raise IndexError("peek from empty stack")
        return(self.tail.prev.val)
    
    def pop(self):
        if self.tail.prev == self.head:
            raise IndexError("pop from empty stack")
        resp_node = self.tail.prev
        resp_prev = resp_node.prev
        resp_prev.next = self.tail
        self.tail.prev = resp_prev
        return(resp_node.val)
```

## Queue
FIFO!

Queue's are First In First Out - similar implementations to Stacks, except you would be inserting new items at the front (head)

While Stacks are able to use Dynamic Arrays OR Doubly Linked Lists, Queue's typically require a Doubly Linked List because inserting at the front of an array is $O(n)$

Queue Typical Operations:
- ***Enqueue***: Add an element to the front
- ***Dequeue***: Access, and remove, element at the end
- ***Peek***: Look at / access element at the end

This also allows us to create another data structure known as a ***Double Ended Queue (Deque)***, which is ultimately the same as a Queue, except you can enqueue and dequeue at either end

Deque Typical Operations:
- ***Enqueue Left***: Add an element to the front
- ***Dequeue Left***: Access, and remove, element at the front
- ***Enqueue Right***: Add an element to the end
- ***Dequeue Right***: Access, and remove, element at the end

The most typical use case of a Queue is [Breadth First Search (BFS)](/docs/dsa/8.%20trees%20&%20graphs/index.md)

There are other examples, like [Sliding Window Rate Limiter Counters](/docs/leetcode/python/numberOfRecentCalls.md), a [Moving Average In DataStream](/docs/leetcode/python/movingAverageInDatastream.md), or really anything that involves moving sliding windows (that aren't solvable by [TwoPointers](/docs/dsa/1.%20arrays%20&%20strings/index.md#two-pointers)!)

## Monotonic
A monotonic Stack or Queue is one whose elements are always ordered

These are typically useful when we have some criteria to find the "next" greatest or less than element, or some sort of criteria

```stack = [1, 5, 8, 15, 23]`
If we wanted to do `stack.push(14)`, we'd first need to pop off `[15, 23]`

```python
stack = []
for num in nums:
    while stack.length > 0 and stack.top >= num:
        stack.pop()
    # Between the above and below lines, do some logic depending on the problem
    stack.push(num)
```

A good example is [Daily Temperatures](/docs/leetcode/python/dailyTemperatures.md) where you continuously push items onto a stack until you come upon a larger one, and once you see that you pop items off stack that are smaller

If an item never gets off the stack, it's never seen a larger item (temperature)

This monotonic way is just a good method to find ***"for any item in the array, find the next larger item after it"*** AKA "next greatest item"

For a monotonic deque, the [Sliding Window Maximum](/docs/leetcode/python/slidingWindowMaximum.md) problem is a good example, but the reason we need a monotonic deque here is comparing "max", similar to temperature problem above, in a ranged window

Because of that max comparison, we need a monotonic deque