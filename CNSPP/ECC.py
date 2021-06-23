from .utils import inverse as _inverse, my_pow as _my_pow
import random as _random
from .SM3 import sm3_calc as _sm3_calc

def lucas(p, X, Y, k):
    delta = X * X - 4 * Y
    U = 1
    V = X
    k_bin = bin(k)[2:]
    k_binlen = len(k_bin)
    for i in range(1, k_binlen):
        U, V = U * V % p, ((V * V + delta * U * U) * (p + 1) // 2) % p # (p + 1) // 2 == _inverse(2, p)
        if k_bin[i] == '1':
            U, V = ((X * U + V) * (p + 1) // 2) % p, ((X * V + delta * U) * (p + 1) // 2) % p
    return U, V


class ECC_Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __str__(self):
        return f'({self.x}, {self.y})' # , curve: {self.curve}

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve == other.curve
    
    def __neg__(self):
        if self.is_infinity():
            return self
        return ECC_Point(self.x, -self.y % self.curve.p, self.curve)
    
    def __add__(self, other):
        if self.curve != other.curve:
            raise ValueError("not on same curve!")
        if self.is_infinity():
            return other
        if other.is_infinity():
            return self
        p = self.curve.p
        if self == other:
            if self.y == 0:
                return ECC_Point(None, None, self.curve)
            t = (3 * self.x * self.x + self.curve.a) * _inverse(2 * self.y, p) % p
        elif self.x == other.x and self.y != other.y:
            return ECC_Point(None, None, self.curve)
        else:
            t = (other.y - self.y) * _inverse(other.x - self.x, p) % p
        x = (t * t - self.x - other.x) % p
        y = (t * (self.x - x) - self.y) % p
        return ECC_Point(x, y, self.curve)

    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, times: int):
        if not self.is_on_curve():
            raise ValueError("not on curve!")
        if self.is_infinity():
            return self
        if times == 0:
            return ECC_Point(None, None, self.curve)
        is_neg = False
        if times < 0:
            is_neg = True
            times = -times
        tmp = self
        res = ECC_Point(None, None, self.curve)
        while times > 0:
            if times & 1 == 1:
                res += tmp
            tmp += tmp
            times >>= 1
        return -res if is_neg else res
    
    def __rmul__(self, times: int):
        return self.__mul__(times)

    def is_infinity(self):
        return self.x == None and self.y == None

    def is_on_curve(self):
        x, y = self.x, self.y
        a, b, p = self.curve.a, self.curve.b, self.curve.p
        return ((y * y) - (x ** 3 + a * x + b)) % p == 0

class Curve:
    def __init__(self, a, b, p, n, G_x, G_y):
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.G_x = G_x
        self.G_y = G_y

    def __str__(self):
        return f'y**2 = x**3 + {self.a}x + {self.b}, p = {self.p}, n = {self.n},G = ({self.G_x}, {self.G_y})'

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.p == other.p and self.n == other.n and self.G_x == other.G_x and self.G_y == other.G_y

    def calc_y(self, x):
        p = self.p
        x = (x * x * x + self.a * x + self.b) % p
        if p % 4 == 3:
            u = p // 4
            y = _my_pow(x, u, p)
            z = _my_pow(y, 2, p)
            if z == x:
                return y
            return None
        elif p % 8 == 5:
            u = p // 8
            z = _my_pow(x, 2 * u + 1, p)
            if z % p == 1:
                return _my_pow(x, u + 1, p)
            elif z % p == -1:
                return (2 * x * _my_pow(4 * x, u, p)) % p
            return None
        elif p % 8 == 1:
            u = p // 8
            while True:
                U, V = lucas(p, _random.randint(1, p - 1), x, 4 * u + 1)
                if V * V % p == 4 * x % p:
                    return (V * (p + 1) // 2) % p
                elif U % p != 1 and U % p != p - 1:
                    return None


SM2_Curve = Curve(
    0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC, # a 
    0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93, # b
    0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF, # p
    0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123, # n
    0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, # G_x
    0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0  # G_y
)

SM2_sign_Curve = Curve(
    0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498,
    0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A,
    0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3,
    0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7,
    0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,
    0x680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
)

test_Curve = Curve(
    -3,
    2455155546008943817740293915197451784769108058161191238065,
    6277101735386680763835789423207666416083908700390324961279,
    6277101735386680763835789423207666416083908700390324961279,
    602046282375688656758213480587526111916698976636884684818,
    174050332293622031404857552280219410364023488927386650641
)

Fp_192 = Curve(
    0xbb8e5e8fbc115e139fe6a814fe48aaa6f0ada1aa5df91985,
    0x1854bebdc31b21b7aefc80ab0ecd10d5b1b3308e6dbf11c1,
    0xbdb6f4fe3e8b1d9e0da8c0d46f4c318cefe4afe3b6b8551f,
    0xbdb6f4fe3e8b1d9e0da8c0d40fc962195dfae76f56564677,
    0x4ad5f7048de709ad51236de65e4d4b482c836dc6e4106640,
    0x02bb3a02d4aaadacae24817a4ca3a1b014b5270432db27d2
)

def str2int(s):
    n = 0
    for i in range(len(s)):
        n <<= 8
        n += ord(s[i])
    return n

def int2str(n):
    s = ''
    while n > 0:
        s = chr(n & 0xff) + s
        n >>= 8
    return s

def byte2int(b):
    return int.from_bytes(b, 'big', signed = False)

def int2byte(n, length = None):
    b = b''
    if length == None:
        length = len(hex(n)) - 2
        length = length // 2 + (length & 1)
    return n.to_bytes(length, 'big')

def str2byte(s):
    return s.encode('utf-8')

def hex2byte(a):
    return int2byte(int(a, 16))

def point2byte(P):
    x, y, curve = P.x, P.y, P.curve
    if x == 0 and y == 0:
        print ("[error] in point2byte: wrong point!")
        return
    X = int2byte(x, (len(hex(curve.p)[2:]) + 1) // 2)
    Y = int2byte(y, (len(hex(curve.p)[2:]) + 1) // 2)
    return b'\x04' + X + Y

def byte2point(b, curve):
    PC = b[0]
    b = b[1:]
    l = len(b) // 2
    x = byte2int(b[:l])
    y = byte2int(b[l:])
    return ECC_Point(x, y, curve)

def ECC_keygen(curve: Curve):
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    sk = _random.randint(1, curve.n - 1)
    pk = sk * G
    return sk, pk

def ECC_sharedkey(Q: ECC_Point, sk: int):
    return Q * sk

def ECC_encrypt_point(curve: Curve, M: ECC_Point, pk: ECC_Point):
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    k = _random.randint(1, curve.n)
    # k = 41
    C1 = k * G
    C2 = M + k * pk
    return C1, C2

def ECC_decrypt_point(curve: Curve, na: int, C1: ECC_Point, C2: ECC_Point):
    M = C2 - na * C1
    return M

def SM2_sign(ENTLA: bytes, IDA: bytes, curve: Curve, point: ECC_Point, msg: bytes, da):
    # point is public key
    Z = ENTLA + IDA + int2byte(curve.a) + int2byte(curve.b) + int2byte(curve.G_x) + int2byte(curve.G_y) + int2byte(point.x) + int2byte(point.y)
    Z = _sm3_calc(Z)
    M_hat = int2byte(int(Z, 16)) + msg
    # print (M_hat)
    # print (_sm3_calc(M_hat))
    e = int(_sm3_calc(M_hat), 16)
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    while True:
        # k = _random.randint(1, curve.n - 1)
        k = 0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
        P = k * G
        r = (e + P.x) % curve.n
        if r != 0 and r + k != curve.n:
            break
    s = _inverse(1 + da, curve.n) * (k - r * da) % curve.n
    return msg, r, s

def SM2_valid(curve: Curve, Z_A, P_A, M, r, s):
    if r <= 1 or r >= curve.n:
        return False
    if s <= 1 or s >= curve.n:
        return False
    M_hat = Z_A + M
    e = int(_sm3_calc(M_hat), 16)
    print (hex(e))
    t = (r + s) % curve.n
    print (hex(t))
    if t == 0:
        return False
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    vPoint = s * G + t * P_A
    print (hex(vPoint.x))
    print (hex(vPoint.y))
    R = (e + vPoint.x) % curve.n
    print (hex(R))
    if R == r:
        return True
    return False

def SM2_KDF(Z: bytes, klen):
    ct = 0x1
    v = 256
    if klen > (2 ** 32 - 1) * v:
        raise ValueError("@klen should smaller than (2 ** 32 - 1) * v")
    Ha = []
    for i in range((klen + v - 1) // v):
        # print (Z + ct.to_bytes(4, 'big'))
        Ha.append(hex2byte(_sm3_calc(Z + ct.to_bytes(4, 'big'))))
        ct += 1
    # print (Ha)
    if klen % v != 0:
        last_len = klen - (klen // v * v)
        mod_len = -last_len % 8
        Ha[-1] = (int.from_bytes(Ha[-1], 'big', signed = False) >> (v - last_len) << mod_len).to_bytes((last_len + mod_len) // 8, 'big')
    K = b''
    for h in Ha[:-2]:
        K += h
    K += Ha[-1]
    return K

def SM2_encrypt(msg, curve, db):
    klen = len(msg) * 8
    k = _random.randint(1, curve.n - 1)
    k = 0x384F30353073AEECE7A1654330A96204D37982A3E15B2CB5
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    C1 = k * G
    C1 = point2byte(C1)
    Pb = db * G
    tmp = k * Pb
    x2, y2 = tmp.x, tmp.y
    curvelen = (len(hex(curve.p)[2:]) + 1) // 2
    x2 = int2byte(x2, curvelen)
    y2 = int2byte(y2, curvelen)
    t = SM2_KDF(x2 + y2, klen)
    C2 = int2byte(byte2int(msg) ^ byte2int(t))
    C3 = hex2byte(_sm3_calc(x2 + msg + y2))
    return C1 + C3 + C2

def main():
    curve = Curve(2, 3, 17, 128, 1, 1)
    P = ECC_Point(2, 7, curve)
    Q = ECC_Point(11, 8, curve)
    print (P + Q)
    curve_b = Curve(2, 3, 97, 128, 1, 1)
    for i in range(6):
        print (ECC_Point(3, 6, curve_b) * i)
    # print (ECC_add(2, 3, 17, (2, 7), (11, 8)))
    # for i in range(6):
    # 	print (ECC_mul(2, 3, 97, i, (3, 6)))
    print (hex(str2int('abc')))
    print (int2str(0x616263))
    print (hex(byte2int(b'abc')))
    print (int2byte(0x616263))
    print (str2byte('abc'))
    curve_en = Curve(0, -4, 257, 129, 2, 2)
    G = ECC_Point(2, 2, curve_en)
    na = 101
    C1, C2 = ECC_encrypt_point(curve_en, ECC_Point(112, 26, curve_en), na * ECC_Point(2, 2, curve_en))
    print (C1)
    print (C2)
    print (ECC_decrypt_point(curve_en, na, C1, C2))
    # M = ECC_Point(2594161300049362469169638638781986485403377947559889224556, -915731655498392811604767074090214190962897463083669095347, test_Curve)
    # pk = ECC_Point(4535708181192800030922425040161683059768487875080759471914, -1061575060680846108649238340040410272066486614691829051119, test_Curve) * 273065013239976945911310331771
    # print (pk)
    # C1, C2 = ECC_encrypt_point(test_Curve, M, pk)
    # print (C1)
    # print (C2)
    print (curve_en.calc_y(112)) # 26 or 231
    public_key = ECC_Point(0x0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A, 0x7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857, SM2_sign_Curve)
    M, r, s = SM2_sign(b'\x00\x90', b'ALICE123@YAHOO.COM', SM2_sign_Curve, public_key, b'message digest', 0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263)
    print (hex(r), hex(s))
    boo = SM2_valid(SM2_sign_Curve, int2byte(0xf4a38489e32b45b6f876e3ac2168ca392362dc8f23459c1d1146fc3dbfb7bc9a), public_key, b'message digest', 0x40f1ec59f793d9f49e09dcef49130d4194f79fb1eed2caa55bacdb49c4e755d1, 0x6fc6dac32c5d5cf10c77dfb20f7c2eb667a457872fb09ec56327a67ec7deebe7)
    print (boo)

if __name__ == '__main__':
    main()
