import random
from math import gcd, isqrt

remaining = 16802022095139032644883792659417247160030463117297451566500667

# Pollard's rho algorithm - good for finding factors when p and q are similar in size
def pollard_rho(n, max_iterations=100000):
    if n % 2 == 0:
        return 2
    
    x = random.randint(2, n - 2)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    iterations = 0
    while d == 1 and iterations < max_iterations:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = gcd(abs(x - y), n)
        iterations += 1
    
    if d == n:
        return None  # Failed, try again with different values
    return d if d != 1 else None

# Try Pollard's rho multiple times with different seeds
print("Attempting Pollard's rho factorization...")
for attempt in range(10):
    factor = pollard_rho(remaining)
    if factor and factor != remaining:
        other_factor = remaining // factor
        print(f"\nFOUND FACTORIZATION!")
        print(f"Factor 1: {factor}")
        print(f"Factor 1 digits: {len(str(factor))}")
        print(f"Factor 2: {other_factor}")
        print(f"Factor 2 digits: {len(str(other_factor))}")
        print(f"Product check: {factor * other_factor == remaining}")
        break
    elif attempt % 3 == 0:
        print(f"Attempt {attempt + 1}: No factor found yet...")

# Also try ECM (Elliptic Curve Method) approach - simplified version
def simple_ecm_attempt(n, bound=10000):
    # Simplified ECM - checking if n is a perfect power
    for k in range(2, 100):
        root = int(n ** (1/k))
        for r in range(max(2, root - 1), root + 2):
            if r ** k == n:
                return r, k
    return None, None

print("\nChecking if it's a perfect power...")
base, exp = simple_ecm_attempt(remaining)
if base:
    print(f"It's {base}^{exp}!")

# Check proximity to perfect squares (might give hints about factor structure)
sqrt_n = isqrt(remaining)
print(f"\nProximity to perfect square:")
print(f"floor(sqrt(n))² = {sqrt_n**2}")
print(f"n - floor(sqrt(n))² = {remaining - sqrt_n**2}")
print(f"ceil(sqrt(n))² - n = {(sqrt_n + 1)**2 - remaining}")

# Fermat's factorization (works well if factors are close to sqrt)
def fermat_factor(n, max_attempts=100000):
    a = isqrt(n)
    if a * a == n:
        return a, a
    
    a += 1
    for _ in range(max_attempts):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
    return None, None

print("\nAttempting Fermat's factorization (good if factors are close)...")
f1, f2 = fermat_factor(remaining)
if f1:
    print(f"FOUND via Fermat's method!")
    print(f"Factor 1: {f1} ({len(str(f1))} digits)")
    print(f"Factor 2: {f2} ({len(str(f2))} digits)")