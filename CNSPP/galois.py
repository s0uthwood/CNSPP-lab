class GF2:
    def __init__(self, v):
        self.data = v
    def __str__(self):
        return hex(self.data)
    def __repr__(self):
        return "GF2(0x%x)" % self.data
    def __add__(self, other):
        return GF2(self.data ^ other.data)
    def __sub__(self, other):
        return GF2(self.data ^ other.data)
    def __lshift__(self, other):
        return GF2(self.data << other)
    def __eq__(self, other):
        if type(other) == type(1):
            if self.data == other:
                return True
            else: 
                return False
        if type(other) == type(self):
            if self.data == other.data:
                return True
            else: 
                return False
        return False
    def __mul__(self, other):
        ans = 0
        for i in range(len(bin(self.data)) - 2):
            if self.data & (1 << i):
                ans ^= other.data << i
        return GF2(ans)
    def __truediv__(self, other):
        a = self
        b = other
        if b.data == 1:
            return a
        lena = len(bin(a.data)) - 2
        lenb = len(bin(b.data)) - 2
        ans = 0
        while lena >= lenb:
            a = a + (b << lena - lenb)
            ans += 1 << (lena - lenb)
            lena = len(bin(a.data)) - 2
        return GF2(ans)
    def __floordiv__(self, other):
        return self / other
    def __isub__(self, other):
        return self - other
    def __mod__(self, other):
        a = self.data
        b = other.data
        lena = len(bin(a)) - 2
        lenb = len(bin(b)) - 2
        for i in range(lena, lenb - 1, -1):
            if a & (1 << i - 1) != 0:
                a ^= (b << i - lenb)
        return GF2(a)
    def __pow__(self, other, modulo = None):
        d = GF2(1)
        while other > 0:
            if other & 1:
                d = d * self
                if modulo != None:
                    d %= modulo
            other >>= 1
            self *= self
            if modulo != None:
                self %= modulo
        return d
    def euclid(self, other):
        if other == 0:
            return self
        return GF2.euclid(other, self % other)
    def ex_euclid(self, other):
        if other.data == 0:
            return self, GF2(1), GF2(0)
        GCD, xtmp, ytmp = GF2.ex_euclid(other, self % other)
        x = ytmp
        y = xtmp + ytmp * (self / other)
        return GCD, x, y
    def inverse(self, other):
        GCD, x, y = GF2.ex_euclid(self, other)
        return x
    def isPrimitive(self):
        for i in range(2, self.data):
            if (self % GF2(i)).data == 0:
                return False
        length = len(bin(self.data)) - 3
        m = (1 << length) - 1
        if GF2((1 << m) + 1) % self != 0:
            return False
        for i in range(length, (1 << length) - 1):
            if GF2((1 << i) + 1) % self == 0:
                return False
        return True


def fast_inverse_init(a, b):
    inverse_pow_list = []
    inverse_pow_list.append(1)
    for i in range(1, 256):
        inverse_pow_list.append(pow(a, i, b))
    return inverse_pow_list


def fast_inverse(a, b):
    is_init = True
    inverse_pow_list = fast_inverse_init(GF2(3), b)
    pos = inverse_pow_list.index(a)
    return inverse_pow_list[255 - pos]


def allPrimitive(k):
    list_prime = []
    for i in range(2 ** (k - 1), 2 ** k):
        if GF2(i).isPrimitive():
            list_prime.append(GF2(i))
    return list_prime
