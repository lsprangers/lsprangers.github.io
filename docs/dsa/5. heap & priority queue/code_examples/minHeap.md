


<!-- Collapsible Python snippet -->
<details>
  <summary>Show Python Script</summary>

```python
from typing import List

class minHeap:
    def __init__(self, heapList: List[int]):
        self.heapList = heapList
    
    def __len__(self):
        return(len(self.heapList))    
    
    def _swap_values(self, idx1: int, idx2: int):
        self.heapList[idx1], self.heapList[idx2] = self.heapList[idx2], self.heapList[idx1]
        return(self.heapList)
    
    def heapify(self):
        """Will update the array in place, and create
        a min heap based - hardcoded int for now

        Args:
            self.heapList (List[int]): Array / object to create a heap out of
        """
        n = len(self.heapList)
        
        # start at n // 2 as that will still cover all children
        #   at 2 * nodeIdx + 2 at the end - no need to start
        #   from last part of array
        for nodeIdx in range(n // 2, -1, -1):
            self.heapifyNode(nodeIdx)
    
    def heapifyNode(self, nodeIdx: int):
        """This will do the sifting-down portion
        where we start in the middle of the heap list,
        compare to children, and swap if any parent
        is larger than their child. If we swap a parent
        with child, we need to continue heapifying and
        checking the swapped parent (which is now a 
        child) and sift down the list
        
        Args:
            nodeIdx (int): _description_
        """
        # For each node, we want to check its children, and 
        # if the children's values are smaller than current, swap
        smallestIdx = nodeIdx
        leftIdx = (2 * nodeIdx) + 1
        rightIdx = (2 * nodeIdx) + 2

        if leftIdx < len(self.heapList) and self.heapList[leftIdx] < self.heapList[smallestIdx]:
            smallestIdx = leftIdx
        if rightIdx < len(self.heapList) and self.heapList[rightIdx] < self.heapList[smallestIdx]:
            smallestIdx = rightIdx

        # swap child with parent, and heapify parent
        if smallestIdx != nodeIdx:
            self._swap_values(smallestIdx, nodeIdx)
            self.heapifyNode(smallestIdx)

    def insert(self, newNum) -> None:
        """Inserts a number at the end of minHeap, and then swaps values
        with parent until heap property is met
        
        Literally just starts at bottom and "bubbles up" curr if it's less than parent

        Args:
            newNum (int): New number to add into heap
        """
        self.heapList.append(newNum)
        currIdx = len(self.heapList) - 1
        while currIdx > 0:
            parentIdx = (currIdx - 1) // 2
            if self.heapList[currIdx] < self.heapList[parentIdx]:
                self._swap_values(currIdx, parentIdx)
                currIdx = parentIdx
            else:
                break

    def deleteNode(self, num):
        """Delete a node from the heap.
        you will just move it to the end, pop it off, and then
        run heapify from where the num used to be

        Args:
            num (_type_): _description_
        """
        size = len(self.heapList)
        
        # find the index of the num
        numIdx = self.heapList.index(num)
        if numIdx == -1:
            return

        # Swap with the last element
        self._swap_values(numIdx, -1)
        self.heapList.pop()  # Remove the last element which is now the number to be deleted

        # Only run heapify if the deleted node was not the last node
        if numIdx < size - 1:
            self.heapifyNode(numIdx)

if __name__ == "__main__":
    heap = minHeap([3, 9, 2, 1, 4, 5])
    heap.heapify()
    print(heap.heapList)
    heap.insert(100)
    heap.insert(50)
    heap.insert(60)
    print(heap.heapList)
    heap.deleteNode(50)
    print(heap.heapList)
```    
</details>