---
title: GCD
category: Implementations
difficulty: Advanced
show_back_link: true
---

# GCD

GCD is just the multiple of common prime factors
12 = 2 * 2 * 3
20 = 2 * 2 * 5
GCD = 2 * 2 = 4
36 = 2 * 2 * 3 * 3
60 = 2 * 2 * 3 * 5
GCD = 2 * 2 * 3 = 12
Walkthrough:
a = 36, b = 60
60 % 36 = 24 (this is remainder)
stack call --> [gcd(36, 60), gcd(24, 36)]
a = 24, b = 36
36 % 24 = 12 (this is remainder)
stack call --> [gcd(24, 12), gcd(36, 60), gcd(24, 36)]
a = 12, b = 24
24 % 12 = 0 (this is remainder)
stack call --> [gcd(0, 12), gcd(24, 12), gcd(36, 60), gcd(24, 36)]
this will finally return, and we'll have 12

```python
def getGCD(a, b):
    if a == 0:
        return(b)
    
    return getGCD(b % a, a)

if __name__ == "__main__":
    assert(getGCD(12, 20) == 4)
    assert(getGCD(36, 60) == 12)
    assert(getGCD(-1, -1) == -1)       
```