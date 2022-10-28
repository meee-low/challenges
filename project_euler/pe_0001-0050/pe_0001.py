# Problem 1 - Multiples of 3 or 5

# Solution 1: simple loop and accumulation
s = 0
for i in range(1000):
    if i % 3 == 0 or i % 5 == 0:
        s += i
print(s)

# Solution 1.2: bad one-liner mess
print(sum(filter(lambda x: x % 3 == 0 or x % 5 == 0, range(1000))))

# Solution 1.3: bad one-liner mess with list-comprehension
print(sum(i for i in range(1000) if (i % 3 == 0 or i % 5 == 0)))

# Solution 2: numpy approach
import numpy as np
arr = np.arange(1000)
bool_arr = np.logical_or(arr % 3 == 0, arr % 5 == 0)
print(arr[bool_arr].sum())

# Solution 3: find the pattern
first_15 = sum(i for i in range(3*5) if (i % 3 == 0 or i % 5 == 0))
d, r = divmod(1000, 15)
print(sum(first_15 * i for i in range(1,d+1)))

print(sum(i for i in range(3*5, 3*5*2) if (i % 3 == 0 or i % 5 == 0)))