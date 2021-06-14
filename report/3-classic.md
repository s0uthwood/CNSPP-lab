# 密码学实验第三次实验报告

## 【实验目的】

1. 通过本次实验，了解古典加密算法思想，掌握常见的古典密码；
2. 学会应用古典密码以及针对部分古典密码的破译。

## 【原理简介】

古典密码的编码方法主要有两种，置换和代替。置换密码重新排列明文中的字符顺序，不改变字符本身；代替密码不改变明文中的字符顺序，而是将字符替换成其他字符。置换密码通常包括列置换和周期置换，代替密码则包括单表代替密码和多表代替密码。

## 【实验环境】

使用win10和WSL Ubuntu双系统，主要使用python3。

## 【实验内容】

### 一. 仿射密码

#### 1. 实验原理

加密：$c=(k\cdot p+b)\mod{26}$

解密：$p=((c-b)\cdot k^{-1})\mod{26}$

#### 2. 算法流程

##### 加密算法：

根据实验原理可知，该算法加密部分流程图如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, k, b
id_init=>operation: string res
i=0
id_for=>condition: i < length(msg)
id_calc=>operation: res[i] = (k * msg[i] + b) % 26
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

其伪代码如下：

```
function(msg, k, b):
    string res
    for c in msg:
        res := res + char((k * c + b) % 26)
    return res
```

python实现如下：

```python
def affine_encrypt(msg, k, b):
    res = ''
    for c in msg:
        if c.isalpha() == False: # 增加对非字母的支持
            res += c
            continue
        t = ord('A') if c.isupper() else ord('a') # 增加对大小写的支持
        res += chr((k * (ord(c) - t) + b) % 26 + t)
    return res
```

##### 解密算法：

根据实验原理可知，该算法解密部分流程图如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, k, b
id_init=>operation: string res
i=0
id_for=>condition: i < length(msg)
id_calc=>operation: res[i] = (msg[i] - b) * inv(k, 26) % 26
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

其伪代码如下：

```
function(msg, k, b):
    string res
    for c in msg:
        res := res + char((c - b) * inverse(k, 26) % 26)
    return res
```

python实现如下：

```python
def affine_decrypt(cipher, k, b):
    res = ''
    for c in cipher:
        if c.isalpha() == False:
            res += c
            continue
        t = ord('A') if c.isupper() else ord('a')
        res += chr(((ord(c) - t) - b) * inverse(k, 26) % 26 + t)
    return res
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
print ("affine:")
test_affine = [
    ['iambuaaer', 3, 1],
    ['beijinghuanyingni', 5, 5],
    ['cryptography', 7, 10],
    ['seeyoutomorrow', 9, 13],
    ['tnumumeurnsftsvt', 15, 20],
    ['abcdef', 2, 1]
]

for test in test_affine:
    str = CNSPP.affine_encrypt(test[0], test[1], test[2])
    print ('cipher text: ' + str)
    print ('plain  text: ' + CNSPP.affine_decrypt(str, test[1], test[2]))
```

结果截图如下：

![affine](3-classic\affine.png)

#### 4. 总结

虽然实验中的测试样例仅需要实现小写字母字符串的加解密算法，但为了更好的解决现实问题，确保在遇到符号与大写字母时仍然能正常工作，添加了对符号与大小写的支持。

仿射密码由于在解密时需要求k对26的模逆，因此在对k进行选择时，需要选择可以模逆的数值。

在进行数据测试时，由于在写模逆运算时对无逆的情况进行了报错，而导致了程序无法继续运行，因此将（自己编写的）库文件中的 `raise` 修改为 `print` ，既可以输出错误信息，又避免了报错导致的程序终止。

### 二、单表代换密码

#### 1. 实验原理

这个密码使用了替换的思想，通过建立字母表的映射关系，将明文中的每个字符用对应的字符替换，以实现加密的目的。

#### 2. 算法流程

##### 加密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: string res
i=0
id_for=>condition: i < length(msg)
id_calc=>operation: res[i] = key[msg[i]]
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

伪代码如下：

```
def substitude_encrypt(msg, key):
    string res
    for c in msg:
        res := res + key[int(c)]
    return res
```

python实现如下：

```python
def substitude_encrypt(msg, key):
    res = ''
    key = key.lower()
    for c in msg:
        if c.isalpha() == False: # 增加对非字母字符的支持
            res += c
            continue
        t = 0
        if c.isupper():
            t = ord('a') - ord('A') # 增加对大小写的支持
        res += key[ord(c.lower()) - ord('a') - t]
    return res
```

##### 解密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 cipher, key
id_init=>operation: string res
i=0
id_for=>condition: i < length(cipher)
id_calc=>operation: res[i] = key.index(cipher[i])
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

伪代码如下：

```
def substitude_decrypt(cipher, key):
    res := ''
    for c in cipher:
        res := res + char(key.index(c))
    return res
```

python实现如下：

```python
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
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
print ("\nsubstitude:")
test_substitude = [
    ['doyouthinkphpisthebestlanguage', 'qwertyuiopasdfghjklzxcvbnm'],
    ['doyouwannatodance', 'qazwsxedcrfvtgbyhnujmiklop'],
    ['pysibrjgbxxphbrig', 'qazwsxedcrfvtgbyhnujmiklop']
]
for test in test_substitude:
    str = CNSPP.substitude_encrypt(test[0], test[1])
    print ('cipher text: ' + str)
    print ('plain  text: ' + CNSPP.substitude_decrypt(str, test[1]))
```

结果截图如下：

![substitude](3-classic\substitude.png)

#### 4. 总结

单表代换密码中，所有的明文字母都用一个固定的代换进行加密。从密钥空间来看，凯撒密码与仿射密码都属于单表代换密码的子集。虽然，虽然单表代换密码的密钥空间高达 $26!-1$ 但若明文长度过高，将很容易通过字母频率分析以及语言特性进行破解，因此在进行密码设计时，需要尽可能使得密文中每个字母的出现概率相等。

### 三、维吉尼亚密码

#### 1. 实验原理

维吉尼亚密码是一种特殊的替换密码，为了避免单表代换密码中固定替换而造成的频率问题，可以通过指定一段密钥，将明文与密钥一一对应进行加密。对于26个字母的英语来说，具体的方法是对明文字符与密钥字符进行模26加法，这样可以有效避免频率不同造成的漏洞，解密时根据密钥进行减法即可。

#### 2. 算法流程

##### 加密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: string res
key = cycle(key)
i = 0
id_for=>condition: i < length(cipher)
id_calc=>operation: res[i] = (msg[i] + key[i]) % 26
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

伪代码如下：

```
def vigenere_encrypt(msg, key):
    res := ''
    for c, k in msg, cycle(key):
        res := res + char((int(c) + int(k)) % 26)
    return res
```

python实现如下：

```python
def vigenere_encrypt(msg, key):
    res = ''
    key = key.lower()
    it_key = itertools.cycle(key)
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
```

##### 解密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: string res
key = cycle(key)
i = 0
id_for=>condition: i < length(cipher)
id_calc=>operation: res[i] = (msg[i] - key[i]) % 26
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

伪代码如下：

```
def vigenere_encrypt(msg, key):
    res := ''
    for c, k in msg, cycle(key):
        res := res + char((int(c) - int(k)) % 26)
    return res
```

python实现如下：

```python
def vigenere_decrypt(msg, key):
    res = ''
    key = key.lower()
    it_key = itertools.cycle(key)
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
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
print ("\nvigenere:")
test_vigenere = [
    ['defuzongxiangsihua', 'lemon'],
    ['zhonghuaminzuweidafuxing', 'interesting'],
    ['jcsqusmddoauclvc', 'boring']
]
for test in test_vigenere:
    str = CNSPP.vigenere_encrypt(test[0], test[1])
    print ('cipher text: ' + str)
    print ('plain  text: ' + CNSPP.vigenere_decrypt(str, test[1]))
```

结果截图如下：

![vigenere](3-classic\vigenere.png)

#### 4. 总结

由于维吉尼亚密码中引入了密钥的概念，相同的明文可能对应不同的密文，相同的密文也可能对应不同的明文，因此可以有效避免字母频率以及语言特征等漏洞。

但维吉尼亚密码同样无法有效防止唯密文攻击。其攻击方法大致为：根据多个重合字符串的最大公约数可以估计出密钥长度，随后根据密钥长度划分子串，子串的每一列都是一种凯撒密码，此时再使用字母频率进行破解。

因此，安全的维吉尼亚密码需要让密钥长度与明文长度的比值不能过大，长度相同时才能最大限度保证其安全性。

### 四、福纳姆密码

#### 1. 实验原理

该算法的目的与维吉尼亚密码相同，区别在于该密码将模26加法转换为了模2加法，即异或运算。因此可以直接根据ascii码进行异或运算，若采用一次一密的密钥，该密码便无法被破译。

#### 2. 算法流程

##### 加密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: string res
key = cycle(key)
i = 0
id_for=>condition: i < length(cipher)
id_calc=>operation: res[i] = msg[i] ^ key[i]
id_next=>operation: i = i + 1
id_output=>inputoutput: 输出 res

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_calc->id_next(left)->id_for
```

伪代码如下：

```
function(msg, key):
    res := ''
    for m, k in msg, cycle(key):
        res := res + char(m ^ k)
    return res
```

python实现如下：

```python
def vermam_encrypt(msg, key):
    cipher = bytes([m ^ ord(k) for m, k in zip(msg, itertools.cycle(key))])
    return cipher
```

由于密钥是循环使用的，可以利用python内置的循环迭代工具进行循环迭代，有效减少代码量。由于维吉尼亚密码需要考虑大小写字母与字符，因此无法使用这种方法。

##### 解密算法：

由于使用的是异或运算，该密码的解密算法与加密算法完全相同。

#### 3. 测试样例及结果截图

测试样例如下：

```python
print ("\nvermam:")
fr = open('input1.txt', "rb")
fw = open('output1.txt', "wb")
test_vermam = fr.read()
str = CNSPP.vermam_encrypt(test_vermam, 'Todayis20200308')
fw.write(str)
print (str)

fr = open('input2.txt', 'rb')
fw = open('output2.txt', 'wb')
test_vermam = fr.read()
str = CNSPP.vermam_encrypt(test_vermam, '12345abcde')
fw.write(str)
print (str)
```

由于输出到文件后，包含大量不可见字符，因此同时用python的bytes输出到窗口中，方便查看实际的二进制结果。

结果截图如下：

![vermam](3-classic\vermam.png)

#### 4. 总结

弗纳姆密码在原理上与维吉尼亚密码类似，区别在于将模26加法换成了模2加法（即异或运算），这种计算方式的好处在于加密算法与解密算法完全相同，便于实现，此外，由于其进行的是二进制计算，可以有效扩展密钥空间与明文密文空间，其使用ascii值进行计算的特点，也方便了软件实现。

弗纳姆密码的唯密文攻击方式与维吉尼亚密码相似，可以先通过重合字符串推测出密钥长度，根据密钥长度分为若干个子串，则每个子串在相同位置所对应的密钥是相同的，此时可以根据密钥空间与明文空间不可能出现不可见字符的特点，缩小密钥空间。若最终确定的密钥空间足够小，则可以进行穷举爆破，或根据语言规律对密钥进行选择。

### 五、栅栏密码

#### 1. 实验原理

栅栏密码是最简单的一种移位密码，其加密算法就是将明文分为N个一组，再从每组的选出一个字母连起来，形成一段无规律的密文。

#### 2. 算法流程

##### 加密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: res = ''
length=length(msg)
i=0
id_for=>condition: i < key
id_output=>inputoutput: 输出 res
id_operat=>operation: 选择所有
  下标模key余i的字符
按顺序加入res字符串
id_add=>operation: i = i + 1

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_operat->id_add(left)->id_for
```

伪代码如下：

```
function(msg, key):
    res := ''
    length := length(msg)
    for i from 0 to key - 1:
        forall j % key = i, j < length:
            res := res + msg[j]
    return res
```

python实现如下：

```python
def fence_encrypt(msg, key):
    res = ''
    length = len(msg)
    for i in range(key):
        for j in range(i, length, key):
            res += msg[j]
    return res
```

##### 解密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: res = ''
length=length(msg)
fenthlen=ceil(length / key)
i=0
id_for=>condition: i < fenthlen
id_output=>inputoutput: 输出 res
id_operat=>operation: 选择所有
  下标模fenthlen余i的字符
按顺序加入res字符串
id_add=>operation: i = i + 1

id_start->id_input->id_init->id_for(no)->id_output->id_end
id_for(yes)->id_operat->id_add(left)->id_for
```

伪代码如下：

```
function(msg, key):
    res := ''
    length := length(msg)
    fenthlen := ceil(length / key)
    for i from 0 to fenthlen - 1:
        forall j % fenthlen = i, j < length:
            res := res + msg[j]
    return res
```

python实现如下：

```python
def fence_decrypt(msg, key):
    res = ''
    length = len(msg)
    fenthlen = length // key + (0 if length % key == 0 else 1) # 向上取整
    for i in range(fenthlen):
        for j in range(i, length, fenthlen):
            res += msg[j]
    return res
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
print ("\nfence:")
test_fence = [
    ['whateverisworthdoingisworthdoingwell', 3],
    ['healthismoreimportantthanwealth', 2]
]
for test in test_fence:
    str = CNSPP.fence_encrypt(test[0], test[1])
    print ('cipher text: ' + str)
    print ('plain  text: ' + CNSPP.fence_decrypt(str, test[1]))
```

结果截图如下：

![fence](3-classic\fence.png)

#### 4. 总结

对于栅栏密码来说，其密钥空间最大为密文长度的一半，因为一旦密钥超过长度的一半，其末尾部分明文与密文将完全相同，因此完全可以利用穷举爆破法对栅栏密码进行破解。

### 六、希尔密码

#### 1. 实验原理

希尔密码将明文转化为 $n$ 维向量，与 $n\times n$ 的矩阵相乘，再将结果模 26。

加密的数学模型：
$$
\left(\begin{matrix}c_1 & c_2 & c_3\end{matrix}\right)=\left(\begin{matrix}p_1 & p_2 & p_3\end{matrix}\right)\left(\begin{matrix}k_{11} & k_{12} & k_{13}\\ k_{21} & k_{22} & k_{23} \\ k_{31} & k_{32} & k_{33}\end{matrix}\right)\pmod{26}
$$

解密的数学模型：

$$
\left(\begin{matrix}p_1 & p_2 & p_3\end{matrix}\right)=\left(\begin{matrix}c_1 & c_2 & c_3\end{matrix}\right)\left(\begin{matrix}k_{11} & k_{12} & k_{13}\\ k_{21} & k_{22} & k_{23} \\ k_{31} & k_{32} & k_{33}\end{matrix}\right)^{-1}\pmod{26}
$$

因此对于希尔密码来说，所选择的矩阵必须是在模 26 下可逆矩阵，即密钥矩阵行列式与 26 互质。

#### 2. 算法流程

##### 加密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: 初始化
id_operation=>operation: 将明文长度对齐密钥
id_operation2=>operation: 将明文按照密钥长度进行划分
id_operation3=>operation: 将每段明文与密钥进行计算
id_operation4=>operation: 将计算结果进行拼接

id_start->id_input->id_init->id_operation->id_operation2->id_operation3->id_operation4->id_end
```

伪代码如下：

```
function(msg, key):
    res := ''
    msg := tolower(msg)
    cryptlen := matrix_size(key)
    fill := cryptlen - (len(msg) % cryptlen)
    msg := msg + fill * char(ascii_value('a') + fill)    ; add padding
    msg := split_as_length(msg, cryptlen)                ; cut to substring
    for block in msg:
        res := res + matrix_mult(block, key)
    return res
```

python实现如下：

```python
def hill_encrypt(msg, key):
    res = ''
    msg = msg.lower()
    cryptlen = len(key)
    fill = cryptlen - (len(msg) % cryptlen)
    msg = re.findall('.{' + str(cryptlen) + '}', msg + fill * chr(ord('a') + fill)) # 末尾填充并分组，由于 mod 26的限制，矩阵大小需要在 25 * 25 以内
    for block in msg:
        res += hill_calc(block, key)
    return res
```

需要注意的是，由于实际实现时，明文长度很可能无法整除矩阵的大小，因此需要在结尾增加冗余，以表示最后需要过滤的字符数量，这里选择采用公钥密码学标准第七号 (PKCS#7)，即最后填充 $n$ 个字节的 $n$ 直到对齐，当无需填充时强制填充一行。而这种填充方式下，由于明文空间为模 26，因此矩阵最大不能超过 $25\times 25$，否则将会带来末尾填充错误的问题。

代码中调用的矩阵计算函数如下：

```python
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
```

##### 解密算法：

算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 msg, key
id_init=>operation: 初始化
计算密钥的逆
id_operation2=>operation: 将密文按照密钥长度进行划分
id_operation3=>operation: 将每段密文与密钥的逆进行计算
id_operation4=>operation: 将计算结果进行拼接
id_operation5=>operation: 根据末尾信息
将末尾填充信息删除

id_start->id_input->id_init->id_operation2->id_operation3->id_operation4->id_operation5->id_end
```

伪代码如下：

```
function(msg, key):
    re_key := matrix_inverse(key, 26)
    res := ''
    cryptlen := matrix_size(key)
    msg := split_as_length(msg, cryptlen)                ; cut to substring
    for block in msg:
        res := res + hill_calc(block, de_key)
    fill := value(res[-1])
    return res[:(-fill)] # 返回删除末尾填充的字符串
```

python实现如下：

```python
def hill_decrypt(msg, key):
    de_key = matrix_invmod(key, 26)
    res = ''
    cryptlen = len(key)
    msg = re.findall('.{' + str(cryptlen) + '}', msg) # 使用正则表达式对字符串进行切分
    for block in msg:
        res += hill_calc(block, de_key)
    fill = ord(res[-1]) - ord('a') # 计算末尾填充
    return res[:(-fill)] # 返回删除末尾填充的字符串
```

过程中调用了逆矩阵函数，对于逆矩阵的计算，有高斯消元法，和余子式法，此处选择高斯消元法。

```python
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
        if gcd(div, modulo) != 1:
            for j in range(i + 1, line):
                if gcd(div - mat[j][i], modulo) == 1:
                    for k in range(line):
                        mat[i][k] -= mat[j][k]
                        extra_mat[i][k] -= extra_mat[j][k]
                    div -= mat[j][i]
                    break # 寻找另一行，与最大行进行相减，使得选择的最大行 gcd 为 0
        if gcd(div, modulo) != 1: # 如果 gcd 仍然不为 0，说明不可逆
            return -1
        for j in range(line):
            mat[i][j] *= inverse(div, modulo)
            mat[i][j] %= modulo
            extra_mat[i][j] *= inverse(div, modulo)
            extra_mat[i][j] %= modulo # 将所选择的行通过乘逆取模的方式使得对应位置变为 1
        for j in range(line):
            if j == i:
                continue
            div = mat[j][i]
            for k in range(line):
                mat[j][k] -= mat[i][k] * div
                mat[j][k] %= 26
                extra_mat[j][k] -= extra_mat[i][k] * div
                extra_mat[j][k] %= 26 # 将其余行的这一列化为 0 
    return extra_mat
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
test_hill = [
    ['paymoremoney', [[17, 17, 5], [21, 18, 21], [2, 2, 19]]],
    ['loveyourself', [[5, 8], [17, 3]]],
    ['ysezymxvv', [[6, 24, 1], [13, 16, 10], [20, 17, 15]]],
    ['youarepretty', [[2, 3], [1, 22]]]
]
print ("\nhill:")
for test in test_hill:
    str = CNSPP.hill_encrypt(test[0], test[1])
    print ('cipher text: ' + str)
    print ('plain  text: ' + CNSPP.hill_decrypt(str, test[1]))
```

结果截图如下：

![hill](3-classic\hill.png)

#### 4. 总结

希尔密码难以抵抗已知明文攻击（详见第九个实验）。除此之外，本实验中采用的填充方式同样会带来漏洞，可以用于密码的破解。具体分析如下：

在有较多组不同的密文时，可以根据密文长度之差的最大公约数得知矩阵的大小，若有一个密文的最后一组对应明文均为填充的padding，则可借此获得一部分密钥信息，不同的padding对应的密文相互结合可以有效减少密钥空间，最终得到密钥或者爆破出密钥。特别是当padding为0时，将会影响到最后一组密钥的矩阵乘法运算。

因此，在末尾的填充标准选择上，优先级 ISO 10126 > PKCS7 > ANSI X9.23。

### 七、字母频率攻击

#### 1. 实验原理

在单表代换实验中提到，由于明密文一一对应，其字母频率仍然符合语言的统计特征，因此可以根据字母频率攻击来推测部分密钥，大幅度降低密钥空间。而在凯撒密码中，由于密钥空间较小，直接使用单字母频率即可进行破解。

为了比较各个密钥的概率，选择使用统计学中的卡方统计，可以用于衡量两种分类概率分布相似程度，分布完全相同时卡方统计结果为 $0$，分布完全不同时结果将更高。公式如下：
$$
\chi^2(C,E)=\sum\limits_{i=A}^{i=Z}\dfrac{(C_i-E_i)^2}{E_i}
$$
其中，$C_A$ 是字母 $A$ 的计数，$E_A$ 是字母 $A$ 的预期计数。 卡方统计是由每个字母实际出现次数和预期出现次数之差的平方除以预期出现次数的和。由于对于所有情况来说，对计数的卡方统计与对频率的卡方统计仅相差一个文本长度的乘积，因此完全可以使用频率代替次数进行卡方统计的计算。

#### 2. 算法流程

算法流程图如下：

伪代码如下：

```
function(list):
    true_rate = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    res = []
    for i in range(26):
        res.append(chi_squared(list, true_rate))
        move first object in list to the end
    return res
```

python实现如下：

```python
def attack_caesar(list):
    true_rate = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
    res = []
    for i in range(26):
        res.append(calc_variance(list, true_rate))
        list = list[1:] + list[:1]
    return res
```

计算卡方的代码如下：

```python
def calc_variance(list_a, list_b):
    sum = 0
    for i in range(len(list_a)):
        sum += ((list_a[i] - list_b[i]) ** 2) / list_b[i]
    return sum
```

由于此函数只需要使用字母出现的频率，因此需对密文进行简单的预处理，统计出所有字母的频率，并用列表调用攻击函数。

#### 3. 测试样例及结果截图

测试样例如下：

```python
print ("\ncaesar attack: ")
''' # 生成一个密文
file = open('attack_caesar4.txt')
output_file = open('cipher_article4.txt', 'w')
key = random.randint(1, 25) # 随机生成密钥
for line in file:
    ciphertext = CNSPP.affine_encrypt(line, 1, key)
    output_file.write(ciphertext)
print (key) # 5
'''

file = open('cipher_article2.txt')
count_list = [0] * 26
count_all = 0
for line in file:
    for char in line:
        if char.isalpha():
            count_list[ord(char.lower()) - ord('a')] += 1
            count_all += 1
rate_list = []
for i in count_list:
    rate_list.append(i / count_all * 100) # 以上为统计字母频率
ans = CNSPP.attack_caesar(rate_list) # 进入攻击函数
max_ans = max(ans)
for i in range(len(ans)): # 将结果按照卡方统计由小到大输出
    index = ans.index(min(ans))
    print (index, ans[index])
    ans[index] = max(ans) + 1
```

结果截图如下：

![caesar_attack](3-classic\caesar_attack.png)

#### 4. 总结

对于凯撒密码攻击，可以针对频率最大的字母直接进行偏移，或者寻找最大的四个字母完全匹配上的偏移，但考虑到文本字母过少时，可能频率最大的几个字母与英文中频率最大的字母并非是完美的对应关系，因此计算卡方统计，对任何大小的文本中，都具有一定的适用性。

从结果中可以看到，对于长度较大的文本，正确的密钥与其它密钥在卡方统计上差距十分明显。用这种方法在处理约 200 字母的文本时，虽然无法有图中所示的较大差异，但同样可以产生明显的区别。

在对单表代换密码的攻击中，同样可以使用卡方统计对相似程度进行比对。但由于卡方统计之间的差异极小，因此可以另外使用四元组统计。

如图所示，使用相同的统计方法攻击密钥为 18 的凯撒密码（程序认为是单表代换密码，使用凯撒密码是为了方便对正确性进行判断）：

![substitute_attack](3-classic\substitute_attack.png)

可见各个不同的密钥对应的卡方统计结果都十分接近且明显小于第三节中的结果，因此仅仅依靠单字母频率对单表代换密码进行攻击时，结果并不足够可靠。当然，图中可以看出一半左右的字母被成功破解，而剩下的字母也在某些可能性中被成功破解，且成功破解的字母往往为出现频率最高的一些字母，因此后续完全可以进行人工调整以成功完全破解。

此外还有四元组统计方式，具体方法为，提取文本中所有的四元组，计算每个四元组出现的次数除以这个四元组在大量训练文本中出现的次数，即
$$
p(C_1C_2C_3C_4)=\dfrac{\mathrm{count}(C_1C_2C_3C_4)}{\mathrm{rawcnt}(C_1C_2C_3C_4)}
$$
为避免浮点数精度问题，对其求 $\log$，最终计算所有四元组的对数之和，即
$$
\log(p(\mathrm{article}))=\log(p(C_1C_2C_3C_4))+\log(p(C_5C_6C_7C_8))+\log(p(C_9C_{10}C_{11}C_{12}))+\ldots
$$
分数越高，说明其与训练原始文本越相似，越有可能是英语。

在单表代换攻击时，可以综合两个统计特征进行优化，可以更有效的凭借语言特征而不是语言词汇来进行破解，其意义在于，在面对维吉尼亚密码与福纳姆密码时，同一个密钥字符对应的所有密文字符，仅仅具备字母频率的特征而不具备语言词汇等特征，因此仅使用频率进行分析适用性更广。

### 九、已知明文攻击

#### 1. 实验原理

由于希尔矩阵是依靠矩阵运算进行的加密，因此在明文与密文均知道的情况下，有较大可能能够成功攻击。具体数学原理如下：
$$
\left(\begin{matrix}c_{11} & c_{12} & c_{13} \\ c_{21} & c_{22} & c_{23} \\ c_{31} & c_{32} & c_{33}\end{matrix}\right) = \left(\begin{matrix}p_{11} & p_{12} & p_{13} \\ p_{21} & p_{22} & p_{23} \\ p_{31} & p_{32} & p_{33}\end{matrix}\right)\left(\begin{matrix}k_{11} & k_{12} & k_{13} \\ k_{21} & k_{22} & k_{23} \\ k_{31} & k_{32} & k_{33}\end{matrix}\right)
$$
因此只需要计算明文矩阵的逆矩阵与密文矩阵的乘积即可。

#### 2. 算法流程

算法流程图如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入明文矩阵 密文矩阵 密钥长度
id_init=>operation: 将明文与密文根据密钥长度划分
id_for=>condition: 选择全排列的下一项
id_judge=>condition: 明文矩阵可逆
id_calc=>operation: 计算明文矩阵逆矩阵与密文矩阵的乘积
id_true=>inputoutput: 输出计算结果
id_false=>inputoutput: no answer

id_start->id_input->id_init->id_for(yes)->id_judge
id_for(no)->id_false->id_end
id_judge(yes)->id_calc->id_true->id_end
id_judge(no)->id_for(top)
```

伪代码如下：

```
function(plain, cipher, block_len):
    plain_block := split_as_length(plain, block_len)
    cipher_block := split_as_length(cipher, block_len)
    res := FALSE
    for i, j in permutations(plain_block, block_len), permutations(cipher_block, block_len):
        if matrix_invmod(i, 26) != -1:
            mat_plain := matrix_invmod(i, 26)
            mat_cipher := j
            res := True
            break
    if res = False:
        return 'no answer'
    return matrix_mult(mat_plain, mat_cipher)
```

python实现如下：

```python
def attack_hill(plain, cipher, block_len):
    plain_block = re.findall('.{' + str(block_len) + '}', plain)
    cipher_block = re.findall('.{' + str(block_len) + '}', cipher)
    list_plain_perm = list(itertools.permutations(plain_block, block_len))
    list_cipher_perm = list(itertools.permutations(cipher_block, block_len)) # 利用全排列寻找可逆的明文矩阵
    res = False
    for i, j in zip(itertools.permutations(plain_block, block_len), itertools.permutations(cipher_block, block_len)):
        list_i = [list(k) for k in i]
        list_j = [list(k) for k in j]
        for len_i in range(len(list_i)):
            for len_j in range(len(list_i[len_i])):
                list_i[len_i][len_j] = ord(list_i[len_i][len_j]) - ord('a')
                list_j[len_i][len_j] = ord(list_j[len_i][len_j]) - ord('a')
        if matrix_invmod(copy.deepcopy(list_i), 26) == -1:
            continue
        else:
            mat_plain = matrix_invmod(list_i, 26)
            mat_cipher = list_j
            res = True
            break
    if res == False:
        return 'no answer'
    return mat_mult(mat_plain, mat_cipher)
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
test_hill_attack = [
    ['youarepretty', 'kqoimjvdbokn', 2],
    ['youaresocute', 'ywwpcwsogfuk', 3]
]
for test in test_hill_attack:
    print (CNSPP.attack_hill(test[0], test[1], test[2]))
```

结果截图如下：

![attack_hill](J:\BUAA\2021-spring\CryptoLab\3\attack_hill.png)

#### 4. 总结

希尔密码虽然避免了字母频率分析等等攻击方式，但由于其数学原理过于简单等原因，其安全性同样较低，虽然对于唯密文攻击具有一定的防御能力，但面对选择明文攻击与已知明文攻击，同样很容易被破解。因此需要寻找更加复杂的加密方式。

## 【思考题】

### 1. $m$ 维 Hill 密码破解效率

在不考虑文本选择的情况下（即已经取好了可逆的明文矩阵），其需要的计算大致包括，求逆矩阵、矩阵乘法。

逆矩阵算法中，最多用到了三层 for 循环，因此时间复杂度为 $O(m^3)$；

矩阵乘法算法中，同样用到了三层 for 循环，因此时间复杂度为 $O(m^3)$；

$\therefore $ 在不考虑文本选择的情况下，时间复杂度为 $O(m^3)$

在文本选择时，选择对所有可能的全排列进行迭代，则明文长度为 $n$ 时，最坏情况下的时间复杂度为 $O(C_{\lceil n/m\rceil}^m)$。

### 2. 古典密码体制的缺陷与不足

从实验结果来看，对于古典密码来说，无论是密钥空间极大的单表代换密码，还是隐藏了字母频率的维吉尼亚密码、弗纳姆密码，都可以利用语言上的统计特征进行唯密文攻击。而基于数学运算的希尔密码在数学上也有严重的缺陷。因此，古典密码的安全性依赖于其算法的保密性而不是破解的难度。

例如，猪圈密码、培根密码等密码，其破译难度仅仅取决于破译者是否知晓这种密码。而其它种类的密码一旦被识别出来，同样可以通过相应的手段得到明文。只有明文较短且经过了多重加密的密文能避免被破解。因此不具备实用性。

## 【总结与建议】

经过本次实验，对古典密码的各种加密算法以及相应的破解方式有了一定的了解，并编写代码进行了实践。同时对古典密码中的替换与移位思想有了一定的认识，为后续的现代密码实验做好铺垫。

经过多次的实验课的实践后，认为算法流程图与算法伪代码在功能上重叠，在已经实现了算法的基础上再同时书写流程图与伪代码仅是徒增工作量，降低效率。因此建议二者选其一即可。