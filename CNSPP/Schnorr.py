# TODO: unfinished

from .RSA import get_prime as _get_prime
from .utils import my_pow as _my_pow, inverse as _inverse
from .ECC import int2byte as _int2byte
import random as _random
import hashlib as _hashlib

def schnorr_key_gen():
    p = _get_prime(1024)
    while True:
        q = _get_prime(160)
        if (p - 1) % q == 0:
            break
    while True:
        g = _random.randint(2, p - 1)
        if _my_pow(g, q, p) == 1:
            break
    x = _random.randint(2, q - 1)
    y = _my_pow(g, x, p)
    return p, q, g, x, y

def schnorr_sign(msg, p, q, g, x):
    k = _random.randint(2, q - 1)
    r = _my_pow(g, k, p)
    if type(msg) == str:
        msg = msg.encode()
    e = _hashlib.md5(_int2byte(r) + msg).hexdigest()
    s = (k + x * int(e, 16)) % q
    return e, s, msg

def schnorr_verify(msg, e, s, p, q, g, y):
    r = _my_pow(g, s, p) * _inverse(_my_pow(y, e, p), p) % p
    if type(msg) == str:
        msg = msg.encode()
    h = _hashlib.md5(_int2byte(r) + msg).hexdigest()
    if h == e:
        return True
    return False
