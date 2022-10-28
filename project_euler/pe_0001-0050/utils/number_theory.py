import numpy as np
import math
from numba import njit

def primes_up_to_n(n) -> np.array:
    """
    Returns a numpy array of primes up to n.
    
    >>> primes_up_to_n(1)
    Traceback (most recent call last):
        ...
    ValueError: `n` must be 2 or higher.
    >>> primes_up_to_n(2)
    array([2])
    >>> primes_up_to_n(3)
    array([2, 3])
    >>> primes_up_to_n(20)
    array([ 2,  3,  5,  7, 11, 13, 17, 19], dtype=int64)
    >>> primes_up_to_n(100)
    array([ 2,  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97], dtype=int64)
    >>> primes_up_to_n(-1)
    Traceback (most recent call last):
        ...
    ValueError: `n` must be 2 or higher.
    >>> primes_up_to_n(3.5)
    Traceback (most recent call last):
        ...
    ValueError: `n` has to be an integer value.
    """
    if n < 2:
        raise ValueError("`n` must be 2 or higher.")
    if math.floor(n) != n:
        raise ValueError("`n` has to be an integer value.")
    if n == 2:
        return np.array([2])
    if n == 3:
        return np.array([2, 3])
    
    sieve = np.arange(3, n+1, 2, dtype='int64')
    for i, m in enumerate(sieve):
        if m > 0:
            sieve[i+m::m] = 0
    primes = np.concatenate((np.array([2]), sieve[sieve>0]))
    return primes


# def prime_factors(n:int) -> np.array:
#     """
#     Returns a numpy array of all numbers < n that are divisors of n.
    
#     >>> prime_factors(2)
#     array([2])
#     >>> prime_factors(10)
#     array([2, 5])
#     """
#     # limit = math.floor(math.sqrt(n))
#     if n in [2, 3]:
#         return np.array([n])
#     limit = n // 2
#     primes = primes_up_to_n(limit)
#     factors = primes[n % primes == 0]
#     if len(factors) == 0 and n >= 2:
#         # n itself has no factors less than it, so it's prime.
#         return np.array([n])
#     return factors

# @njit
def prime_factors(n:int) -> np.array:
    """
    Returns a numpy array of all numbers < n that are divisors of n.
    
    >>> prime_factors(2)
    array([2])
    >>> prime_factors(10)
    array([2, 5])
    """
    limit = max(n//2 + 1, 5)
    divisors = []
    while n % 2 == 0:
        n = n // 2
        divisors.append(2)
    for i in range(3, limit, 2): 
        while n % i == 0:
            n = n // i
            divisors.append(i)
        if n == 1:
            break
    return np.unique(divisors)

def is_prime(n:int) -> bool:
    """
    Returns True if n is prime.
    
    >>> is_prime(10)
    False
    >>> is_prime(2)
    True
    >>> is_prime(1)
    False
    """
    if n in [0, 1]:
        return False
    # Alternative: return all(n % i != 0 for i in range(2, n//2 + 1))
    return len(prime_factors(n)) == 1

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # print(prime_factors(10))