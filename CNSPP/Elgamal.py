from .utils import my_pow as _my_pow, gcd as _gcd, inverse as _inverse
from .RSA import get_prime
import random
import hashlib

def elgamel_key_gen(bit_size):
    p = get_prime(bit_size)
    g = 2
    x = random.randint(2, p - 3)
    y = _my_pow(g, x, p)
    return y, p, g, x

def elgamel_sign(msg, y, p, g, x):
    if type(msg) == str:
        msg = msg.encode()
    while True:
        k = random.randint(2, p - 3)
        if _gcd(k, p - 1) == 1:
            break
    h = hashlib.md5(msg).hexdigest()
    r = _my_pow(g, k, p)
    s = ((int(h, 16) - (x * r)) * _inverse(k, p - 1)) % (p - 1)
    return r, s, msg

def elgamel_verify(msg, s, r, y, p, g):
    if r <= 0 or r >= p:
        return False
    if s <= 0 or s >= p:
        return False
    if type(msg) == str:
        msg = msg.encode()
    h = hashlib.md5(msg).hexdigest()
    if _my_pow(g, int(h, 16), p) != (_my_pow(r, s, p) * _my_pow(y, r, p)) % p:
        return False
    return True

if __name__ == "__main__":
    y, p, g, x= elgamel_key_gen(256)
    msg = "Hello World!"
    r, s, msg = elgamel_sign(msg, y, p, g, x)
    print (elgamel_verify(msg, s, r, y, p, g))
