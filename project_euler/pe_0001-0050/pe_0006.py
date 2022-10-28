# Problem 6: Sum square difference

# Solution 1: numpy
import numpy as np
first_100_numbers = np.arange(1, 100+1)
print(first_100_numbers.sum() ** 2 - (first_100_numbers ** 2).sum())