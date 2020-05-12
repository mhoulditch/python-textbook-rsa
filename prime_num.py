import math, random

def prime_sieve(size):
    ''' a list of prime numbers using sieve of eratosthenes '''

    sieve = [True] * size

    # exceptions
    sieve[0] = False
    sieve[1] = False

    #create the sieve
    for i in range(2, int(math.sqrt(size)) + 1):
        pointer = i * 2
        while pointer < size:
            sieve[pointer] = False
            pointer += i
    # compile the list of primes
    primes = []
    for i in range(size):
        if sieve[i] == True:
            primes.append(i)

    return primes

def rabin_miller(num):
    # R.M. doesn't work on even ints
    if num % 2 == 0 or num < 2:
        return False
    if num == 3:
        return True
    s = num - 1
    t = 0

    # halve until it is odd. count how many times we halve.
    while s % 2 == 0:
        s = s // 2
        t += 1
    # primality test 5 times
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        # exception if v is 1
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

LOW_PRIMES = prime_sieve(100)

def is_prime(num):
    if (num < 2):
        return False
    for prime in LOW_PRIMES:
        if (num % prime == 0):
            return False
    return rabin_miller(num)

def generate_large_prime(keysize=2048):
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if is_prime(num):
            return num
