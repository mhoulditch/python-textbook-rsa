# generate a public and private keypair

import random, sys, os, prime_num 

def gcd(a, b):
    ''' Euclidean algorithm '''
    # calculate b mod a, loop if a not 0,
    # multiple assignment trick swaps positions of b and a.
    # final val of b is GCD
    while a != 0:
        a,b = b % a, a
    return b

def find_mod_inverse(a, m):
    ''' return x such that a*x % m = 1 '''
    # numbers not relatively prime so modular inverse doesn't exist
    if gcd(a, m) != 1:
        return None

    # extended Euclidean algorithm
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = ( u1 - q * v1), (u2 - q * v2), \
            (u3 - q * v3), v1, v2, v3
    return u1 % m

def generate_key(key_size):
    ''' generate a public and private key pair using textbook RSA '''
    p = 0
    q = 0
    # generate large primes p and q to find n.
    while p == q:
        p = prime_num.generate_large_prime(key_size)
        q = prime_num.generate_large_prime(key_size)
    n = p * q
    # find e that is relatively prime to (p-1)*(q-1) 
    while True:
        e = random.randrange(2 ** (key_size - 1), 2 ** (key_size))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break
    # find the modular inverse of e 
    d = find_mod_inverse(e, (p - 1) * (q - 1))

    public_key = (n, e)
    private_key = (n, d)
    return (public_key, private_key)

# main function
# i.e. make_key_files('maxwell', 2048)
def make_key_files(name, key_size):
    ''' make textfiles for the public and private key pair '''
    if os.path.exists('{}_pubkey.txt'.format(name)) or \
    os.path.exists('{}_privkey.txt'.format(name)):
        sys.exit('keyfiles already exist with the name {}_pubkey.txt \
        or {}_privkey.txt'.format(name, name))

    public_key, private_key = generate_key(key_size)
    print('writing key files...')
    with open('{}_pubkey.txt'.format(name), 'w') as file:
        file.write('{},{},{}'.format(key_size, public_key[0], public_key[1]))


    with open('{}_privkey.txt'.format(name), 'w') as file:
        file.write('{},{},{}'.format(key_size, private_key[0], private_key[1]))
