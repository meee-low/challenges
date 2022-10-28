# Problem 3: Largest prime factor

# Solution 1:
from utils.number_theory import prime_factors
import numpy as np
# from numba import njit

print(prime_factors(600851475143).max())