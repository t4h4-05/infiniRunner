def isEven(num: int|float) -> bool:
    return num & 1 == 0
def isOdd(num: int|float) -> bool:
    return num & 1 == 1
def isPrime(num: int|float) -> bool:
    if num <= 1:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True
def isPowerOfN(num: int|float, n: int|float) -> bool:
    # Handle edge cases
    if num <= 0 or n <= 0:
        return False
    if num == 1:
        return True
    if n == 1:
        return num == 1
        
    # Keep dividing by n until we can't anymore
    while num > 1:
        if num % n != 0:
            return False
        num /= n
    return num == 1

print(isPowerOfN(8, 2))
print(isPowerOfN(27, 3))
print(isPowerOfN(16, 4))
print(isPowerOfN(10, 2))
print(isPowerOfN(10, 3))

