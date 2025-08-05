---
title: In Memory Stream Join On UserID
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Stream Join On UserID
Problem

You’re given two input streams:

    click_stream(timestamp, user_id, page)

    purchase_stream(timestamp, user_id, item)

Join them such that for every click, you return the click and any purchases by the same user within the next 5 seconds.

Constraints

    You must keep a rolling buffer of clicks and purchases

    Each process(timestamp) step should check for joinable data and emit matching pairs

Expose:

    add_click(ts, uid, page)

    add_purchase(ts, uid, item)

    process(ts) -> List[Tuple[click, purchase]]

Test Case 1

joiner.add_click(10, "u1", "home")
joiner.add_purchase(12, "u1", "shoes")
joiner.add_click(15, "u2", "checkout")
joiner.add_purchase(18, "u1", "socks")
print(joiner.process(20))
# Should return:
# [
#   (("u1", "home"), ("u1", "shoes")),   # shoes is within 5s of home click
# ]

✈️ Bonus Setup for Offline Work

You can copy-paste this structure into your editor or notebook and implement each class with:

    Internal data structures (min-heaps, deques, hashmaps)

    Print debug output as needed (you won’t have a debugger in the air)
