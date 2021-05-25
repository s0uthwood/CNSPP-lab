from utils import *
import random

class ECC_Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __str__(self):
        return f'({self.x}, {self.y}), curve: {self.curve}'

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

SM2_Curve = Curve(
    0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC, # a 
    0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93, # b
    0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF, # p
    0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123, # n
    0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, # G_x
    0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0  # G_y
)

'''
def ECC_add(a, b, p, G, Q):
    # y**2 = x**3 + a*x + b
    # G = (x1, y1)
    # Q = (x2, y2)
    if G == (0, 0):
    	return Q
    if Q == (0, 0):
    	return G
    x1, y1 = G
    x2, y2 = Q
    if x1 == x2:
        if y1 == y2 and y1 != 0:
            t = (3 * x1 * x1 + a) * inverse(2 * y1, p) % p
        else:
            return (0, 0)
    else:
        t = (y2 - y1) * inverse(x2 - x1, p) % p
    x3 = (t * t - x1 - x2) % p
    y3 = (t * (x1 - x3) - y1) % p
    return (x3, y3)

def ECC_sub(a, b, p, G, Q):
    if Q == None:
        return G
    x2, y2 = Q
    return ECC_add(a, b, p, G, (x2, -y2))

def ECC_mul(a, b, p, k, G):
	x3, y3 = 0, 0
	tmp = G
	times = k
	while times > 0:
		if times & 1 == 1:
			x3, y3 = ECC_add(a, b, p, (x3, y3), tmp)
		tmp = ECC_add(a, b, p, tmp, tmp)
		times >>= 1
	return (x3, y3)
'''
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


def ECC_keygen(curve: Curve):
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    sk = random.randint(1, curve.n - 1)
    pk = sk * G
    return sk, G


def ECC_encrypt_point(curve: Curve, M: ECC_Point, pk: ECC_Point):
    G = ECC_Point(curve.G_x, curve.G_y, curve)
    k = random.randint(1, curve.n)
    k = 41
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
    curve_en = Curve(0, -4, 257, 257, 2, 2)
    na = 101
    C1, C2 = ECC_encrypt_point(curve_en, ECC_Point(112, 26, curve_en), na * ECC_Point(2, 2, curve_en))
    print (C1)
    print (C2)
    print (ECC_decrypt_point(curve_en, na, C1, C2))

if __name__ == '__main__':
    main()