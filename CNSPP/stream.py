from utils import gcd

def BBS(p, q, s, num):
    if(p % 4 != 3 or q % 4 != 3):
        print ("error p, q")
        return 0
    n = p * q
    if (gcd(n, s) != 1):
        print ("error s")
        return 0
    X = [s ** 2 % n]
    B = [X[0] & 1]
    for i in range(num):
        X.append(X[-1] ** 2 % n)
        B.append(X[-1] & 1)
    return X, B

def __rc4_init(key):
    keylength = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_crypt(key, data):
    S = __rc4_init(key)
    i = j = 0
    result = b''
    for a in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = (a ^ S[(S[i] + S[j]) % 256]).to_bytes(1, 'big')
        result += k
    return result

if __name__ == "__main__":
    from libnum import n2s, s2n
    X, B = BBS(383, 503, 101355, 20)
    for i in range(21):
        print (X[i], B[i])
    test_rc4 = [
        [0x6e6f742d736f2d72616e646f6d2d6b6579, 0x476f6f6420796f752061726520636f7272656374],
        [0x3475bd76fa040b73f521ffcd9de93f24, 0x1b5e8b0f1bc78d238064826704830cdb],
        [0x2b24424b9fed596659842a4d0b007c61, 0x41b267bc5905f0a3cd691b3ddaee149d],
        [0x0f1571c947d9e8590cb7add6af7f6798, 0x0123456789abcdeffedcba9876543210]
    ]
    def convert(k):
        ret = []
        while k > 0:
            ret.append(k & 0xff)
            k >>= 8
        return ret[::-1]
    for test in test_rc4:
        cipher = rc4_crypt(convert(test[0]), convert(test[1]))
        print ('cipher:%x' % int.from_bytes(cipher, 'big', signed = False)) # 如果使用 s2n，某些字符会被转义，影响结果正确性
