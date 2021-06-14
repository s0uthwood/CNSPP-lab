# 实验报告

## 【实验目的】

本实验主要实现密码学中常见的基础数论算法，为后续密码实验提供可直接调用的函数。

## 【实验环境】

使用了win10和WSL Ubuntu双系统，主要使用python3。

## 【实验内容】

### 一、欧几里得算法

#### 1. 算法流程

##### 欧几里得算法

本算法大致流程如下：

```flow
flowchart
    id_start=>start:         start
    id_input=>inputoutput:     输入x, y
    id_operation=>operation: x = x % y
swap(x, y)
    id_condition=>condition: y != 0
    id_output=>inputoutput: 输出x
    id_end=>end:             end
    id_start->id_input->id_condition
    id_condition(yes, right)->id_operation(top)->id_condition
    id_condition(no)->id_output->id_end
```

伪代码如下：

```
function(x, y):
	while y != 0:
		x = x % y
		swap(x, y)
	return abs(x)
```

python语言实现代码如下：

```python
def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return abs(x)
```

##### 扩展欧几里得算法

本算法大致流程如下：

```flow
flowchart
	id_start=>start: start
	id_input=>inputoutput: 输入x, y
	id_condition=>condition: y != 0
	id_new_matrix=>operation: 新建一个[x, 1, 0][y, 0, 1]的矩阵
	id_calc=>operation: 按照矩阵减法，第一行减第二行
直到第一行首位小于第二行且大于0
	id_swap=>operation: 第一行与第二行进行交换
	id_end=>end: end
	id_start->id_input->id_new_matrix->id_condition(no)->id_end
	id_condition(yes, right)->id_calc(right)->id_swap(right)->id_condition(top)
```

伪代码如下：

```
Function(a, b):
	if b == 0 then
		return a, 1, 0
	else
		d, x1, y1 = Function(b, a mod b)
		x0, y0 = y1, x1 - [a / b] * y1
		return d, x0, y0
```

python实现如下：

```python
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
```

#### 2. 测试样例及结果截图

```python
import CNSPP # 将所有函数整合并放到CNSPP文件夹内，方便调用

def test(x, y):
    ans = CNSPP.utils.gcd(x, y)
    list_a = CNSPP.utils.ex_gcd(x, y)
    assert x % ans == 0
    assert y % ans == 0
    assert x % list_a[0] == 0
    assert y % list_a[0] == 0
    assert list_a[1] * x + list_a[2] * y == list_a[0]
    print (ans, list_a)

test(7,5)
test(31,-13)
test(24,36)
test(2461502723515673086658704256944912426065172925575, 1720876577542770214811199308823476528929542231719)
test(13709616469144948883512229123502305176385931810284088906755090238431898972708904439178898468021710798401875986657125211084472621499595371254346390738382042, 19235039994987625167590963480899777255933775238312044097122773255647530276806317636026727679800825370459321617724871515442147432420951257037823141069640181)
test(96557807278640299121519463045206377934978887298086994211590515571717325955785923783159432436307870512742354877476790046891802153053719263845602618422474671707896136814707875793300040916757228826108499490311295942553478010913043680523612655400526255290702983490382191419067057726624348815391509161304477322782, 146116799305702219220540123503890666704710410600856387071776221592477256752759997798169931809156426471243799795374072510423645363680537337813774268658907130969994146783451692837222772144941434909050652825715582967684984814095461041109999161468223272534833391335036612863782740784573110824091866969655931097032)

```

当出现 `assert 0` 时，会出现如下报错：

![AssertionError](1-utils\AssertionError.png)

WSL Ubuntu Python3 环境下运行结果：

![test_gcd_res](1-utils\test_gcd_res.png)

未出现 `AssertionError`，说明结果正确。

#### 3. 总结

本算法有递归实现与循环实现两种实现方式，在本实验中，我选择使用循环实现，相较于递归，可以节省一定的空间与时间消耗。

此外，由于可能出现负数，在欧几里得算法中，选择返回结果的绝对值，在扩欧算法中，判断是否需要取相反数。

### 二、厄拉多塞筛法

#### 1. 算法流程

本算法大致流程如下：

```flow
flowchart
    id_start=>start:         start
    id_input=>inputoutput:     输入n
    id_iferror=>condition: n < 2
    id_operation=>operation: 构建一个大小为n的bool数组is_prime将0和1设置为False，其余为True
令i=2,3,...,n，当is_prime[i]为真时，将i的倍数的is_prime赋值为False
    id_output=>inputoutput: 输出x
    id_end=>end:             end
    id_start->id_input->id_iferror
    id_iferror(yes)->id_end
    id_iferror(no)->id_operation->id_end
```

伪代码如下：

```
Function(n)
	initialize flag = [True, True, ..., True] // flag.length = n + 1
	for i = 2 to sqrt(n)
		if flag[i] == True then
			set j = i * i
			while j < n
				set flag[j] = False
				compute j += i
	return x if flag[x] = Ture for x = 2 to n
```

python实现代码如下：

```python
def all_prime(n):
    if n < 2:
        raise ValueError("n < 2, range(2, n) error") # n < 2时，抛出异常
    prime = [ False ] * (n // 2) # 在对于较大数据时，可以不判断偶数，节省一定空间和时间
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
```

#### 2. 测试样例及结果截图

WSL Ubuntu Python3 环境下进行测试

```python
import CNSPP

n1 = [2, 103]
n2 = [10000, 1000000, 4275117753]
for n in n1:
    print (CNSPP.utils.all_prime(n))

for n in n2:
    ans = CNSPP.utils.all_prime(n)
    print (ans[-20:])
    print (len(ans))

```

结果为

![test_prime_res](1-utils\test_prime_res.png)

#### 3. 总结

为计算较大数据，在原算法基础上进行如下优化：

1. 在初始化flag数组时只为大于3的奇数开辟空间，在处理较大数据时可节省大量内存；
2. 在初始化数组的基础上，将原先的 `sqrt(n) + n` 次循环压缩为 `n / 2` 次循环；
3. 在素数筛法上，原先的筛法会出现大量的重叠，将 `2 * i` 开始更改为 `i * i` 开始，可以减少一部分重叠情况；
4. 经过测试，python中效率 `[ True for i in range(n) ]` < `[True] * n` ，因此选择后者。

### 三、快速幂

#### 1. 算法流程

本算法大致流程如下：

```flow
flowchart
	id_start=>start: start
	id_input=>inputoutput: 输入x, n, m
	id_init=>operation: d = 1
	id_while=>condition: n > 0
	id_condition=>condition: n mod 2 == 1
	id_compute=>operation: d = (d * x) mod m
	id_set=>operation: n = (n - (n mod 2)) / 2
x = (x * x) mod m
	id_output=>inputoutput: 输出d
	id_end=>end: end
	
	id_start->id_input->id_init->id_while(no)->id_output->id_end
	id_while(yes, right)->id_condition
	id_condition(yes)->id_compute(right)->id_set
	id_condition(no)->id_set
	id_set(right)->id_while(top)
```

伪代码如下：

```
function(x, n, m)
	initialize d = 1
	while n > 0:
		if n mod 2 == 1 then
			compute d = (d * x) mod m
			set n = (n - 1) / 2
		else
			set n = n / 2
		set x = (x * x) mod m
	return d
```

python实现代码如下：

```python
def my_pow(a, b, m):
    d = 1
    while b > 0:
        if b & 1:
            d = (d * a) % m
        b >>= 1
        a = (a * a) % m
    return d
```

#### 2. 测试样例及结果截图

测试文件代码如下：

```python
import CNSPP

def test(a, b, c):
    ans = CNSPP.utils.my_pow(a, b, c)
    print (ans)
    assert ans == pow(a, b, c) # 与内置的pow函数进行结果对比，若不相等将报错
    return

a = [7, 5, 1494462659429290047815067355171411187560751791530, 
22490812876539885046336053040043361022772062226905764414319531416752624982967181455912526153033030222985778230314070837549143068021815197910334221004333099, 
237218075278892229535140238768762235405145645557640724744207466370544846457682663369976322798944392433104280595584635896821245048737637289361896703300454795175488861724813324867455119120284612785871304351940501930714775024417724051440337510897547661217466354700893011496892348407228806138461120064957907686566, 
448491664748214835887077572737743989471818983924746533195711112723370968680112145505675868905886297697651811535959153343019297445815718781370807622258565317729681110144781420923700723193680834808549790079348059612669341617763791748262779560287414722951999863579554855226385841903174595011558143906566236113746355880815410935162653615576832860612181499713446185302492149321184607038850277]
b = [16, 1003, 65537, 65537, 65537, 
266848195381815818463717950266554236453862598799637312683425703733349860929573593996414020829279843574050749733141808826377733991992433000295290381444934817157435190251178268111713086611665708753888640498769964215272509919856595016440707694201919276657450513307401642404169770745634306482286288562684063317756864776774548994812022552274677735053131675109617882635817658233698378909301711242970820585209428037532351125028227556492657705501994644156977193457255573644987541990311834672767028439520378145222935082885623390192713665176848108677291865357438200]
c = [3, 31, 2268838711304724304304396119509416774597723292474, 
26381036806254391211255825330031625908895486635496820170811397576118892705526151526139312916798859030242219181178517837920904022720459931859633170905729517, 
349972806688784936669965759420500287481274799328355633592840001661382340587247200055746522814275902430370330954725697648747610084477917676220179203273361291098368287612837135979510900982047154261023406927515096043384562410643544643505195484211397819374480917731785250826080723518532061522456937734714740424476, 
26449610480694582663087914798262349275307583705769208320615999887968533547578043032399193471649467130397212338172281740898344480836053483980415141663259446884375373371451231004101622624801199838411707260636384692208754088842619258012627585405663559933995516981379631336446313020148817646717985549051301115238527677472914852742788256890259402224899453419484216558327523122341749054612967901747155276100157913910547784136439888489952724508554613632641420487039242881743232756168292709989984925436911267322885917953348064673021283822937158706678666372103627074163021260578078017304088904154859161289037070912220207946945]

for i in range(len(a)):
    test(a[i], b[i], c[i])
```

WSL Ubuntu环境下运行结果：

![test_pow_res](1-utils\test_pow_res.png)

没有出现assert报错，说明结果正确。

#### 3. 总结

常规的幂计算中依次进行乘法，而在快速幂中，使用了平方的方法快速求解，将时间复杂度从 $O(n)$ 减小为 $O(log n)$。

### 四、中国剩余定理

#### 1. 扩展中国剩余定理算法的原理

不妨设 $x\equiv b_1\pmod{a_1}, x\equiv b_2\pmod{a_2}$

有 $x = a_1k_1+b_1 = a_2k_2+b_2$

$a_1k_1=a_2k_2+b_2-b_1$

$\therefore (b_2-b_1)\mid (a_1, a_2)$

$\therefore \dfrac{a_1}{(a_1, a_2)}k_1\equiv \dfrac{b_2-b_1}{(a_1, a_2)}\pmod{\dfrac{a_2}{(a_1, a_2)}}$

$\therefore k_1\equiv \left(\dfrac{a_1}{(a_1, a_2)}\right)^{-1} * \dfrac{b_2-b_1}{(a_1, a_2)}\pmod{\dfrac{a_2}{(a_1, a_2)}}$

$\therefore k_1=inv\left(\dfrac{a_1}{(a_1, a_2)}, \dfrac{a_2}{(a_1, a_2)}\right) * \dfrac{b_2-b_1}{(a_1, a_2)}+\dfrac{a_2}{(a_1, a_2)} * k$

$\therefore x = a_1*inv\left(\dfrac{a_1}{(a_1, a_2)}, \dfrac{a_2}{(a_1, a_2)}\right) * \dfrac{b_2-b_1}{(a_1, a_2)}+\dfrac{a_1a_2}{(a_1, a_2)} * k + b_1$

$\therefore x \equiv a_1*inv\left(\dfrac{a_1}{(a_1, a_2)}, \dfrac{a_2}{(a_1, a_2)}\right) * \dfrac{b_2-b_1}{(a_1, a_2)}+ b_1\pmod{\dfrac{a_1a_2}{(a_1, a_2)}}$

对于多组数据的计算，每次选择前两组进行计算，整合后继续与下一组计算即可。

#### 2. 算法流程

中国剩余定理算法大致流程如下：

```flow
id_start=>start: start
id_input=>inputoutput: 输入a, m, k
id_operation1=>operation: M = m[1] * m[2] * ... * m[k]
id_operation2=>operation: e[i] = inverse(M / m[i], m[i])
id_operation3=>operation: sum = 0
id_operation4=>operation: sum = sum + M / m[i] * e[i] * a[i]
id_output=>inputoutput: 输出sum mod M
id_end=>end: end
id_start->id_input->id_operation1->id_operation2->id_operation3->id_operation4->id_output->id_end
```

算法伪代码如下：

```
function(a, m , k)
	compute M = m[1] * m[2] * ... * m[k]
	for i = 1 to k
		compute e[i] = inverse(M / m[i], m[i])
	set sum = 0
	for i = 1 to k
		compute sum += M / m[i] * e[i] * a[i]
```

算法及扩展算法的python实现如下：

```python
def inverse(a, n):
    if n < 2:
        raise ValueError("n < 2, error")
    g, x, y = ex_gcd(a, n)
    if g != 1:
        raise ValueError("gcd(a, n) != 1, no inverse modular")
    return x % n

def crt(a, m, k):
    M = 1
    for i in m:
        M *= i
    e = [ 0 for i in range(k) ]
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
```

在实现该算法时，需要计算逆元，因此通过 `inverse` 函数调用了扩欧算法。在扩展中国剩余定理算法中，同时调用了欧几里得算法。

#### 3. 测试样例及结果截图

```python
import CNSPP

def test(a, m, k):
    x = CNSPP.utils.ex_crt(a, m, k)
    for i in range(k):
        assert x % m[i] == a[i] % m[i]
    return x

a = [[0, 0, 0], [5, 20, 34], [283, 102, 23], [802310684485241212312289432691586430708135062249, 961714109955647014172499578071923389425123540027, 1381194006087304024683552712488022595194097928701], [8157969540288411637818433039558323184074779086100165504668538221920170369774913261335059602331627321130656458962980224196880533337839226059601303464776145, 9699616044315021194953572561076502992783130623216574220426043600142343504101508838526221359049417564415801914072315788919275792502477693022853881785198116, 7832693802256371667866514213119452199821916193668106904135812283217637737600922381702016472708855675649121271702977408217814917908566132517503707494037556]]

m = [[23, 28, 33], [23, 28, 33], [23, 28, 33], [489808178709479466279507878773770708214878979673, 896234965496726578561614071442814700467907036641, 1213827005758305602466882992172310409456053868843], [13392316081651420877308875276166772808601812122052371442339078877740399569281672683820206196320955005869072002883847646526584107260355414977120453263391947, 9734466939658282823343760206593283968765904848250021580218634383869090913086348857668999272399075016287736914000854272239315769632719896968098820774563511, 9460200357790728398862913232664036038694521858415765931064505193755202156521446156499075450033429983317127589636591133111239548821251790171694322930011927]]
```

WSL Ubuntu Python3 运行结果：

![test_crt_res](1-utils\test_crt_res.png)

未出现报错，说明结果正确。

#### 4. 总结

本算法中，难点在于模数不互素的情况，无法直接计算逆元。对此采用数学求解的方式，使用扩展中国剩余定理的方法进行求解。

### 五、Miller_Rabin法判断质数

#### 1. 算法流程

伪代码如下：

```
test(n)
	找出k, q (k > 0, q为奇数), s.t. (n - 1 = 2 ^ k * q)
	随机选择整数a (1 < a < n - 1)
	if a ^ q mod n == 1
		return True
	for j = 0 to k - 1
		if a ^ (2 ^ j * q) mod n = n - 1
			return True
	return False
```

多次重复test函数，若均返回True，则可以相信n为素数

python实现如下：

```python
from random import randint # 使用基本python函数生成随机数

def is_prime_miller(n):
    primelist = all_prime(1000) # 通过使用小质数进行简单判断，可进行初步筛选，并提高较小数据的判断准确性
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
```

在该算法中，调用了快速幂算法，以及python内部的随机数生成算法。

#### 2. 测试样例及结果截图

测试程序如下：

```python
import CNSPP
from Crypto.Util.number import isPrime # 使用pycrypto库中的素数检测进行对拍

def check(n):
    assert isPrime(n) == CNSPP.utils.is_prime_miller(n) # 对拍，不相等时将报错
    print('sat', CNSPP.utils.is_prime_miller(n)) # 若对拍结果正确，则输出sat

n = [1000023, 1000033, 100160063, 1500450271, 1494462659429290047815067355171411187560751791530, 22490812876539885046336053040043361022772062226905764414319531416752624982967181455912526153033030222985778230314070837549143068021815197910334221004333099, 173114538715442253801652636578504897235814058376012019984132280493073144140873423822066926533851768593567972986030786930865304524765873917291156820356593465395949615668311730524585862713216977118030162614331116320577533153712280997129347743623082819252354000224098702300466561157715990374851814717133985999661]

for i in n:
    check(i)
```

WSL Ubuntu20 Python3环境下测试结果为：

![test_miller_res](1-utils\test_miller_res.png)

#### 3. 总结

可以证明，miller-rabin算法一次检测的错误率为 $\dfrac{1}{4}$，则多次检测后，错误率为 $\left(\dfrac{1}{4}\right)^n$，在实现时，选择 $n=15$ ，此时错误率约为 $10^{-9}$。

