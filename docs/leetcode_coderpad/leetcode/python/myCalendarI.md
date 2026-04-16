---
title: myCalendarI
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# myCalendarI

```python
class MyCalendar:

    def __init__(self):
        self.bookings = SortedList()

    def book(self, startTime: int, endTime: int) -> bool:
        if len(self.bookings) < 1:
            self.bookings.add([startTime, endTime])
            return(True)
        
        # bisect_left means everything to the left is strictly less than
        # bisect_right means everything to the right is strictly greater than
        # [10, 20], [20, 30], [35,50]
        # inserting [15, 20] we would want to check placement based on 10, 15, 20
        #   bisect_right gives 1
        # inserting [10*, 25] bisect_left gives 1
        # inserting [10, 19] bisect_left gives 0
        bookingPlacement = bisect.bisect_right(self.bookings, [startTime, endTime])

        # If our bookingPlacement is 0, simply check to see if the current 0'th spot is
        #   going to have a start time overlapping with our endTime (only check 2nd condition)

        # If our booking placement is at the very end, we just need to check that the current last
        #   scheduled end time doesn't overlap with out start time (only check 1st condition)

        # If we're in the middle, check that both the placement behind us won't have an endTime greater
        #   than our start time, and check the placement in front of us won't have a startTime less than
        #   our end time
        if  (
                bookingPlacement > 0 and \
                self.bookings[bookingPlacement - 1][1] > startTime) or \
            (
                bookingPlacement < len(self.bookings) and 
                self.bookings[bookingPlacement][0] < endTime):
            return False

        self.bookings.add([startTime, endTime])
        return(True)
```