from .galois import GF2
from copy import deepcopy
import random

_aes_s_box = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]
_aes_s_box_inverse = [
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
]

def __convert_to_array(plain_int):
    plain_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4)[::-1]:
        for j in range(4)[::-1]:
            plain_array[j][i] = plain_int & 0xff
            plain_int >>= 8
    return plain_array

def __get_num_from_sbox(index):
    row = (index & 0xf0) >> 4
    col = index & 0xf
    return _aes_s_box[row][col]

def __get_num_from_sbox_inverse(index):
    row = (index & 0xf0) >> 4
    col = index & 0xf
    return _aes_s_box_inverse[row][col]

def __sub_bytes(input_array):
    for i in range(4):
        for j in range(4):
            input_array[i][j] = __get_num_from_sbox(input_array[i][j])

def __sub_bytes_inverse(input_array):
    for i in range(4):
        for j in range(4):
            input_array[i][j] = __get_num_from_sbox_inverse(input_array[i][j])

def __shift_rows(input_array):
    input_array[1] = input_array[1][1:] + [input_array[1][0]]
    input_array[2] = input_array[2][2:] + input_array[2][:2]
    input_array[3] = [input_array[3][3]]  + input_array[3][:3]

def __shift_rows_inverse(input_array):
    input_array[3] =   input_array[3][1:] + [ input_array[3][0] ]
    input_array[2] =   input_array[2][2:]   + input_array[2][:2]
    input_array[1] = [ input_array[1][3] ]  + input_array[1][:3]

columns_matrix = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
]

def __mix_columns(input_array):
    res_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            res = GF2(0)
            for k in range(4):
                res += GF2(columns_matrix[i][k]) * GF2(input_array[k][j])
            res %= GF2(0b100011011)
            res_array[i][j] = res.data
    return res_array

columns_matrix_inverse = [
    [0xe, 0xb, 0xd, 0x9],
    [0x9, 0xe, 0xb, 0xd],
    [0xd, 0x9, 0xe, 0xb],
    [0xb, 0xd, 0x9, 0xe]
]

def __mix_columns_inverse(input_array):
    res_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        for j in range(4):
            res = GF2(0)
            for k in range(4):
                res += GF2(columns_matrix_inverse[i][k]) * GF2(input_array[k][j])
            res %= GF2(0b100011011)
            res_array[i][j] = res.data
    return res_array

def __add_round_key(input_array, key_array):
    for i in range(4):
        for j in range(4):
            input_array[i][j] ^= key_array[i][j]

def __key_schedule(pre_key, round):
    next_key = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    # print (pre_key)
    for i in range(4):
        next_key[i][0] = pre_key[i - 3][3]
    __sub_bytes(next_key)
    for i in range(4):
        next_key[i][0] ^= pre_key[i][0]
    next_key[0][0] ^= (GF2(pow(2, round)) % GF2(0x11b)).data
    for i in range(1, 4):
        for j in range(4):
            next_key[j][i] = next_key[j][i - 1] ^ pre_key[j][i]
    return next_key

def __key_schedule_inverse(next_key, round):
    pre_key = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(3, 0, -1):
        for j in range(4):
            pre_key[j][i] = next_key[j][i - 1] ^ next_key[j][i]
    pre_key[0][0] = (GF2(pow(2, round)) % GF2(0x11b)).data
    for i in range(4):
        pre_key[i][0] ^= next_key[i][0]
        pre_key[i][0] ^= __get_num_from_sbox(pre_key[i - 3][3])
    return pre_key

def __aes_key_gen(key):
    key = __convert_to_array(key)
    round_key = [key]
    for i in range(10):
        round_key.append(__key_schedule(round_key[i], i))
    return round_key

def __convert_to_int(input_array):
    output_int = 0
    for i in range(4):
        for j in range(4):
            output_int <<= 8
            output_int |= input_array[j][i]
    return output_int

def aes_encrypt(plain_text, key):
    plain_text ^= key
    round_key = __aes_key_gen(key)
    # print_array(round_key[9])
    # print_array(round_key[10])
    plain_array = __convert_to_array(plain_text)
    for i in range(1, 10):
        __sub_bytes(plain_array)
        __shift_rows(plain_array)
        # if i == 9:
            # print_array(plain_array)
        plain_array = __mix_columns(plain_array)
        __add_round_key(plain_array, round_key[i])
    __sub_bytes(plain_array)
    __shift_rows(plain_array)
    __add_round_key(plain_array, round_key[10])
    # print_array(plain_array)
    return __convert_to_int(plain_array)

def aes_decrypt(cipher_text, key):
    round_key = __aes_key_gen(key)[::-1]
    cipher_array = __convert_to_array(cipher_text)
    __add_round_key(cipher_array, round_key[0])
    for i in range(1, 10):
        __shift_rows_inverse(cipher_array)
        __sub_bytes_inverse(cipher_array)
        __add_round_key(cipher_array, round_key[i])
        cipher_array = __mix_columns_inverse(cipher_array)
    __shift_rows_inverse(cipher_array)
    __sub_bytes_inverse(cipher_array)
    __add_round_key(cipher_array, round_key[10])
    return __convert_to_int(cipher_array)

# for debug
def print_array(array):
    print ()
    for i in array:
        print ('[', end=' ')
        for j in i:
            print (f'0x%2x' % j, end= ' ')
        print (']')


# attack
# input: a list of epsilon (len: 4)
# output: all posible key (only 4 bytes), 4 sets in a list
def fault_analysis(epsilon, true_res, col):
    c = [2, 1, 1, 3]
    # print (epsilon, true_res, col, c)
    S = [ [e, cur_c, set()] for e, cur_c in zip(epsilon, c) ]
    for s in S:
        for e in range(2 ** 8):
            for x in range(2 ** 8):
                if __get_num_from_sbox(x ^ (GF2(s[1]) * GF2(e) % GF2(0x11b)).data) == __get_num_from_sbox(x) ^ s[0]:
                    s[2].add(e)
                    break
    s = S[0][2]
    for k in S:
        s &= k[2]
    X = [ set() for i in range(4) ]
    for e in s:
        for x in range(2 ** 8):
            for i in range(4):
                if __get_num_from_sbox(x ^ (GF2(c[i]) * GF2(e) % GF2(0x11b)).data) == __get_num_from_sbox(x) ^ epsilon[i]:
                    X[i].add(x)
    K = [ set() for i in range(4) ]
    for i in range(4):
        for lam in X[i]:
            K[i].add(__get_num_from_sbox(lam) ^ true_res[i])
    return K

def __sim_last_round(input_array, key_9, key_10):
    input_array = __mix_columns(input_array)
    __add_round_key(input_array, key_9)
    __sub_bytes(input_array)
    __shift_rows(input_array)
    __add_round_key(input_array, key_10)
    return input_array


# input: an cipher in round 9 waiting to be injected, two keys only used to pass to the crypt matchine
# output: key in round 10
def error_injection(array_to_inject, key_9, key_10):
    correct = __sim_last_round(deepcopy(array_to_inject), key_9, key_10) # 首先计算正确结果
    key = [ set(j for j in range(2 ** 8)) for i in range(16) ]
    impact = [[0, 13, 10, 7], [4, 1, 14, 11], [8, 5, 2, 15], [12, 9, 6, 3]]
    for i in range(4):
        # 若对应四个位置的密钥空间完全确定，再确定下四个位置的密钥
        while len(key[impact[i][0]]) > 1 or len(key[impact[i][1]]) > 1 or len(key[impact[i][2]]) > 1 or len(key[impact[i][3]]) > 1:
            injected_array = deepcopy(array_to_inject)
            fault = random.randint(1, 0xff)
            injected_array[0][i] ^= fault
            error = __sim_last_round(deepcopy(injected_array), key_9, key_10) # 注入错误
            true_res = []
            epsilon = []
            for j in range(4):
                row = impact[i][j] & 3
                col = impact[i][j] >> 2
                true_res.append(correct[row][col])
                epsilon.append(error[row][col] ^ true_res[-1])
            # 以上代码目的在于将错误注入到特定位置，并计算出错误密文的与正确密文的偏差
            # 实际的错误分析中，仅需要调用 fault_analysis 函数，并以此来缩小密钥空间即可
            ans_res = fault_analysis(epsilon, true_res, i)
            # print (fault, epsilon, true_res)
            for j in range(4):
                key[impact[i][j]] &= ans_res[j]
    last_key = [ [0] * 4 for i in range(4) ]
    for i in range(4):
        for j in range(4):
            last_key[j][i] = list(key[(i << 2) + j])[0]
    # 用最终计算出的Key[10]反向推算出Key[0]
    for i in range(9, -1, -1):
        last_key = __key_schedule_inverse(last_key, i)
    return __convert_to_int(last_key)



