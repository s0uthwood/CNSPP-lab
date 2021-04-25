SBOX = [
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48
]

fk = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]
ck = [
    0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
    0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
    0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
    0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
    0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
    0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
    0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
    0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279,
]

def shift(pre, x):
    aft = ((pre % (1 << (32 - x))) << x) + (pre >> (32 - x))
    return aft

def sbox(pre):
    if(pre < (1 << 8)):
        aft = SBOX[pre]
    return aft

def sm4_round(rk, x):
    x_3 = x % (1 << 32)
    x_2 = (x >> 32) % (1 << 32)
    x_1 = (x >> 64) % (1 << 32)
    x_0 = (x >> 96) % (1 << 32)
    pre_sbox = x_1 ^ x_2 ^ x_3 ^ rk
    aft_sbox = 0
    for i in range(4):
        aft_sbox += sbox((pre_sbox >> (i * 8)) % (1 << 8)) << i * 8
    x_4 = x_0 ^ aft_sbox ^ shift(aft_sbox, 2) ^ shift(aft_sbox, 10) ^ shift(aft_sbox, 18) ^ shift(aft_sbox, 24)
    return x_4

def key_round(k, ck):
    k_3 = k % (1 << 32)
    k_2 = (k >> 32) % (1 << 32)
    k_1 = (k >> 64) % (1 << 32)
    k_0 = (k >> 96) % (1 << 32)
    pre_sbox = k_1 ^ k_2 ^ k_3 ^ ck
    aft_sbox = 0
    for i in range(4):
        aft_sbox += sbox((pre_sbox >> (i * 8)) % (1 << 8)) << i * 8
    k_4 = k_0 ^ aft_sbox ^ shift(aft_sbox, 13) ^ shift(aft_sbox, 23)
    return k_4

def convert_to_list(int_in):
    list_out = []
    for i in range(4):
        list_out = [int_in & 0xffffffff] + list_out
        int_in >>= 32
    return list_out

def padding_pkcs7(int_in, length_in, block_length):
    target_length = block_length - (length_in % block_length)
    for i in range(target_length):
        int_in <<= 8
        int_in += target_length
    return int_in

def key_expension(mk):
    mk = convert_to_list(mk)
    rk = [0, 0, 0, 0]
    for i in range(4):
        rk[i] = mk[i] ^ fk[i]
    for i in range(32):
        res = key_round((rk[i] << 96) + (rk[i + 1] << 64) + (rk[i + 2] << 32) + rk[i + 3], ck[i])
        rk.append(res)
    return rk

def sm4_encrypt(x, mk):
    x = convert_to_list(x)
    rk = key_expension(mk)
        # print hex(rk[-1])[2:-1]
    for i in range(32):
        x.append(sm4_round(rk[i + 4], (x[i] << 96) + (x[i + 1] << 64) + (x[i + 2] << 32) + x[i + 3]))
        # print hex(x[-1])[2:-1]
    res = b''
    for i in range(4):
        # res += ('%x' % x[35 - i]).zfill(8)
        res += x[35 - i].to_bytes(4, byteorder = 'big')
    return res

def sm4_decrypt(x, mk):
    x = convert_to_list(x)
    rk = key_expension(mk)
    rk = rk[::-1]
    for i in range(32):
        x.append(sm4_round(rk[i], (x[i] << 96) + (x[i + 1] << 64) + (x[i + 2] << 32) + x[i + 3]))
        # print hex(x[-1])[2:-1]
    res = b''
    for i in range(4):
        # res += ('%x' % x[35 - i]).zfill(8)
        res += x[35 - i].to_bytes(4, byteorder = 'big')
    return res

def sm4_encrypt_rk(x, rk):
    x = convert_to_list(x)
    for i in range(32):
        x.append(sm4_round(rk[i + 4], (x[i] << 96) + (x[i + 1] << 64) + (x[i + 2] << 32) + x[i + 3]))
    res = b''
    for i in range(4):
        # res += ('%x' % x[35 - i]).zfill(8)
        res += x[35 - i].to_bytes(4, byteorder = 'big')
    return res

def sm4_decrypt_rk(x, rk):
    rk = rk[::-1]
    x = convert_to_list(x)
    for i in range(32):
        x.append(sm4_round(rk[i], (x[i] << 96) + (x[i + 1] << 64) + (x[i + 2] << 32) + x[i + 3]))
    res = b''
    for i in range(4):
        # res += ('%x' % x[35 - i]).zfill(8)
        res += x[35 - i].to_bytes(4, byteorder = 'big')
    return res

def sm4_encrypt_ecb(xs, mk):
    plain_length = len(xs)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    xs = padding_pkcs7(xs, plain_length, 16)
    # xs = convert_to_list(xs)
    # list_length = len(xs)
    cipher = b''
    # for i in range(0, xs, 4):
    rk = key_expension(mk)
    while xs > 0:
        cipher = sm4_encrypt_rk(xs & 0xffffffffffffffffffffffffffffffff, rk) + cipher
        xs >>= 128
    return cipher

def sm4_decrypt_ecb(xs, mk):
    cipher_length = len(xs)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    plain = b''
    rk = key_expension(mk)
    while xs > 0:
        plain = sm4_decrypt_rk(xs & 0xffffffffffffffffffffffffffffffff, rk) + plain
        xs >>= 128
    padding_length = plain[-1]
    return plain[:-padding_length * 2]

def sm4_encrypt_cbc(xs, mk, iv):
    plain_length = len(xs)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    xs = padding_pkcs7(xs, plain_length, 16)
    cipher = b''
    rk = key_expension(mk)
    plain = []
    while xs > 0:
        plain.append(xs & ((1 << 128) - 1))
        xs >>= 128
    for p in plain[::-1]:
        c = sm4_encrypt_rk((p & 0xffffffffffffffffffffffffffffffff) ^ iv, rk)
        cipher += c
        iv = int.from_bytes(c, byteorder='big', signed=False)
    return cipher

def sm4_decrypt_cbc(xs, mk, iv):
    cipher_length = len(xs)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    plain = b''
    rk = key_expension(mk)
    cipher = []
    while xs > 0:
        cipher.append(xs & ((1 << 128) - 1))
        xs >>= 128
    for c in cipher[::-1]:
        res = sm4_decrypt_rk(c & 0xffffffffffffffffffffffffffffffff, rk)
        res = int.from_bytes(res, byteorder = 'big', signed = False)
        plain += (res ^ iv).to_bytes(16, byteorder = 'big')
        iv = c
    padding_length = plain[-1]
    return plain[:-padding_length * 2]

def sm4_encrypt_ctr(xs, mk, ctr):
    plain_length = len(xs)
    padding_length = 16 - (plain_length % 16)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    key = 0
    rk = key_expension(mk)
    for i in range(plain_length // 16 + 1):
        res = sm4_encrypt_rk(ctr, rk)
        key <<= 128
        key += int.from_bytes(res, byteorder = 'big', signed = False)
        ctr += 1
    cipher = (key >> (padding_length * 8)) ^ xs
    return cipher.to_bytes(plain_length, byteorder = 'big')

def sm4_decrypt_ctr(xs, mk, ctr):
    cipher_length = len(xs)
    padding_length = 16 - (cipher_length % 16)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    rk = key_expension(mk)
    key = 0
    for c in range(cipher_length // 16 + 1):
        res = sm4_encrypt_rk(ctr, rk)
        key <<= 128
        key += int.from_bytes(res, byteorder = 'big', signed = False)
        ctr += 1
    plain = (key >> (padding_length * 8)) ^ xs
    return plain.to_bytes(cipher_length, byteorder = 'big')


# input: 32 bytes of cipher (first 16 is iv)
# input for decrypt server: key
# output: 16 bytes of plain
def padding_attack(cipher, key):
    if len(cipher) != 32:
        return False
    origin_iv = int.from_bytes(cipher[:16], byteorder = 'big', signed = False)
    hack_iv = origin_iv >> 8 << 8 # hack_iv & 0xff..ff00
    last_padding = []
    for j in range(0x100):
        # print (last_plain)
        if sm4_decrypt_cbc_in_server(cipher[-16:], key, hack_iv) == True:
            last_padding.append(j)
        hack_iv += 1
    hack_iv = (origin_iv >> 8 << 8) | (last_padding[0] ^ 1 ^ 2)
    start = 2
    if len(last_padding) > 1:
        start = last_padding[0] ^ last_padding[1] ^ 1
        tmp_hack_iv = (hack_iv >> 16 << 16) ^ (hack_iv & 0xff)
        hack_iv = (hack_iv >> 8 << 8) | last_padding[0]
        FLAG = True
        if start == 2:
            FLAG = False # 如果填充为0202的话，异或后结尾为01，一定成功，此时遇到False才需要更换
        for j in range(0x100):
            # print (hex(tmp_hack_iv))
            if sm4_decrypt_cbc_in_server(cipher[-16:], key, tmp_hack_iv) == FLAG:
                hack_iv = (hack_iv >> 8 << 8) | (last_padding[1])
                break
            tmp_hack_iv += 0x100
        # print (hex(last_padding[0]), hex(last_padding[1]))
        # print (hack_iv.to_bytes(16, 'big'))
        # print (origin_iv.to_bytes(16, 'big'))
        hack_iv = hack_iv ^ int(("%x" % (start ^ (start + 1))).rjust(2, '0') * start, 16)
        start += 1
    for i in range(start, 17):
        hack_iv = (hack_iv >> (8 * i) << (8 * i)) ^ (hack_iv & ((1 << 8 * (i - 1)) - 1)) # hack_iv & 0xff..f00f..ff
        for j in range(0xff):
            if sm4_decrypt_cbc_in_server(cipher[-16:], key, hack_iv) == True:
                break
            hack_iv += 1 << (8 * (i - 1))
        if i < 16:
            hack_iv ^= int(("%x" % (i ^ (i + 1))).rjust(2, '0') * i, 16)
        # hack_iv ^= int(("%x" % (i + 1)).rjust(2, '0') * i, 16)
    return (hack_iv ^ 0x10101010101010101010101010101010 ^ origin_iv).to_bytes(16, byteorder='big')

def sm4_decrypt_cbc_in_server(xs, mk, iv):
    cipher_length = len(xs)
    xs = int.from_bytes(xs, byteorder='big', signed=False)
    plain = b''
    rk = key_expension(mk)
    cipher = []
    while xs > 0:
        cipher.append(xs & ((1 << 128) - 1))
        xs >>= 128
    for c in cipher[::-1]:
        res = sm4_decrypt_rk(c & 0xffffffffffffffffffffffffffffffff, rk)
        res = int.from_bytes(res, byteorder = 'big', signed = False)
        plain += (res ^ iv).to_bytes(16, byteorder = 'big')
        iv = c
    # print (plain)
    return server_judge(plain)

def server_judge(decrypted_value):
    padding = decrypted_value[-1]
    if padding > 16 or padding == 0:
        return False
    for i in range(1, padding + 1):
        if decrypted_value[-i] != padding:
            return False
    return True
