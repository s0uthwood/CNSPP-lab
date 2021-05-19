from utils import *

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


def main():
    print (ECC_add(2, 3, 17, (2, 7), (11, 8)))
    for i in range(6):
    	print (ECC_mul(2, 3, 97, i, (3, 6)))

if __name__ == '__main__':
    main()