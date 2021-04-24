from random import randint

def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return abs(x)

def ex_gcd(x, y):
    list_x = [x, 1, 0]
    list_y = [y, 0, 1]
    while list_y[0] != 0:
        r = list_x[0] // list_y[0]
        for i in range(3):
            list_x[i] -= r * list_y[i]
        list_x, list_y = list_y, list_x
    if list_x[0] < 0:
        list_x[0], list_x[1], list_x[2] = -list_x[0], -list_x[1], -list_x[2]
    return list_x

def inverse(a, n):
    if n < 2:
        raise ValueError("n < 2, error")
    g, x, y = ex_gcd(a, n)
    if g != 1:
        print ("gcd(a, n) != 1, no inverse modular")
    return x % n

def all_prime(n):
    if n < 2:
        raise ValueError("n < 2, range(2, n) error")
    prime = [ False ] * (n // 2)
    ans = [2]
    i = 0
    num = i * 2 + 3
    while num <= n:
        if prime[i] == False:
            ans.append(num)
            j = num
            while j * num <= n:
                prime[(j * num - 3) // 2] = True
                j += 2
        i += 1
        num = i * 2 + 3
    return ans

def my_pow(a, b, m):
    d = 1
    while b > 0:
        if b & 1:
            d = (d * a) % m
        b >>= 1
        a = (a * a) % m
    return d

def is_prime_miller(n):
    primelist = all_prime(1000)
    if n < 2:
        return False
    for i in primelist:
        if n == i:
            return True
        if n % i == 0:
            return False
    k = 0
    q = n - 1
    while q % 2 == 0 and q > 0:
        q >>= 1
        k += 1
    T = 15
    while T:
        a = randint(3, n - 1)
        if gcd(a, n) > 1:
            return False
        a = my_pow(a, q, n)
        if a != 1:
            for i in range(k):
                if a == n - 1:
                    break
                if a == 1:
                    return False
                a = pow(a, 2, n)
        if a != 1 and a != n - 1:
            return False
        T -= 1
    return True

def crt(a, m, k):
    M = 1
    for i in m:
        M *= i
    e = [0]  * k
    for i in range(k):
        e[i] = inverse(M // m[i], m[i])
    sum = 0
    for i in range(k):
        sum += M // m[i] * e[i] * a[i]
        sum %= M
    return sum

def ex_crt(a, m, k):
    for i in range(1, k):
        t = gcd(m[i], m[i - 1])
        if (a[i] - a[i - 1]) % t != 0:
            return -1
        a[i] = (inverse(m[i - 1] // t, m[i] // t) * (a[i] - a[i - 1]) // t) % (m[i] // t) * m[i - 1] + a[i - 1]
        m[i] = m[i] // t * m[i - 1]
        a[i] = (a[i] % m[i] + m[i]) % m[i]
    return a[-1]
