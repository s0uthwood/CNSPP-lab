from .ZUC import left_rot
from .ECC import str2byte

k = [
    0x5A827999, # t in [0, 19]
    0x6ED9EBA1, # t in [20, 39]
    0x8F1BBCDC, # t in [40, 59]
    0xCA62C1D6  # t in [60, 79]
]

init_H = [
    0x67452301,
    0xEFCDAB89,
    0x98BADCFE,
    0x10325476,
    0xC3D2E1F0
]

def sha1_padding(m: bytes):
    m_len = len(m)
    m_bin = bin(int.from_bytes(m, 'big', signed=False))[2:].rjust(m_len * 8, '0')
    m_bin += '1'
    m_bin_len = len(m_bin)
    pad_len = (448 - m_bin_len) % 512
    m_bin += '0' * pad_len
    m_bin += bin(m_bin_len - 1)[2:].rjust(64, '0')
    return m_bin

def f_t(t, B, C, D):
    t //= 20
    if t == 0:
        return (B & C) | ((~B & 0xffffffff) & D)
    elif t == 1 or t == 3:
        return B ^ C ^ D
    elif t == 2:
        # return (B & C) | (B & D) | (C & D)
        return (B & C) ^ (B & D) ^ (C & D)
    else:
        raise ValueError("Wrong t")

def sha1_extend(m):
    w = []
    for t in range(16):
        w.append(int(m[t * 32: (t + 1) * 32], 2))
    for t in range(16, 80):
        w.append(left_rot(w[t - 3] ^ w[t - 8] ^ w[t - 14] ^ w[t - 16], 1, 32))
    return w


def sha1_compress(m, reg):
    # m is bin string, e.g. "010101"
    w = sha1_extend(m)
    # for _ in w:
    #     print (hex(_))
    A, B, C, D, E = reg
    for t in range(80):
        TEMP = (left_rot(A, 5, 32) + f_t(t, B, C, D) + E + w[t] + k[t // 20]) & 0xffffffff
        A, B, C, D, E = TEMP, A, left_rot(B, 30, 32), C, D
        # print ("%8x %8x %8x %8x %8x" % (A, B, C, D, E))
    reg[0] = (reg[0] + A) & 0xffffffff
    reg[1] = (reg[1] + B) & 0xffffffff
    reg[2] = (reg[2] + C) & 0xffffffff
    reg[3] = (reg[3] + D) & 0xffffffff
    reg[4] = (reg[4] + E) & 0xffffffff
    return reg

def sha1_calc(m: bytes):
    reg = [h for h in init_H]
    m = sha1_padding(m)
    n = len(m) // 512
    for i in range(n):
        reg = sha1_compress(m[i << 9: (i + 1) << 9], reg)
    digest = ''
    for r in reg:
        digest += hex(r)[2:].rjust(8, '0')
    return digest

def hmac_sha1(M: bytes, K: bytes, bit_len):
    if bit_len % 8 != 0:
        raise ValueError("wrong bit length")
    K += b'\x00' * (bit_len // 8 - len(K))
    K = int.from_bytes(K, 'big', signed=False)
    ipad = int("00110110" * (bit_len // 8), 2)
    # K_plus = int(bin(K)[2:].rjust(bit_len, '0'), 2)
    K_plus = K
    Si = K_plus ^ ipad
    tmp = sha1_calc(Si.to_bytes(bit_len // 8, 'big') + M)
    print (Si.to_bytes(bit_len // 8, 'big') + M)
    opad = int("01011100" * (bit_len // 8), 2)
    So = K_plus ^ opad
    return sha1_calc(So.to_bytes(bit_len // 8, 'big') + int(tmp, 16).to_bytes(20, 'big'))

def main():
    print (sha1_calc(b'abc'))
    print (sha1_calc(b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'))
    print (sha1_calc(b'aa' * 500000))
    print (hmac_sha1(b'Hi There', b'\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b', 160))

if __name__ == "__main__":
    main()
