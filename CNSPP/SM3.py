from ZUC import left_rot

init_iv = 0x7380166f4914b2b9172442D7DA8A0600A96F30BC163138AAE38DEE4DB0FB0E4E
T = [0x79cc4519] * 16 + [0x7a879d8a] * 48

def FF(j, X, Y, Z):
    if j < 16:
        return X ^ Y ^ Z
    else: 
        return (X & Y) | (X & Z) | (Y & Z)

def GG(j, X, Y, Z):
    if j < 16:
        return X ^ Y ^ Z
    else:
        return (X & Y) | ((~X & 0xffffffff) & Z)

def P0(X):
    return X ^ left_rot(X, 9, 32) ^ left_rot(X, 17, 32)

def P1(X):
    return X ^ left_rot(X, 15, 32) ^ left_rot(X, 23, 32)

def sm3_padding(m: bytes):
    m_len = len(m)
    m_bin = bin(int.from_bytes(m, 'big', signed=False))[2:].rjust(m_len * 8, '0')
    # print (m_bin)
    m_bin += '1'
    # print (m_bin)
    m_bin_len = len(m_bin)
    pad_len = (448 - m_bin_len) % 512
    m_bin += '0' * pad_len
    # print (m_bin)
    m_bin += bin(m_bin_len)[2:].rjust(64, '0')
    # print (m_bin)
    return m_bin

def sm3_extend(m):
    # len(m) = 512bit
    # type(m) = string
    w1 = []
    w2 = []
    for i in range(16):
        w1.append(int(m[i * 32 : (i + 1) * 32], 2))
    for i in range(16, 68):
        w1.append(P1(w1[i - 16] ^ w1[i - 9] ^ left_rot(w1[i - 3], 15, 32)) ^ left_rot(w1[i - 13], 7, 32) ^ w1[i - 6])
    for i in range(64):
        w2.append(w1[i] ^ w1[i + 4])
    return w1, w2

def sm3_compress(m, reg):
    w1, w2 = sm3_extend(m)
    ss1 = 0
    ss2 = 0
    A, B, C, D, E, F, G, H = reg
    for j in range(64):
        ss1 = left_rot((left_rot(A, 12, 32) + E + left_rot(T[j], j, 32)) & 0xffffffff, 7, 32)
        ss2 = ss1 ^ left_rot(A, 12, 32)
        tt1 = (FF(j, A, B, C) + D + ss2 + w2[j]) & 0xffffffff
        tt2 = (GG(j, E, F, G) + H + ss1 + w1[j]) & 0xffffffff
        A, B, C, D, E, F, G, H = tt1, A, left_rot(B, 9, 32), C, P0(tt2), E, left_rot(F, 19, 32), G
    reg[0] ^= A
    reg[1] ^= B
    reg[2] ^= C
    reg[3] ^= D
    reg[4] ^= E
    reg[5] ^= F
    reg[6] ^= G
    reg[7] ^= H
    return reg

def sm3_calc(m):
    reg = []
    for i in range(8):
        reg.append((init_iv >> ((7 - i) * 32)) & 0xffffffff)
    m_new = sm3_padding(m)
    n = len(m_new) // 512
    # print (len(m_new))
    for i in range(n):
        reg = sm3_compress(m_new[i << 9:(i + 1) << 9], reg)
    digest = ''
    for r in reg:
        digest += hex(r)[2:].rjust(8, '0')
    return digest

if __name__ == "__main__":
    # print (sm3_padding(b'abc'))
    print (sm3_calc(b'abc'))
    print (sm3_calc(b'\x33\x66\x77\x99\x00'))
    print (sm3_calc(b'\xf4\xa3\x84\x89\xe3+E\xb6\xf8v\xe3\xac!h\xca9#b\xdc\x8f#E\x9c\x1d\x11F\xfc=\xbf\xb7\xbc\x9amessage digest'))