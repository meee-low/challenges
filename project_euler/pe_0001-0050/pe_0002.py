# Problem 2: Even Fibonacci numbers

# Solution 1:
import functools

@functools.lru_cache(maxsize=5)
def fibonacci(n):
    # Returns the n-th fibonacci number.
    if n < 1:
        raise ValueError("Fibonacci is a sequence. No negative indexes allowed.")
    if n == 1:
        return 1
    if n == 2:
        return 2
    return fibonacci(n-2) + fibonacci(n-1)

s = 0
i = 1
while (f:=fibonacci(i)) <= 4_000_000:
    if f % 2 == 0:
        s += f
    i += 1
print(s)