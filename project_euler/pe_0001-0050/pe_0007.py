# Problem 7: 10001st prime

# Solution 1:
from utils.number_theory import primes_up_to_n

import numpy as np
from numba import njit

print(primes_up_to_n(1_000_000)[10_000])