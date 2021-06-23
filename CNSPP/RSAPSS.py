from .SHA1 import sha1_calc as _sha1_calc
import random as _random
from .ECC import int2byte as _int2byte, byte2int as _byte2int, hex2byte as _hex2byte

HLEN = 20
HASH_FUNC = _sha1_calc

def byte_xor(a: bytes, b: bytes):
    if len(a) < len(b):
        a, b = b, a
    res = a[:len(a) - len(b)]
    for i, j in zip(a[-len(b):], b):
        res += (i ^ j).to_bytes(1, 'big')
    return res

def MGF(X, mask_len):
    if type(X) == str:
        X = X.encode()
    # HLEN = 20
    T = ''
    k = (mask_len + (HLEN - 1)) // HLEN + 1 # ceil{mask_len / HLEN} + 1
    for i in range(k):
        T = T + HASH_FUNC(X + i.to_bytes(4, 'little'))
    mask = T[:mask_len]
    return _hex2byte(mask)
    
def RSA_PSS_sign(msg, em_bits):
    # HLEN = 20
    slen = HLEN
    em_len = (em_bits + 7) // 8
    if type(msg) == str:
        msg = msg.encode()
    m_hash = _int2byte(int(HASH_FUNC(msg), 16))
    padding_1 = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    salt = _random.randint(0, 2 ** (2 * slen)).to_bytes(slen, 'little')
    M = padding_1 + m_hash + salt
    H = _hex2byte(HASH_FUNC(M))
    padding_2 = b'\x00' * (em_len - slen - HLEN - 2) + b'\x01'
    db = padding_2 + salt
    db_mask = MGF(H, em_len - HLEN - 1)
    # masked_db = _int2byte(_byte2int(db) ^ _byte2int(db_mask))
    masked_db = byte_xor(db, db_mask)
    zero_len = 8 * em_len - em_bits
    masked_db = (masked_db[0] % (1 << (8 - zero_len))).to_bytes(1, 'big') + masked_db[1:]
    em = masked_db + H + b'\xbc'
    return em

def RSA_PSS_verify(msg, em, em_bits):
    if type(msg) == str:
        msg = msg.encode()
    if type(em) == str:
        em = em.encode()
    em_len = (em_bits + 7) // 8
    slen = HLEN
    padding_1 = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    padding_2 = b'\x00' * (em_len - slen - HLEN - 2) + b'\x01'
    m_hash = _hex2byte(HASH_FUNC(msg))
    if em_len < HLEN + slen + 2:
        return False
    if em[-1] != 0xbc:
        return False
    masked_db = em[:em_len - HLEN - 1]
    h = em[em_len - HLEN - 1: -1]
    if masked_db[0] >> (8 - (8 * em_len - em_bits)) != 0:
        return False
    db_mask = MGF(h, em_len - HLEN - 1)
    # db = _int2byte(_byte2int(masked_db) ^ _byte2int(db_mask))
    db = byte_xor(masked_db, db_mask)
    zero_len = 8 * em_len - em_bits
    db = (db[0] % (1 << (8 - zero_len))).to_bytes(1, 'big') + db[1:]
    # print (db[:em_len - HLEN - slen - 1])
    # print (padding_2)
    if db[:em_len - HLEN - slen - 1] != padding_2:
        return False
    salt = db[-slen:]
    M = padding_1 + m_hash + salt
    # print (h)
    # print (_hex2byte(HASH_FUNC(M)))
    if h == _hex2byte(HASH_FUNC(M)):
        return True
    else:
        return False
    