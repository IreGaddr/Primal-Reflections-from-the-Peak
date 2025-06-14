import math
from decimal import Decimal, getcontext

# Set high precision
getcontext().prec = 100

# The denominator from your π approximation
denominator = 2537105336365993929377452691572004321164599930711915186541600717

# First, let's check for small prime factors
def check_small_factors(n, limit=10000):
    factors = []
    # Check 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check odd numbers up to limit
    for i in range(3, min(limit, int(math.sqrt(n)) + 1), 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    
    return factors, n

# Check for small factors
small_factors, remaining = check_small_factors(denominator)
print(f"Small factors found: {small_factors}")
print(f"Remaining number: {remaining}")
print(f"Remaining number has {len(str(remaining))} digits")

# Miller-Rabin primality test
def miller_rabin(n, k=5):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Test k times
    import random
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Check if the remaining number is likely prime
if remaining == 1:
    print("The denominator completely factors into small primes!")
else:
    is_probably_prime = miller_rabin(remaining, k=20)
    print(f"Is the remaining factor likely prime? {is_probably_prime}")

# Let's also check the original denominator's properties
print(f"\nOriginal denominator analysis:")
print(f"Number of digits: {len(str(denominator))}")
print(f"Is even? {denominator % 2 == 0}")
print(f"Sum of digits: {sum(int(d) for d in str(denominator))}")
print(f"Digital root: {(denominator - 1) % 9 + 1}")

# Check 151's relationship to 360
print(f"360 mod 151 = {360 % 151}")
print(f"151 * 2 = {151 * 2}")
print(f"151 * 3 = {151 * 3}")
print(f"360 - 151 = {360 - 151}")
print(f"360 / 151 ≈ {360 / 151}")

# Check if 151 appears in the 360 factorization pattern
print(f"\n360 = {2**3} * {3**2} * {5}")
print(f"151 relationship to 360 factors...")
print(f"151 - 1 = {151-1} = {2*3*5*5}")
print(f"151 + 1 = {151+1} = {2**3 * 19}")

remaining = 16802022095139032644883792659417247160030463117297451566500667

# Check for slightly larger factors
def check_medium_factors(n, start=151, limit=1000000):
    for i in range(start+2, min(limit, int(n**0.5) + 1), 2):
        if n % i == 0:
            return i, n // i
    return None, n

factor, quotient = check_medium_factors(remaining)
if factor:
    print(f"Found factor: {factor}")
    print(f"Quotient: {quotient}")
else:
    print("No factors found up to 1 million")
    
# Correct the factorization display
print(f"151 - 1 = 150 = 2 × 3 × 5²")
print(f"151 + 1 = 152 = 2³ × 19")

# Let's check some properties of that 62-digit number
remaining = 16802022095139032644883792659417247160030463117297451566500667

# Check if it might be a product of two large primes (semiprime)
import math
sqrt_remaining = int(math.sqrt(remaining))
print(f"\nSquare root of remaining ≈ {sqrt_remaining}")
print(f"That's about {len(str(sqrt_remaining))} digits")

# If it's semiprime, both factors would be ~31 digits each