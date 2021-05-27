from utils import gcd, ex_gcd, inverse, all_prime, my_pow, is_prime_miller, crt, ex_crt
import random

def lucas(p, X, Y, k):
    delta = X * X - 4 * Y
    U = 1
    V = X
    k_bin = bin(k)[2:]
    k_binlen = len(k_bin)
    for i in range(1, k_binlen):
        U, V = U * V % p, ((V * V + delta * U * U) * (p + 1) // 2) % p # (p + 1) // 2 == inverse(2, p)
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
            t = (3 * self.x * self.x + self.curve.a) * inverse(2 * self.y, p) % p
        elif self.x == other.x and self.y != other.y:
            return ECC_Point(None, None, self.curve)
        else:
            t = (other.y - self.y) * inverse(other.x - self.x, p) % p
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
            y = my_pow(x, u, p)
            z = my_pow(y, 2, p)
            if z == x:
                return y
            return None
        elif p % 8 == 5:
            u = p // 8
            z = my_pow(x, 2 * u + 1, p)
            if z % p == 1:
                return my_pow(x, u + 1, p)
            elif z % p == -1:
                return (2 * x * my_pow(4 * x, u, p)) % p
            return None
        elif p % 8 == 1:
            u = p // 8
            while True:
                U, V = lucas(p, random.randint(1, p - 1), x, 4 * u + 1)
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

test_Curve = Curve(
    -3,
    2455155546008943817740293915197451784769108058161191238065,
    6277101735386680763835789423207666416083908700390324961279,
    6277101735386680763835789423207666416083908700390324961279,
    602046282375688656758213480587526111916698976636884684818,
    174050332293622031404857552280219410364023488927386650641
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
    n = 0
    for i in range(len(b)):
        n <<= 8
        n += b[i]
    return n

def int2byte(n):
    b = b''
    length = len(hex(n)) - 2
    length = length // 2 + (length & 1)
    return n.to_bytes(length, 'big')

def str2byte(s):
    return s.encode('utf-8')

def point2byte(P, p, mode):
    # p: field F_p
    # mode == 0: compression
    # mode == 1: uncompression
    # mode == 2: mix
    x, y = P
    if x == 0 and y == 0:
        print ("[error] in point2byte: wrong point!")
        return
    X = int2byte(x)
    if mode == 0:
        y_t = y & 1
        return (b'\x02' if y_t == 0 else b'\x03') + X
    Y = int2byte(y)
    if mode == 1:
        return b'\x04' + X + Y
    if mode == 2:
        y_t = y & 1
        return (b'\x06' if y_t == 0 else b'\x07') + X + Y
    print ("[error] in point2byte: mode should [ 0 | 1 | 2 ]")
    return 

def byte2point(b):
    PC = b[0]
    if PC == 2 or PC == 3:
        y_t = PC - 2
    elif PC == 4:
        return
    elif PC == 6 or PC == 7:
        return 

def msg2point(curve: Curve, m):
    m = len(m).to_bytes(1, 'big') + m
    while True:
        x = int.from_bytes(m, 'big')
        y = curve.calc_y(x)
        if y != None:
            return ECC_Point(x, y, curve)
        m += random.randint(1, 0xff).to_bytes(1, 'big')

def point2msg(curve: Curve, P):
    msg = int2byte(P.x)
    msg_len = msg[0]
    return msg[1 : msg_len + 1]

def ECC_keygen(curve: Curve):
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    sk = random.randint(1, curve.n - 1)
    pk = sk * G
    return sk, pk

def ECC_sharedkey(Q: ECC_Point, sk: int):
    return Q * sk

def ECC_encrypt_point(curve: Curve, M: ECC_Point, pk: ECC_Point):
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    k = random.randint(1, curve.n)
    # k = 41
    C1 = k * G
    C2 = M + k * pk
    return C1, C2

def ECC_decrypt_point(curve: Curve, na: int, C1: ECC_Point, C2: ECC_Point):
    M = C2 - na * C1
    return M

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
    M = ECC_Point(2594161300049362469169638638781986485403377947559889224556, -915731655498392811604767074090214190962897463083669095347, test_Curve)
    pk = ECC_Point(4535708181192800030922425040161683059768487875080759471914, -1061575060680846108649238340040410272066486614691829051119, test_Curve) * 273065013239976945911310331771
    # print (pk)
    C1, C2 = ECC_encrypt_point(test_Curve, M, pk)
    print (C1)
    print (C2)
    print (curve_en.calc_y(112)) # 26 or 231

if __name__ == '__main__':
    main()
