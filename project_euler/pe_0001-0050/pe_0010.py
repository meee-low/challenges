# Problem 10: Summation of primes

# Solution 1
from utils.number_theory import primes_up_to_n

n = 2_000_000
print(primes_up_to_n(n).sum())