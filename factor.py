import random
from math import isqrt, gcd

# The factors we need to check
factor1 = 65648263
factor2 = 255940086261521232403114651478550881994097286584680109

def trial_division(n, limit=None):
    """Check for small prime factors up to limit or sqrt(n)"""
    if n < 2:
        return False, []
    if n == 2:
        return True, [2]
    if n % 2 == 0:
        return False, [2]
    
    if limit is None:
        limit = isqrt(n) + 1
    
    factors = []
    for i in range(3, min(limit, isqrt(n) + 1), 2):
        if n % i == 0:
            factors.append(i)
            return False, factors
    
    return True, []

def miller_rabin(n, k=40):
    """Miller-Rabin primality test with k rounds"""
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
    
    # Witness loop
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

def lucas_lehmer_test(n):
    """Additional primality test for extra confidence"""
    if n == 2:
        return True
    if n % 2 == 0 or n < 2:
        return False
    
    # Find the first D such that Jacobi(D,n) = -1
    D = 5
    while True:
        g = gcd(abs(D), n)
        if g > 1 and g < n:
            return False
        if jacobi_symbol(D, n) == -1:
            break
        if D > 0:
            D = -(D + 2)
        else:
            D = -(D - 2)
    
    # Lucas sequence
    P, Q = 1, (1 - D) // 4
    
    # This is a simplified version - full test would be more complex
    return True  # Placeholder for full implementation

def jacobi_symbol(a, n):
    """Compute Jacobi symbol (a/n)"""
    if n <= 0 or n % 2 == 0:
        return 0
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == n % 4 == 3:
            result = -result
        a = a % n
    return result if n == 1 else 0

# Check the 8-digit factor
print("Checking 65648263...")
print(f"Number: {factor1}")
print(f"Digits: {len(str(factor1))}")

# Trial division for small factors
is_prime_trial, small_factors = trial_division(factor1, 10000)
if not is_prime_trial:
    print(f"Found factor via trial division: {small_factors[0]}")
else:
    print("No small factors found (up to 10000)")

# Miller-Rabin test
mr_result = miller_rabin(factor1, k=50)
print(f"Miller-Rabin test (50 rounds): {'PRIME' if mr_result else 'COMPOSITE'}")

# Check some properties
print(f"Fermat test (base 2): 2^{factor1-1} ≡ {pow(2, factor1-1, factor1)} (mod {factor1})")
print(f"Check Fermat (base 3): 3^{factor1-1} ≡ {pow(3, factor1-1, factor1)} (mod {factor1})")

print("\n" + "="*50 + "\n")

# Check the 54-digit factor
print("Checking 255940086261521232403114651478550881994097286584680109...")
print(f"Number has {len(str(factor2))} digits")

# For large number, we'll rely primarily on Miller-Rabin
print("Running Miller-Rabin test with 100 rounds...")
mr_result_large = miller_rabin(factor2, k=100)
print(f"Miller-Rabin test result: {'PRIME' if mr_result_large else 'COMPOSITE'}")

# Additional confidence tests
print("\nRunning additional primality tests for confidence...")

# Check Fermat's little theorem with several bases
fermat_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
fermat_pass = True
for base in fermat_bases:
    result = pow(base, factor2-1, factor2)
    if result != 1:
        print(f"FAILED Fermat test with base {base}: {base}^(n-1) ≡ {result} (mod n)")
        fermat_pass = False
        break

if fermat_pass:
    print(f"Passed Fermat's little theorem for all test bases: {fermat_bases}")

# Summary
print("\n" + "="*50)
print("SUMMARY:")
print(f"151: Known prime")
print(f"65648263: {'PRIME' if mr_result else 'COMPOSITE'}")
print(f"255940086261521232403114651478550881994097286584680109: {'PRIME' if mr_result_large else 'COMPOSITE'}")

if mr_result and mr_result_large:
    print("\nThe denominator factors as: 151 × 65648263 × [54-digit prime]")
    print("This creates a three-layer computational firewall!")