# Problem 5: Smallest multiple

# Solution 1:
from utils.number_theory import primes_up_to_n
import numpy as np

def smallest_multiple_of_all_under_n(n):
    primes = primes_up_to_n(n)
    powers = np.log(n) // np.log(primes)
    max_pure_powers = primes ** powers
    return int(max_pure_powers.prod())

print(smallest_multiple_of_all_under_n(20))