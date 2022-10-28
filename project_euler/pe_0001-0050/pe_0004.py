# Problem 4: Largest palindrome product

# Solution 1
def is_palindrome(n:int) -> bool:
    str_n = str(n)
    return all(a == b for a, b in zip(str_n, str_n[::-1]))

best = 0

for i in range(999, 0, -1):
    if i * i < best:
        break
    for j in range(i, 0, -1):
        if is_palindrome(prod := i*j):
            if prod > best:
                best = prod
            break

print(best)