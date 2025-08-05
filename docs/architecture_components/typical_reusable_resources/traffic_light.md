---
title: In Memory Traffic Light Simulation
category: Implementations
difficulty: Advanced
show_back_link: true
---

# Traffic Light Simulation
Problem

You’re building a traffic light system at a pedestrian crosswalk.

There are two main event sources:

    Traffic light cycle: cycles through "GREEN" → "YELLOW" → "RED" in fixed time intervals.

    Pedestrian walk button: can be pressed at any time. The system should schedule a WALK phase after the next RED state.

Light Timings

    GREEN: 10 seconds

    YELLOW: 3 seconds

    RED: 7 seconds

    WALK: 5 seconds (only after RED, if button was pressed during GREEN or YELLOW)

System Behavior

    The light cycles automatically, starting with GREEN at t = 0.

    If the walk button is pressed during GREEN or YELLOW, the system will allow a WALK phase immediately after the next RED.

    Once WALK is shown, it is cleared (reset).

    No WALK is inserted if button was not pressed.

Required Methods

class TrafficLightSystem:
    def __init__(self):
        ...

    def tick(self, seconds: int) -> str:
        """Advance time by given seconds and return the current light state."""

    def press_button(self, timestamp: int):
        """Register a walk button press at a specific timestamp."""

Expected Output

You should model the state transitions internally and return the correct light phase on every tick. WALK only occurs after RED and only if someone pressed the button since last WALK.
Test Case

sys = TrafficLightSystem()

print(sys.tick(5))   # GREEN
sys.press_button(6)
print(sys.tick(5))   # now at 10s → YELLOW
print(sys.tick(3))   # now at 13s → RED
print(sys.tick(7))   # now at 20s → WALK should occur because button was pressed
print(sys.tick(5))   # now at 25s → back to GREEN
print(sys.tick(10))  # GREEN still
print(sys.tick(3))   # YELLOW
print(sys.tick(7))   # RED (no walk button pressed)
print(sys.tick(3))   # stays in GREEN (since no walk inserted)


Phase Order Logic
State	Duration (s)	Transitions To
GREEN	10	YELLOW
YELLOW	3	RED
RED	7	WALK (if requested) or GREEN
WALK	5	GREEN
🛠️ Suggested Internal Structure

Use:

    A cycle timer with modulo logic or absolute phase end times

    A walk_requested boolean

    Track total current_time

    Reset walk_requested = False after WALK

🧠 Extra Credit Ideas

If you want to make it more complex on the plane:

    Add multiple walk buttons (per direction)

    Prevent double pressing

    Log all transitions as an event stream