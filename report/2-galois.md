# 实验报告

## 【实验目的】

1. 通过本次实验，了解 $GF(2^n)$ 上元素的性质及四则运算；
2. 掌握 $GF(2^n)$ 上的本原多项式的判定和生成算法。

## 【实验环境】

使用了win10和WSL Ubuntu双系统，主要使用python3。

## 【实验内容】

### 一、加减乘除运算

#### 1. 实验原理

对于二元域加法与减法，有
$$
0+0=0,\quad0-0=0\\
0+1=1,\quad0-1=1\\
1+0=1,\quad1-0=1\\
1+1=0,\quad1-1=0
$$
与异或运算相同。

对于乘法，有
$$
101\times11=(11<<2)\oplus(11<<0)
$$
即根据a中1的位置，对b进行相应的左移，并相加。

对于除法，当被除数长度大于等于除数长度时，将除数进行左移对齐并相减，相减的结果进行下一轮计算，并将左移的位数与商相加。而除法的余数就是模数。

#### 2. 算法流程

加减法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入a, b
id_output=>inputoutput: 输出 (a ^ b)
id_start->id_input->id_output->id_end
```

伪代码如下：

```
function(a, b):
	return a ^ b
```

乘法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 a, b
id_init=>operation: ans = 0, i = -1
id_add=>operation: i = i + 1
id_for=>condition: i < len(bin(a))
id_calc=>operation: if a & (1 << i) == 0:
ans = ans ^ (b << i)
id_output=>inputoutput: 输出ans


id_start->id_input->id_init->id_add->id_for(no)->id_output->id_end
id_for(yes, right)->id_calc(top)->id_add(top)
```

伪代码如下：

```
function(a, b):
	ans = 0
	for i from 0 to len(bin(a))
		if a & (1 << i) == 0
			ans = ans ^ (b << i)
	return ans
```

除法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 a, b
id_init=>operation: len_b = len(bin(b))
ans = 0
id_init2=>operation: len_a = len(bin(a))
id_while=>condition: lena >= lenb
id_yes=>operation: a = a ^ (b << lena - lenb)
id_calc=>operation: ans = ans ^ 1 << (lena - lenb)
id_output=>inputoutput: 输出 ans

id_start->id_input->id_init->id_init2->id_while(no)->id_output->id_end
id_while(yes, right)->id_yes->id_calc(right)->id_init2
```

伪代码如下：

```
function(a, b):
    if b == 0:
        return error
    if b == 1:
        return a
    lena = len(bin(a))
    lenb = len(bin(b))
    ans = 0
    while lena >= lenb:
        a = a + (b << lena - lenb)
        ans = ans + 1 << (lena - lenb)
        lena = len(bin(a))
    return GF2(ans)
```

python实现代码如下：

```python
def __add__(self, other):
    return GF2(self.data ^ other.data)
def __sub__(self, other):
    return GF2(self.data ^ other.data)
def __mul__(self, other):
    ans = 0
    for i in range(len(bin(self.data)) - 2):
        if self.data & (1 << i):
            ans ^= other.data << i
    return GF2(ans)
def __truediv__(self, other):
    a, b = self, other
    if b.data == 0:
        raise ValueError("x / 0, error")
    if b.data == 1:
        return a
    lenb = len(bin(b.data)) - 2
    ans = 0
    while lena >= lenb:
        lena = len(bin(a.data)) - 2
        a = a + (b << lena - lenb)
        ans += 1 << (lena - lenb)
    return GF2(ans)
```

#### 3. 测试样例及结果截图

```python
from CNSPP.galois import *

print ("add:")
list_add = [[0x89, 0x4d], [0xaf, 0x3b], [0x35, 0xc6]]
for i in range(len(list_add)):
    print (f'{GF2(list_add[i][0])} + {GF2(list_add[i][1])} = {GF2(list_add[i][0]) + GF2(list_add[i][1])}')

print ("mul:")
list_mul = [[0xce, 0xf1], [0x70, 0x99], [0x00, 0xa4]]
for i in range(len(list_mul)):
    print (f'{GF2(list_mul[i][0])} * {GF2(list_mul[i][1])} = {(GF2(list_mul[i][0]) * GF2(list_mul[i][1])) % pub_modulo}')

print ("div:")
list_div = [[0xde, 0xc6], [0x8c, 0x0a], [0x3e, 0xa4]]
for i in range(len(list_div)):
    print (f'{GF2(list_div[i][0])} / {GF2(list_div[i][1])} = {GF2(list_div[i][0]) / GF2(list_div[i][1])}')
```

测试结果如下：

![test_basic](2-galois\test_basic.png)

#### 4. 总结

由于这是二元域中的运算，加法与减法直接使用异或运算即可，而对于乘法与除法，则仿照高精度算法的思路进行计算，使用位运算，更加清晰直观。

### 二、快速模幂运算

#### 1. 算法流程

取余运算的算法步骤与除法相同，区别在于无需计算商，最终返回余数即可。

二元域下快速模幂算法与整数下快速幂算法相同，只需使用二元域下的加减乘除即可。

python实现代码如下：

```python
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
```

#### 2. 测试样例及结果截图

测试样例如下：

```python
from CNSPP.galois import *

pub_modulo = GF2(0x11b)

print ("pow:")
l_pow = [[0x4d, 63108], [0x7b, 21902], [0x89, 18829], [0x3e, 28928], [0x19, 26460], [0xba, 13563]]
for i in range(len(l_pow)):
    print (f'pow({GF2(l_pow[i][0])}, {l_pow[i][1]}, {pub_modulo}) = {pow(GF2(l_pow[i][0]), l_pow[i][1], pub_modulo)}')
```

结果如下：

![test_pow](2-galois\test_pow.png)

#### 3. 总结

在将基础运算进行重载后，快速幂算法可以直接使用。

### 三、欧几里得算法

#### 1. 算法流程

在原先算法的基础上，使用新运算即可。

python代码如下：

```python
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
```

#### 2. 测试样例及结果截图

测试样例如下：

```python
print("euclid:")
l_euc = [[0x0e, 0xb9, 0x75, 0xac, 0xf8, 0x48, 0xc], [0x74, 0x65, 0x35, 0x59, 0x2e, 0x99, 0x11b]]
for i in range(len(l_euc[0])):
    print (GF2.ex_euclid(GF2(l_euc[0][i]), GF2(l_euc[1][i])))
```

结果如下：

![test_euclid](2-galois\test_euclid.png)

#### 3. 总结

在将基础运算进行重载后，欧几里得算法可以直接使用。

### 四、求元素的逆元

#### 1. 算法流程

调用扩展欧几里得算法即可求得逆元。

python代码实现如下：

```python
def inverse(self, other):
    GCD, x, y = GF2.ex_euclid(self, other)
    return x
```

#### 2. 测试样例及结果截图

测试样例如下：

```python
from CNSPP.galois import *

pub_modulo = GF2(0x11b)

print ("inverse:")
l_inv = [0xc, 0xea, 0x8c, 0xbe, 0x1, 0x2d]
for i in range(len(l_inv)):
    print (GF2.inverse(GF2(l_inv[i]), pub_modulo))
```

结果如下：

![test_inverse](2-galois\test_inverse.png)

#### 3. 快速求逆算法

使用本原多项式 $x$ 构建对数表，来快速计算逆元。

python代码如下：

```python
def fast_inverse_init(a, b):
    inverse_pow_list = []
    inverse_pow_list.append(1)
    for i in range(1, 256):
        inverse_pow_list.append(pow(a, i, b))
    return inverse_pow_list

def fast_inverse(a, b):
    inverse_pow_list = fast_inverse_init(GF2(3), b)
    pos = inverse_pow_list.index(a)
    return inverse_pow_list[255 - pos]
```

### 五、本原多项式的判定与生成

#### 1. 算法原理

根据定义，可以得到本原多项式判定方法：

1. $f(x)$ 是不可约多项式
2. $f(x)$ 可整除 $x^m+1, m=2^n-1$
3. $f(x)$ 不可整除 $x^q+1, q < 2^n-1$

#### 2. 算法流程

判断是否为本原多项式的算法流程如下：

```flow
id_start=>start: start
id_end=>end: end
id_input=>inputoutput: 输入 k
id_init_i=>operation: i = 1
id_add1=>operation: i = i + 1
id_for1=>condition: i < k
id_if1=>condition: k % i == 0
id_false1=>inputoutput: 输出 False
id_init_nm=>operation: n = bin_len(k) - 1
m = (1 << n) - 1
id_if2=>condition: ((1 << m) + 1) % k != 0
id_init_i2=>operation: i = n - 1
id_add2=>operation: i = i + 1
id_for2=>condition: i < (1 << n) - 1
id_if3=>condition: ((1 << i) + 1) % k == 0
id_true=>inputoutput: 输出 True
id_false2=>inputoutput: 输出 False

id_start->id_input->id_init_i->id_add1->id_for1(yes, right)->id_if1(yes)->id_false1->id_end
id_if1(no)->id_add1(top)
id_for1(no)->id_init_nm->id_if2(yes, right)->id_false1
id_if2(no)->id_init_i2->id_add2->id_for2(yes, right)->id_if3(yes)->id_false2->id_end
id_for2(no)->id_true->id_end
id_if3(no)->id_add2(top)
```

伪代码如下：

```
function(k):
	for i from 2 to k - 1:
		if k % i == 0:
			return False
	l = bin_len(k) - 1
	m = (1 << l) - 1
	if ((1 << m) + 1) % k != 0:
		return False
	for i from length to (1 << l) - 2:
		if ((1 << i) + 1) % k == 0:
			return False
	return True
```

python实现如下：

```python
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
```

如需生成某一次数的所有本原多项式，只需要对所有多项式依次判定即可，其python代码如下：

```python
def allPrimitive(k):
    list_prime = []
    for i in range(2 ** (k - 1), 2 ** k):
        if GF2(i).isPrimitive():
            list_prime.append(GF2(i))
    return list_prime
```

#### 3. 测试样例及结果截图

测试样例如下：

```python
from CNSPP.galois import *

print ("0x1cf is Primitive:")
print (GF2(0x1cf).isPrimitive())

print ("all Primitive < 2^9:")
print (allPrimitive(9))
```

结果如下：

![test_primitive](2-galois\test_primitive.png)

共有16个八次本原多项式。

#### 4. 总结

由于数量级较小，本代码选择使用朴素方法生成所有本原多项式。如果需要加快速度，可以使用筛法的方式先对不可约多项式筛选，随后再判断剩下两个条件。

### 六、收获与建议

通过本次实验，我复习了有限域的加减乘除基本运算，学习了本原多项式的判定与生成算法，为后续的密码学学习打下了基础。
