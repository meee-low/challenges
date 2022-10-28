# Problem 9: Special Pythagorean triplet


# Solution 1
def find_special_pythagorean(n):
    for a in range(1, n):
        for b in range(a+1, n-a):
            c = (a ** 2 + b ** 2) ** 0.5
            if a + b + c ==  n:
                return int(a * b * c)
            
print(find_special_pythagorean(1000))