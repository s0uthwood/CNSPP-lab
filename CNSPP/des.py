def print_hex_as_len(output_num, length):
    output_str = '0x' + ('%x' % output_num).zfill(length)
    print (output_str)
    return output_str

def __transform(input, len_input, table, len_table):
    output = 0
    for i in range(len_table):
        output <<= 1
        output |= (input >> (len_input - table[i])) & 1
    return output

def __left_rot(input, len_input, round):
    input = input << round
    output = input | (input >> (len_input))
    output %= 1 << len_input
    return output

des_key_init_transform_table = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
]

def __des_key_init_transform(input):
    abandon_table = [8, 16, 24, 32, 40, 48, 56, 64][::-1]
    abandon_key = 0
    for i in range(8):
        abandon_key ^= (input >> (64 - abandon_table[i] - i)) & (1 << i)
    return __transform(input, 64, des_key_init_transform_table, 56), abandon_key

def __half_split(input, len_input):
    pos = len_input // 2
    return [input >> pos, input % (1 << pos)]

def __re_merge(input, len_input):
    return (input[0] << len_input) + input[1]

des_sepermuted_table = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

def __des_sepermuted(input):
    abandon_table = [9, 18, 22, 25, 35, 38, 43, 54][::-1]
    abandon_key = 0
    for i in range(8):
        abandon_key ^= (input >> (56 - abandon_table[i] - i)) & (1 << i)
    return __transform(input, 56, des_sepermuted_table, len(des_sepermuted_table)), abandon_key

des_initial_table = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

def __des_initial(input):
    return __transform(input, 64, des_initial_table, len(des_initial_table))

des_expansion_table = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
]

def des_expansion(input):
    return __transform(input, 32, des_expansion_table, len(des_expansion_table))

def des_fast_expansion(input):
    out = input & 1
    out = (out << 5) | ((input >> 27) & 0x1f)
    out = (out << 6) | ((input >> 23) & 0x3f)
    out = (out << 6) | ((input >> 19) & 0x3f)
    out = (out << 6) | ((input >> 15) & 0x3f)
    out = (out << 6) | ((input >> 11) & 0x3f)
    out = (out << 6) | ((input >>  7) & 0x3f)
    out = (out << 6) | ((input >>  3) & 0x3f)
    out = (out << 5) | (input & 0x1f)
    out = (out << 1) | ((input >> 31) & 1)
    return out

des_sbox_table = [
    [
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9, 0,  7,
        0 , 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5, 3,  8,
        4 ,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10, 5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0, 6, 13
    ],
    [
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
         3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
         0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9,
    ],
    [
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
         1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12,
    ],
    [
         7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
         3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14,
    ],
    [
         2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
         4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3,
    ],
    [
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
         9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
         4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13,
    ],
    [
         4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
         1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
         6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12,
    ],
    [
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
         1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
         7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
         2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11,
    ]
]

def __des_sbox(input):
    output = 0
    for i in range(8):
        output <<= 4
        tmp = (input >> (48 - 6 * (i + 1))) & 0x3f
        tmp = (tmp & 0x20) + ((tmp & 1) << 4) + ((tmp & 0x1e) >> 1)
        output += des_sbox_table[i][tmp]
    return output

des_pbox_table = [
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
]

def __des_pbox(input):
    return __transform(input, 32, des_pbox_table, len(des_pbox_table))

des_final_transform_table = [
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25,
]

def __des_final_transform(input):
    return __transform(input, 64, des_final_transform_table, 64)

def __des_text_std_calc(L, R, key):
    next_L = R
    R = des_expansion(R)
    R ^= key
    R = __des_sbox(R)
    R = __des_pbox(R)
    # R = __des_psbox(R)
    R ^= L
    return [next_L, R]

def __des_text_fast_calc(L, R, key):
    next_L = R
    R = des_fast_expansion(R)
    R ^= key
    # R = __des_psbox(R)
    R = __des_fast_psbox(R)
    R ^= L
    return [next_L, R]

def __des_text_safety_calc(L, R, key, ab_key):
    next_L = R
    R = des_fast_expansion(R)
    R ^= key
    R = __des_fast_safety_psbox(R, ab_key)
    R ^= L
    return [next_L, R]

def des_std_encrypt(plain, key):
    key, _ = des_key_create(key)
    plain = __des_initial(plain)
    plain = __half_split(plain, 64)
    for round in range(16):
        plain = __des_text_std_calc(plain[0], plain[1], key[round])
    plain[0], plain[1] = plain[1], plain[0]
    cipher = __re_merge(plain, 32)
    return __des_final_transform(cipher)

def des_std_decrypt(plain, key):
    key, _ = des_key_create(key)
    plain = __des_initial(plain)
    plain = __half_split(plain, 64)
    for round in range(16):
        plain = __des_text_std_calc(plain[0], plain[1], key[16 - round])
    plain[0], plain[1] = plain[1], plain[0]
    cipher = __re_merge(plain, 32)
    return __des_final_transform(cipher)

def des_encrypt(plain, key):
    key, _ = des_key_create(key)
    plain = __des_initial(plain)
    plain = __half_split(plain, 64)
    for round in range(16):
        plain = __des_text_fast_calc(plain[0], plain[1], key[round])
    plain[0], plain[1] = plain[1], plain[0]
    cipher = __re_merge(plain, 32)
    return __des_final_transform(cipher)

def des_safety_encrypt(plain, key):
    key, ab_key = des_key_create(key)
    plain = __des_initial(plain)
    plain = __half_split(plain, 64)
    for round in range(16):
        plain = __des_text_safety_calc(plain[0], plain[1], key[round], ab_key[round])
    plain[0], plain[1] = plain[1], plain[0]
    cipher = __re_merge(plain, 32)
    return __des_final_transform(cipher)

def des_key_create(raw_key):
    raw_key, init_abandon = __des_key_init_transform(raw_key)
    raw_key = __half_split(raw_key, 56)
    key_left_rot_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    key = []
    ab_key = []
    for round in range(16):
        raw_key[0] = __left_rot(raw_key[0], 28, key_left_rot_table[round])
        raw_key[1] = __left_rot(raw_key[1], 28, key_left_rot_table[round])
        new_key, abandon_key = __des_sepermuted(__re_merge(raw_key, 28))
        key.append(new_key)
        ab_key.append(abandon_key << 8 | init_abandon)
    return key, ab_key

def des_decrypt(cipher, key):
    key, _ = des_key_create(key)
    cipher = __des_initial(cipher)
    cipher = __half_split(cipher, 64)
    for round in range(16):
        cipher = __des_text_fast_calc(cipher[0], cipher[1], key[15 - round])
    cipher[0], cipher[1] = cipher[1], cipher[0]
    plain = __re_merge(cipher, 32)
    return __des_final_transform(plain)

def des_safety_decrypt(cipher, key):
    key, ab_key = des_key_create(key)
    cipher = __des_initial(cipher)
    cipher = __half_split(cipher, 64)
    for round in range(16):
        cipher = __des_text_safety_calc(cipher[0], cipher[1], key[15 - round], ab_key[15 - round])
    cipher[0], cipher[1] = cipher[1], cipher[0]
    plain = __re_merge(cipher, 32)
    return __des_final_transform(plain)

des_psbox_table = [
    [8421888, 32768, 8421378, 2, 512, 8421890, 8389122, 8388608, 514, 8389120, 33280, 8421376, 32770, 8388610, 0, 33282, 0, 8421890, 33282, 32768, 8421888, 512, 8421378, 2, 8389120, 33280, 8421376, 8389122, 8388610, 32770, 514, 8388608, 32768, 2, 8421888, 8388608, 8421378, 33280, 512, 8389122, 8421890, 8421376, 8388610, 33282, 514, 8389120, 32770, 0, 8421890, 8421376, 8388608, 512, 32768, 8388610, 2, 33282, 32770, 8389122, 514, 8421888, 8389120, 0, 33280, 8421378],
    [1074282512, 16384, 524288, 1074266128, 1073741840, 1074282496, 1073758208, 16, 540672, 1073758224, 1073741824, 540688, 524304, 0, 16400, 1074266112, 1073758208, 540688, 16, 1073758224, 1074282512, 1073741824, 524288, 1074266128, 524304, 0, 16384, 1074266112, 1073741840, 540672, 1074282496, 16400, 0, 1074266128, 1073758224, 1074282496, 1074266112, 16, 540688, 16384, 16400, 524288, 524304, 1073741840, 540672, 1073758208, 1073741824, 1074282512, 540688, 524288, 1074266112, 16384, 1073758208, 1074282512, 16, 1073741824, 1074282496, 1073741840, 1073758224, 524304, 0, 16400, 1074266128, 540672],
    [260, 0, 67109120, 65796, 65540, 67108868, 67174660, 67174400, 67108864, 67174656, 65792, 67174404, 67109124, 65536, 4, 256, 67174656, 67174404, 0, 67109120, 67108868, 65536, 65540, 260, 4, 256, 67174400, 65796, 65792, 67109124, 67174660, 67108864, 67174656, 65540, 65536, 67109120, 256, 67174660, 67108868, 0, 67109124, 67108864, 4, 65792, 67174400, 260, 65796, 67174404, 67108864, 260, 67174656, 0, 65540, 67109120, 256, 67174404, 65536, 67174660, 65796, 67108868, 67109124, 67174400, 4, 65792],
    [2151682048, 2147487808, 4198464, 2151677952, 0, 4198400, 2147483712, 4194368, 2147483648, 4194304, 64, 2147487744, 2151678016, 4160, 4096, 2151682112, 2147487808, 64, 2151678016, 2147487744, 4198400, 2151682112, 0, 2151677952, 4096, 2151682048, 4194304, 4160, 2147483648, 4194368, 4198464, 2147483712, 4194368, 4198400, 2147483712, 0, 4160, 2151678016, 2151682048, 2147487808, 2151682112, 2147483648, 2151677952, 4198464, 2147487744, 4194304, 64, 4096, 2151677952, 2151682112, 0, 4198400, 4194368, 2147483648, 2147487808, 64, 2147483712, 4096, 2147487744, 2151678016, 4160, 2151682048, 4194304, 4198464],
    [128, 17039360, 262144, 536870912, 537133184, 16777344, 553648256, 262272, 16777216, 537133056, 536871040, 553910400, 553910272, 0, 17039488, 553648128, 17039488, 553648256, 128, 17039360, 262144, 537133184, 553910272, 536870912, 537133056, 0, 553910400, 16777344, 536871040, 553648128, 16777216, 262272, 262144, 128, 536870912, 553648256, 16777344, 553910272, 537133184, 16777216, 553910400, 553648128, 17039360, 537133056, 262272, 536871040, 0, 17039488, 553648256, 16777216, 17039360, 537133184, 536870912, 17039488, 128, 553910272, 262272, 553910400, 0, 553648128, 16777344, 262144, 537133056, 536871040],
    [268435464, 8192, 270532608, 270540808, 268443648, 2097152, 2097160, 268435456, 0, 268443656, 2105344, 8, 270532616, 2105352, 8200, 270540800, 270532608, 270540808, 8, 2097152, 2105352, 268435464, 268443648, 8200, 2097160, 8192, 268443656, 270532616, 0, 270540800, 2105344, 268435456, 268443648, 270532616, 270540808, 8200, 2097152, 268435456, 268435464, 2105344, 2105352, 0, 8, 270532608, 8192, 268443656, 270540800, 2097160, 8, 2105344, 2097152, 268435464, 268443648, 8200, 270540808, 270532608, 270540800, 270532616, 8192, 2105352, 2097160, 0, 268435456, 268443656],
    [1048576, 33555457, 1024, 1049601, 34604033, 0, 1, 34603009, 33555456, 1048577, 33554433, 34604032, 34603008, 1025, 1049600, 33554432, 34603009, 0, 33555457, 34604032, 1048576, 33554433, 33554432, 1025, 1049601, 33555456, 34603008, 1048577, 1024, 34604033, 1, 1049600, 33554432, 1048576, 33555457, 34603009, 1048577, 33555456, 34604032, 1049601, 1025, 34604033, 1049600, 1, 0, 34603008, 33554433, 1024, 1049600, 33555457, 34603009, 1, 33554432, 1048576, 1025, 34604032, 33554433, 34603008, 0, 34604033, 1049601, 1024, 33555456, 1048577],
    [134219808, 131072, 134217728, 32, 131104, 134350880, 134350848, 2048, 134348800, 134219776, 133120, 134348832, 2080, 0, 134217760, 133152, 2048, 134350880, 134219808, 134217728, 134348800, 133120, 133152, 32, 134217760, 2080, 131104, 134350848, 0, 134348832, 134219776, 131072, 133152, 134350848, 32, 2048, 134219776, 134217760, 134348832, 131072, 0, 131104, 134348800, 134219808, 134350880, 133120, 2080, 134217728, 131072, 2048, 134348832, 133152, 32, 134348800, 134217728, 134219808, 134350880, 134217760, 134219776, 0, 133120, 2080, 131104, 134350848]
]

def __des_psbox(input):
    output = 0
    for i in range(8):
        tmp = (input >> (48 - 6 * (i + 1))) & 0x3f
        tmp = (tmp & 0x20) + ((tmp & 1) << 4) + ((tmp & 0x1e) >> 1)
        output ^= des_psbox_table[i][tmp]
    return output

des_fast_safety_psbox_table = [
    [8421888, 0, 32768, 8421890, 8421378, 33282, 2, 32768, 512, 8421888, 8421890, 512, 8389122, 8421378, 8388608, 2, 514, 8389120, 8389120, 33280, 33280, 8421376, 8421376, 8389122, 32770, 8388610, 8388610, 32770, 0, 514, 33282, 8388608, 32768, 8421890, 2, 8421376, 8421888, 8388608, 8388608, 512, 8421378, 32768, 33280, 8388610, 512, 2, 8389122, 33282, 8421890, 32770, 8421376, 8389122, 8388610, 514, 33282, 8421888, 514, 8389120, 8389120, 0, 32770, 33280, 0, 8421378],
    [1074282512, 1073758208, 16384, 540688, 524288, 16, 1074266128, 1073758224, 1073741840, 1074282512, 1074282496, 1073741824, 1073758208, 524288, 16, 1074266128, 540672, 524304, 1073758224, 0, 1073741824, 16384, 540688, 1074266112, 524304, 1073741840, 0, 540672, 16400, 1074282496, 1074266112, 16400, 0, 540688, 1074266128, 524288, 1073758224, 1074266112, 1074282496, 16384, 1074266112, 1073758208, 16, 1074282512, 540688, 16, 16384, 1073741824, 16400, 1074282496, 524288, 1073741840, 524304, 1073758224, 1073741840, 524304, 540672, 0, 1073758208, 16400, 1073741824, 1074266128, 1074282512, 540672],
    [260, 67174656, 0, 67174404, 67109120, 0, 65796, 67109120, 65540, 67108868, 67108868, 65536, 67174660, 65540, 67174400, 260, 67108864, 4, 67174656, 256, 65792, 67174400, 67174404, 65796, 67109124, 65792, 65536, 67109124, 4, 67174660, 256, 67108864, 67174656, 67108864, 65540, 260, 65536, 67174656, 67109120, 0, 256, 65540, 67174660, 67109120, 67108868, 256, 0, 67174404, 67109124, 65536, 67108864, 67174660, 4, 65796, 65792, 67108868, 67174400, 67109124, 260, 67174400, 65796, 4, 67174404, 65792],
    [2151682048, 2147487808, 2147487808, 64, 4198464, 2151678016, 2151677952, 2147487744, 0, 4198400, 4198400, 2151682112, 2147483712, 0, 4194368, 2151677952, 2147483648, 4096, 4194304, 2151682048, 64, 4194304, 2147487744, 4160, 2151678016, 2147483648, 4160, 4194368, 4096, 4198464, 2151682112, 2147483712, 4194368, 2151677952, 4198400, 2151682112, 2147483712, 0, 0, 4198400, 4160, 4194368, 2151678016, 2147483648, 2151682048, 2147487808, 2147487808, 64, 2151682112, 2147483712, 2147483648, 4096, 2151677952, 2147487744, 4198464, 2151678016, 2147487744, 4160, 4194304, 2151682048, 64, 4194304, 4096, 4198464],
    [128, 17039488, 17039360, 553648256, 262144, 128, 536870912, 17039360, 537133184, 262144, 16777344, 537133184, 553648256, 553910272, 262272, 536870912, 16777216, 537133056, 537133056, 0, 536871040, 553910400, 553910400, 16777344, 553910272, 536871040, 0, 553648128, 17039488, 16777216, 553648128, 262272, 262144, 553648256, 128, 16777216, 536870912, 17039360, 553648256, 537133184, 16777344, 536870912, 553910272, 17039488, 537133184, 128, 16777216, 553910272, 553910400, 262272, 553648128, 553910400, 17039360, 0, 537133056, 553648128, 262272, 16777344, 536871040, 262144, 0, 537133056, 17039488, 536871040],
    [268435464, 270532608, 8192, 270540808, 270532608, 8, 270540808, 2097152, 268443648, 2105352, 2097152, 268435464, 2097160, 268443648, 268435456, 8200, 0, 2097160, 268443656, 8192, 2105344, 268443656, 8, 270532616, 270532616, 0, 2105352, 270540800, 8200, 2105344, 270540800, 268435456, 268443648, 8, 270532616, 2105344, 270540808, 2097152, 8200, 268435464, 2097152, 268443648, 268435456, 8200, 268435464, 270540808, 2105344, 270532608, 2105352, 270540800, 0, 270532616, 8, 8192, 270532608, 2105352, 8192, 2097160, 268443656, 0, 270540800, 268435456, 2097160, 268443656],
    [1048576, 34603009, 33555457, 0, 1024, 33555457, 1049601, 34604032, 34604033, 1048576, 0, 33554433, 1, 33554432, 34603009, 1025, 33555456, 1049601, 1048577, 33555456, 33554433, 34603008, 34604032, 1048577, 34603008, 1024, 1025, 34604033, 1049600, 1, 33554432, 1049600, 33554432, 1049600, 1048576, 33555457, 33555457, 34603009, 34603009, 1, 1048577, 33554432, 33555456, 1048576, 34604032, 1025, 1049601, 34604032, 1025, 33554433, 34604033, 34603008, 1049600, 0, 1, 34604033, 0, 1049601, 34603008, 1024, 33554433, 33555456, 1024, 1048577],
    [134219808, 2048, 131072, 134350880, 134217728, 134219808, 32, 134217728, 131104, 134348800, 134350880, 133120, 134350848, 133152, 2048, 32, 134348800, 134217760, 134219776, 2080, 133120, 131104, 134348832, 134350848, 2080, 0, 0, 134348832, 134217760, 134219776, 133152, 131072, 133152, 131072, 134350848, 2048, 32, 134348832, 2048, 133152, 134219776, 32, 134217760, 134348800, 134348832, 134217728, 131072, 134219808, 0, 134350880, 131104, 134217760, 134348800, 134219776, 134219808, 0, 134350880, 133120, 133120, 2080, 2080, 131104, 134217728, 134350848],
]

def __des_fast_safety_psbox(input, ab_key):
    output = 0
    H = ab_key % 40320
    R = [0] * 7
    modulo = 5040
    for i in range(7):
        R[6 - i] = H // modulo
        H %= modulo
        modulo //= (7 - i)
    order = [0] * 8
    for i in range(6, -1, -1):
        place = 7
        for j in range(R[i]):
            while order[place] != 0:
                place -= 1
            place -= 1
        while order[place] != 0:
            place -= 1
        order[place] = i + 1
    for i in range(8):
        tmp = (input >> (42 - 6 * i)) & 0x3f
        output ^= des_fast_safety_psbox_table[order[i]][tmp]
    return output

des_fast_psbox_table = [
    [8421888, 0, 32768, 8421890, 8421378, 33282, 2, 32768, 512, 8421888, 8421890, 512, 8389122, 8421378, 8388608, 2, 514, 8389120, 8389120, 33280, 33280, 8421376, 8421376, 8389122, 32770, 8388610, 8388610, 32770, 0, 514, 33282, 8388608, 32768, 8421890, 2, 8421376, 8421888, 8388608, 8388608, 512, 8421378, 32768, 33280, 8388610, 512, 2, 8389122, 33282, 8421890, 32770, 8421376, 8389122, 8388610, 514, 33282, 8421888, 514, 8389120, 8389120, 0, 32770, 33280, 0, 8421378],
    [1074282512, 1073758208, 16384, 540688, 524288, 16, 1074266128, 1073758224, 1073741840, 1074282512, 1074282496, 1073741824, 1073758208, 524288, 16, 1074266128, 540672, 524304, 1073758224, 0, 1073741824, 16384, 540688, 1074266112, 524304, 1073741840, 0, 540672, 16400, 1074282496, 1074266112, 16400, 0, 540688, 1074266128, 524288, 1073758224, 1074266112, 1074282496, 16384, 1074266112, 1073758208, 16, 1074282512, 540688, 16, 16384, 1073741824, 16400, 1074282496, 524288, 1073741840, 524304, 1073758224, 1073741840, 524304, 540672, 0, 1073758208, 16400, 1073741824, 1074266128, 1074282512, 540672],
    [260, 67174656, 0, 67174404, 67109120, 0, 65796, 67109120, 65540, 67108868, 67108868, 65536, 67174660, 65540, 67174400, 260, 67108864, 4, 67174656, 256, 65792, 67174400, 67174404, 65796, 67109124, 65792, 65536, 67109124, 4, 67174660, 256, 67108864, 67174656, 67108864, 65540, 260, 65536, 67174656, 67109120, 0, 256, 65540, 67174660, 67109120, 67108868, 256, 0, 67174404, 67109124, 65536, 67108864, 67174660, 4, 65796, 65792, 67108868, 67174400, 67109124, 260, 67174400, 65796, 4, 67174404, 65792],
    [2151682048, 2147487808, 2147487808, 64, 4198464, 2151678016, 2151677952, 2147487744, 0, 4198400, 4198400, 2151682112, 2147483712, 0, 4194368, 2151677952, 2147483648, 4096, 4194304, 2151682048, 64, 4194304, 2147487744, 4160, 2151678016, 2147483648, 4160, 4194368, 4096, 4198464, 2151682112, 2147483712, 4194368, 2151677952, 4198400, 2151682112, 2147483712, 0, 0, 4198400, 4160, 4194368, 2151678016, 2147483648, 2151682048, 2147487808, 2147487808, 64, 2151682112, 2147483712, 2147483648, 4096, 2151677952, 2147487744, 4198464, 2151678016, 2147487744, 4160, 4194304, 2151682048, 64, 4194304, 4096, 4198464],
    [128, 17039488, 17039360, 553648256, 262144, 128, 536870912, 17039360, 537133184, 262144, 16777344, 537133184, 553648256, 553910272, 262272, 536870912, 16777216, 537133056, 537133056, 0, 536871040, 553910400, 553910400, 16777344, 553910272, 536871040, 0, 553648128, 17039488, 16777216, 553648128, 262272, 262144, 553648256, 128, 16777216, 536870912, 17039360, 553648256, 537133184, 16777344, 536870912, 553910272, 17039488, 537133184, 128, 16777216, 553910272, 553910400, 262272, 553648128, 553910400, 17039360, 0, 537133056, 553648128, 262272, 16777344, 536871040, 262144, 0, 537133056, 17039488, 536871040],
    [268435464, 270532608, 8192, 270540808, 270532608, 8, 270540808, 2097152, 268443648, 2105352, 2097152, 268435464, 2097160, 268443648, 268435456, 8200, 0, 2097160, 268443656, 8192, 2105344, 268443656, 8, 270532616, 270532616, 0, 2105352, 270540800, 8200, 2105344, 270540800, 268435456, 268443648, 8, 270532616, 2105344, 270540808, 2097152, 8200, 268435464, 2097152, 268443648, 268435456, 8200, 268435464, 270540808, 2105344, 270532608, 2105352, 270540800, 0, 270532616, 8, 8192, 270532608, 2105352, 8192, 2097160, 268443656, 0, 270540800, 268435456, 2097160, 268443656],
    [1048576, 34603009, 33555457, 0, 1024, 33555457, 1049601, 34604032, 34604033, 1048576, 0, 33554433, 1, 33554432, 34603009, 1025, 33555456, 1049601, 1048577, 33555456, 33554433, 34603008, 34604032, 1048577, 34603008, 1024, 1025, 34604033, 1049600, 1, 33554432, 1049600, 33554432, 1049600, 1048576, 33555457, 33555457, 34603009, 34603009, 1, 1048577, 33554432, 33555456, 1048576, 34604032, 1025, 1049601, 34604032, 1025, 33554433, 34604033, 34603008, 1049600, 0, 1, 34604033, 0, 1049601, 34603008, 1024, 33554433, 33555456, 1024, 1048577],
    [134219808, 2048, 131072, 134350880, 134217728, 134219808, 32, 134217728, 131104, 134348800, 134350880, 133120, 134350848, 133152, 2048, 32, 134348800, 134217760, 134219776, 2080, 133120, 131104, 134348832, 134350848, 2080, 0, 0, 134348832, 134217760, 134219776, 133152, 131072, 133152, 131072, 134350848, 2048, 32, 134348832, 2048, 133152, 134219776, 32, 134217760, 134348800, 134348832, 134217728, 131072, 134219808, 0, 134350880, 131104, 134217760, 134348800, 134219776, 134219808, 0, 134350880, 133120, 133120, 2080, 2080, 131104, 134217728, 134350848],
]

def __des_fast_psbox(input):
    output = 0
    for i in range(8):
        tmp = (input >> (42 - 6 * i)) & 0x3f
        output ^= des_fast_psbox_table[i][tmp]
    return output