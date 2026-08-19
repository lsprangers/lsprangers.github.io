---
title: cinemaSeatAllocation
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# cinemaSeatAllocation

```python
class Solution:
    def maxNumberOfFamilies(self, n: int, reservedSeats: List[List[int]]) -> int:
        reservedSeats.sort()
        nRowsWithReservations = 0

        # greedy
        seatPtr = 0
        resp = 0

        # go through all reserved seats
        while seatPtr < len(reservedSeats):
            nRowsWithReservations += 1
            currReservedRow = reservedSeats[seatPtr][0]

            reservedSeatsSet = set()
            while seatPtr < len(reservedSeats) and reservedSeats[seatPtr][0] == currReservedRow:
                reservedSeatsSet.add(reservedSeats[seatPtr][1])
                seatPtr += 1
            
            if not any([seat in reservedSeatsSet for seat in [2, 3, 4, 5]]) and not any([seat in reservedSeatsSet for seat in [6, 7, 8, 9]]):
                resp += 2
            elif not any([seat in reservedSeatsSet for seat in [2, 3, 4, 5]]):
                resp += 1
            elif not any([seat in reservedSeatsSet for seat in [4, 5, 6, 7]]):
                resp += 1
            elif not any([seat in reservedSeatsSet for seat in [6, 7, 8, 9]]):
                resp += 1
        
        resp += (n - nRowsWithReservations) * 2
        
        
        return(resp)
```