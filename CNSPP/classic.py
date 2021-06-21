from .utils import inverse as _inverse, gcd as _gcd
import itertools as _itertools
import re as _re
import copy as _copy


def affine_encrypt(msg, k, b):
    res = ''
    for c in msg:
        if c.isalpha() == False:
            res += c
            continue
        t = ord('A') if c.isupper() else ord('a')
        res += chr((k * (ord(c) - t) + b) % 26 + t)
    return res

def affine_decrypt(cipher, k, b):
    res = ''
    for c in cipher:
        if c.isalpha() == False:
            res += c
            continue
        t = ord('A') if c.isupper() else ord('a')
        res += chr(((ord(c) - t) - b) * _inverse(k, 26) % 26 + t)
    return res


def substitude_encrypt(msg, key):
    res = ''
    key = key.lower()
    for c in msg:
        if c.isalpha() == False:
            res += c
            continue
        t = 0
        if c.isupper():
            t = ord('a') - ord('A')
        res += key[ord(c.lower()) - ord('a') - t]
    return res

def substitude_decrypt(cipher, key):
    res = ''
    key = key.lower()
    for c in cipher:
        if c.isalpha() == False:
            res += c
            continue
        t = 0
        if c.isupper():
            t = ord('a') - ord('A')
        res += chr(key.index(c.lower()) + ord('a') - t)
    return res


def vigenere_encrypt(msg, key):
    res = ''
    key = key.lower()
    it_key = _itertools.cycle(key)
    for c in msg:
        if c.isalpha() == False:
            res += c
            continue
        k = next(it_key)
        if c.isupper():
            t = ord('A')
        if c.islower():
            t = ord('a')
        c = ord(c) - t
        res += chr((c + ord(k) - ord('a')) % 26 + t)
    return res

def vigenere_decrypt(msg, key):
    res = ''
    key = key.lower()
    it_key = _itertools.cycle(key)
    for c in msg:
        if c.isalpha() == False:
            res += c
            continue
        k = next(it_key)
        if c.isupper():
            t = ord('A')
        if c.islower():
            t = ord('a')
        c = ord(c) - t
        res += chr((c - (ord(k) - ord('a'))) % 26 + t)
    return res


def vermam_encrypt(msg, key):
    cipher = bytes([m^ord(k) for m, k in zip(msg, _itertools.cycle(key))])
    return cipher


def fence_encrypt(msg, key):
    res = ''
    length = len(msg)
    for i in range(key):
        for j in range(i, length, key):
            res += msg[j]
    return res

def fence_decrypt(msg, key):
    res = ''
    length = len(msg)
    fenthlen = length // key + (0 if length % key == 0 else 1) # 向上取整
    for i in range(fenthlen):
        for j in range(i, length, fenthlen):
            res += msg[j]
    return res


def hill_calc(block, key):
    X = []
    Y = [0] * len(key)
    for i in range(len(block)):
        X.append(ord(block[i]) - ord('a'))
    res = ''
    for i in range(len(block)):
        for j in range(len(block)):
            Y[i] += X[j] * key[j][i]
        res += chr(Y[i] % 26 + ord('a'))
    return res

def matrix_invmod(mat, modulo):
    line = len(mat)
    extra_mat = [ ([0] * i + [1] + [0] * (line - i - 1)) for i in range(line) ]
    for i in range(line):
        k = i
        for j in range(i + 1, line):
            if mat[j][i] > mat[k][i]:
                k = j
        if mat[k][i] == 0:
            return -1
        div = mat[k][i]
        mat[i], mat[k] = mat[k], mat[i]
        extra_mat[i], extra_mat[k] = extra_mat[k], extra_mat[i]
        if _gcd(div, modulo) != 1:
            for j in range(i + 1, line):
                if _gcd(div - mat[j][i], modulo) == 1:
                    for k in range(line):
                        mat[i][k] -= mat[j][k]
                        extra_mat[i][k] -= extra_mat[j][k]
                    div -= mat[j][i]
                    break
        if _gcd(div, modulo) != 1:
            return -1
        for j in range(line):
            mat[i][j] *= _inverse(div, modulo)
            mat[i][j] %= modulo
            extra_mat[i][j] *= _inverse(div, modulo)
            extra_mat[i][j] %= modulo
        for j in range(line):
            if j == i:
                continue
            div = mat[j][i]
            for k in range(line):
                mat[j][k] -= mat[i][k] * div
                mat[j][k] %= 26
                extra_mat[j][k] -= extra_mat[i][k] * div
                extra_mat[j][k] %= 26
    return extra_mat

def hill_encrypt(msg, key):
    res = ''
    msg = msg.lower()
    cryptlen = len(key)
    fill = cryptlen - (len(msg) % cryptlen)
    msg = _re.findall('.{' + str(cryptlen) + '}', msg + fill * chr(ord('a') + fill)) # 末尾填充并分组，由于 mod 26的限制，矩阵大小需要在 25 * 25 以内
    for block in msg:
        res += hill_calc(block, key)
    return res

def hill_decrypt(msg, key):
    de_key = matrix_invmod(key, 26)
    res = ''
    cryptlen = len(key)
    msg = _re.findall('.{' + str(cryptlen) + '}', msg)
    for block in msg:
        res += hill_calc(block, de_key)
    fill = ord(res[-1]) - ord('a') # 删除末尾填充
    return res[:(-fill)]


def calc_variance(list_a, list_b):
    sum = 0
    for i in range(len(list_a)):
        sum += ((list_a[i] - list_b[i]) ** 2) / list_b[i]
    return sum

def attack_caesar(list):
    true_rate = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    res = []
    for i in range(26):
        res.append(calc_variance(list, true_rate))
        list = list[1:] + list[:1]
    return res


def mat_mult(mat_a, mat_b):
    size_x = len(mat_a)
    size_y = len(mat_b[0])
    size_z = len(mat_b)
    mat_res = [[0 for i in range(size_x)] for j in range(size_y)]
    for i in range(size_x):
        for j in range(size_y):
            for k in range(size_z):
                mat_res[i][j] += mat_a[i][k] * mat_b[k][j]
                mat_res[i][j] %= 26
    return mat_res

def attack_hill(plain, cipher, block_len):
    plain_block = _re.findall('.{' + str(block_len) + '}', plain)
    cipher_block = _re.findall('.{' + str(block_len) + '}', cipher)
    res = False
    for i, j in zip(_itertools.permutations(plain_block, block_len), _itertools.permutations(cipher_block, block_len)):
        list_i = [list(k) for k in i]
        list_j = [list(k) for k in j]
        for len_i in range(len(list_i)):
            for len_j in range(len(list_i[len_i])):
                list_i[len_i][len_j] = ord(list_i[len_i][len_j]) - ord('a')
                list_j[len_i][len_j] = ord(list_j[len_i][len_j]) - ord('a')
        if matrix_invmod(_copy.deepcopy(list_i), 26) != -1:
            mat_plain = matrix_invmod(list_i, 26)
            mat_cipher = list_j
            res = True
            break
    if res == False:
        return 'no answer'
    return mat_mult(mat_plain, mat_cipher)


def search_next(list, T):
    res = []
    for i in range(26):
        for j in range(26):
            if i == j:
                continue
            tmp_list = _copy.deepcopy(list) # 需要使用深复制，否则会改变原始值
            tmp_list[1][i], tmp_list[1][j] = tmp_list[1][j], tmp_list[1][i]
            tmp_list[2] = calc_variance([tmp_list[0][k][0] for k in range(26)], [tmp_list[1][k][0] for k in range(26)])
            if tmp_list[2] > list[2]:
                res.append(tmp_list)
    res.sort(key = lambda tup: tup[2])
    return res[:T]

def attack_substitude(test_rate, T):
    true_rate = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    true_rate = [[true_rate[i], i] for i in range(len(true_rate))]
    test_rate = [[test_rate[i], i] for i in range(len(test_rate))]
    true_rate.sort(key = lambda tup: tup[0], reverse = True)
    test_rate.sort(key = lambda tup: tup[0], reverse = True)
    basic = calc_variance([true_rate[i][0] for i in range(26)], [test_rate[i][0] for i in range(26)])
    ans = []
    queue = [[true_rate, test_rate, basic]]
    while T > 0:
        tmp = min(queue, key = lambda tup: tup[2])
        queue.remove(tmp)
        if len(ans) != 0:
            while tmp[-1] == ans[-1][-1]: # 很可能出现重复情况，需要过滤掉
                tmp = min(queue, key = lambda tup: tup[2])
                queue.remove(tmp)
        ans.append([[tmp[0][i][1], tmp[1][i][1]] for i in range(len(tmp[0]))] + [tmp[2]])
        queue += search_next(tmp, T)
        T = T - 1
    return ans

