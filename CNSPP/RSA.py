from utils import gcd, ex_gcd, inverse, all_prime, my_pow, is_prime_miller, crt, ex_crt
from random import randint
import math

def get_prime(bit_length):
	while True:
		x = randint((1 << (bit_length - 1)), (1 << bit_length) - 1)
		x += 1 - (x & 1)
		if is_prime_miller(x):
			if is_prime_miller((x - 1) // 2):
				break
	return x

def RSA_keygen(bit_length, e):
	p_length = bit_length // 2
	q_length = bit_length - p_length
	while True:
		p = get_prime(p_length)
		while gcd(p - 1, e) != 1:
			p = get_prime(p_length)
		q = get_prime(q_length)
		while gcd(q - 1, e) != 1:
			q = get_prime(q_length)
		phi = (p - 1) * (q - 1)
		if gcd(phi, e) == 1:
			return p, q

def RSA_encrypt(m, p, q, e):
	if not is_prime_miller(p) and not is_prime_miller(q):
		print ("wrong p q!")
		return
	N = p * q
	return my_pow(m, e, N)

def RSA_decrypt_CRT(c, p, q, e):
	if not is_prime_miller(p) and not is_prime_miller(q):
		print ("wrong p q!")
		return 
	N = p * q
	phi_N = (p - 1) * (q - 1)
	d = inverse(e, phi_N)
	d1 = d % (p - 1)
	d2 = d % (q - 1)
	c1 = c % p
	c2 = c % q
	m1 = my_pow(c1, d1, p)
	m2 = my_pow(c2, d2, q)
	M = ex_crt([m1, m2], [p, q], 2)
	return M

def is_perfect_square(x):
	left = 0
	right = x
	while left <= right:
		mid = (left + right) // 2
		test = mid * mid
		if test == x:
			return mid
		elif test < x:
			left = mid + 1
		else:
			right = mid - 1
	return -1

def wiener_attack(e, N):
	# find the continued fraction expansion of e/N
	x = []
	a, b = e, N
	while (b != 0):
		x.append(a // b)
		a, b = b, a % b
	# an example: x = [3, 7, 15, 1, 292, 1, 1, 1, 2]
	nominators = [x[0]]
	denominators = [1]
	for i in range(1, len(x)):
		if i == 1:
			nominators.append(x[i] * x[i - 1] + 1)
			denominators.append(x[i])
		else:
			nominators.append(x[i] * nominators[-1] + nominators[-2])
			denominators.append(x[i] * denominators[-1] + denominators[-2])
	# search all posible k & d
	for k, d in zip(nominators, denominators):
		if k == 0:
			continue
		cur_phi = (e * d - 1) // k
		b = N + 1 - cur_phi            # we have p^2 - b * p + n = 0
		attack_res = is_perfect_square(b * b - 4 * N)   # sqrt(b^2 - 4ac)
		# print (attack_res)
		if attack_res >= 0:
			p1 = (b + attack_res) // 2
			p2 = (b - attack_res) // 2
			return (p1, p2, d)


if __name__ == "__main__":
	from libnum import n2s
	print (RSA_keygen(512, 65537))
	p = 780862373351
	q = 2694390009002158502159675471958109058427811853007950153726807530201964991300337771811472999684268349834479470830859598452183054815548222837274388694871
	c = 1557822317635545996723033767564307143735601984422708057233119748579354270160257344153164937880352525867134608292240275238324090074000491936146989591988221080515113
	print (n2s(RSA_decrypt_CRT(c, p, q, 3)))
	# print (wiener_attack(73, 95))
	e = 284100478693161642327695712452505468891794410301906465434604643365855064101922252698327584524956955373553355814138784402605517536436009073372339264422522610010012877243630454889127160056358637599704871937659443985644871453345576728414422489075791739731547285138648307770775155312545928721094602949588237119345
	n = 468459887279781789188886188573017406548524570309663876064881031936564733341508945283407498306248145591559137207097347130203582813352382018491852922849186827279111555223982032271701972642438224730082216672110316142528108239708171781850491578433309964093293907697072741538649347894863899103340030347858867705231
	c = 225959163039382792063969156595642930940854956840991461420767658113591137387768433807406322866630268475859008972090971902714782079518283320987088621381668841235751177056166331645627735330598686808613971994535149999753995364795142186948367218065301138932337812401877312020570951171717817363438636481898904201215
	p, q, d = wiener_attack(e, n)
	print (n2s(RSA_decrypt_CRT(c, p, q, e)))
	