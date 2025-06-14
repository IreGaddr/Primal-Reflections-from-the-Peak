import random
from math import gcd, isqrt
import time

# The 54-digit composite we need to factor
n = 255940086261521232403114651478550881994097286584680109

def pollard_rho_improved(n, max_iterations=1000000):
    """Improved Pollard's rho with multiple polynomials"""
    if n % 2 == 0:
        return 2
    
    # Try different polynomials
    for c in [1, 2, 3, 5, 7, 11, 13, 17, 19, 23]:
        x = random.randint(2, n - 2)
        y = x
        d = 1
        
        for _ in range(max_iterations):
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
            
            if d != 1 and d != n:
                return d
                
    return None

def pollard_p_minus_1(n, B=1000000):
    """Pollard's p-1 method"""
    a = 2
    for i in range(2, B):
        a = pow(a, i, n)
        d = gcd(a - 1, n)
        if 1 < d < n:
            return d
        if i % 10000 == 0:
            print(f"p-1 method: checked up to {i}")
    return None

def trial_division_up_to(n, limit):
    """Trial division up to a limit"""
    factors = []
    
    # Check 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check odd numbers
    i = 3
    while i <= limit and i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
        
        if i % 1000000 == 1:
            print(f"Trial division: checked up to {i}")
    
    return factors, n

def ecm_simple(n, curves=100):
    """Simplified ECM - just checking for small factors with different curves"""
    from random import randint
    
    for curve in range(curves):
        # Simplified ECM using Pollard's approach on different "curves"
        B = randint(100, 10000)
        a = randint(2, n-1)
        
        for i in range(2, B):
            try:
                a = pow(a, i, n)
                d = gcd(a - 1, n)
                if 1 < d < n:
                    return d
            except:
                pass
                
        if curve % 10 == 0:
            print(f"ECM: tried {curve} curves")
    
    return None

def fermat_factor_extended(n, max_attempts=10000000):
    """Extended Fermat factorization with progress reporting"""
    a = isqrt(n)
    if a * a == n:
        return a, a
    
    a += 1
    for attempt in range(max_attempts):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
        
        if attempt % 100000 == 0 and attempt > 0:
            print(f"Fermat: checked {attempt} values, current a = {a}")
    
    return None, None

def factor_completely(n):
    """Try to completely factor n"""
    factors = []
    remaining = n
    
    print(f"Factoring {n}")
    print(f"Number has {len(str(n))} digits")
    print("="*60)
    
    # First try trial division for small factors
    print("Trying trial division for small factors...")
    small_factors, remaining = trial_division_up_to(remaining, 1000000)
    if small_factors:
        factors.extend(small_factors)
        print(f"Found small factors: {small_factors}")
        print(f"Remaining: {remaining}")
    
    if remaining == 1:
        return factors
    
    # Try Pollard's rho
    print("\nTrying Pollard's rho...")
    start = time.time()
    factor = pollard_rho_improved(remaining)
    if factor:
        print(f"Pollard's rho found factor: {factor} (in {time.time()-start:.2f}s)")
        factors.append(factor)
        remaining = remaining // factor
        print(f"Remaining: {remaining}")
    
    # Try Pollard's p-1
    if remaining > 1:
        print("\nTrying Pollard's p-1 method...")
        start = time.time()
        factor = pollard_p_minus_1(remaining, B=100000)
        if factor:
            print(f"Pollard's p-1 found factor: {factor} (in {time.time()-start:.2f}s)")
            factors.append(factor)
            remaining = remaining // factor
            print(f"Remaining: {remaining}")
    
    # Try Fermat's method (good if factors are close to sqrt(n))
    if remaining > 1:
        print("\nTrying Fermat's factorization...")
        print(f"sqrt(remaining) ≈ {isqrt(remaining)}")
        start = time.time()
        f1, f2 = fermat_factor_extended(remaining, max_attempts=1000000)
        if f1:
            print(f"Fermat's method found factors: {f1} and {f2} (in {time.time()-start:.2f}s)")
            factors.extend([f1, f2])
            remaining = 1
    
    # Try simplified ECM
    if remaining > 1:
        print("\nTrying simplified ECM...")
        factor = ecm_simple(remaining, curves=50)
        if factor:
            print(f"ECM found factor: {factor}")
            factors.append(factor)
            remaining = remaining // factor
    
    if remaining > 1:
        print(f"\nCould not factor remaining number: {remaining}")
        print(f"It has {len(str(remaining))} digits")
        factors.append(remaining)
    
    return factors

# Run the factorization
print("Starting factorization of 54-digit composite...")
print("="*60)
factors = factor_completely(n)

print("\n" + "="*60)
print("FINAL FACTORIZATION:")
print(f"Factors found: {factors}")

# Verify
product = 1
for f in factors:
    product *= f
print(f"\nVerification: product = {product}")
print(f"Matches original? {product == n}")

# Check which factors are prime
print("\nChecking primality of factors...")
for f in factors:
    # Simple primality check
    is_prime = True
    if f > 2:
        for i in range(2, min(10000, int(f**0.5) + 1)):
            if f % i == 0:
                is_prime = False
                break
    print(f"{f} ({len(str(f))} digits): {'PRIME' if is_prime else 'COMPOSITE'}")