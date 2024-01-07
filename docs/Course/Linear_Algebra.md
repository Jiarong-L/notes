<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="http://127.0.0.1:8000/Statistics/Basis/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://github.com/Jiarong-L/notes/blob/main/docs/Statistics/Basis/tex-svg.js">
</script>


<style>
img{
    width: 60%;
}
</style>

教材：《线性代数（同济）》，略去部分线性方程组的解



## 基本概念

* 先**规定**$n$个不同的元素之间的**标准次序**；在这$n$个元素的当前排列中，某**一对**元素的先后次序与标准次序不同，则构成**1个逆序**；当前排列中所有**逆序的总数**称为这个排列的**逆序数**
    - e.g. 规定标准次序为: 123456..., 某一排列：321 的逆序数=0+1+2
    - 逆序数为奇数的排列称为**奇排列**，需要进行奇数次元素**对换**才能变为标准排列（偶排列 同理）




### 行列式

$$D=
\begin{vmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\\\
a_{21} & a_{22} & \dots & a_{2n} \\\\
 \dots & \dots & \dots & \dots  \\\\
a_{n1} & a_{n2} & \dots & a_{nn} 
\end{vmatrix}=
k \begin{vmatrix}
a_{11}/k & a_{12} & \dots & a_{1n} \\\\
a_{21}/k & a_{22} & \dots & a_{2n} \\\\
 \dots & \dots & \dots & \dots  \\\\
a_{n1}/k & a_{n2} & \dots & a_{nn} 
\end{vmatrix}
$$

$$D=
\begin{vmatrix}
a+b & c+d \\\\
a_{21} & a_{22} 
\end{vmatrix}=
\begin{vmatrix}
a & c \\\\
a_{21} & a_{22} 
\end{vmatrix} + 
\begin{vmatrix}
b & d \\\\
a_{21} & a_{22} 
\end{vmatrix}=
\begin{vmatrix}
a+b+a_{21} & c+d+a_{22} \\\\
a_{21} & a_{22} 
\end{vmatrix}
$$


* $n$阶行列式$D$中，每一个元素$a_{ij}$称为行列式的**元**

* 计算：$D=\sum(-1)^t a_{1p_1}a_{2p_2} \dots a_{np_n}$，其中$p_j$是列标序号，$t$是列标序号排列的逆序数
    - e.g. 二阶行列式 = $(-1)^0a_{11}a_{22}+(-1)^1a_{12}a_{21}$；$p_j$排列分别为(12)、(21)
* 性质（345参考上方示例）
    1. 行列式$D$与它的**转置**行列式$D^T$相等
    2. 对换行列式的两行（列），行列式变号
        * 推论：如果行列式有两行（列）完全相同，则此行列式=0
    3. 行列式**某一行（列）的公因子**可以提取到行列式记号外侧
    4. 若行列式某一行（列）的元素都是两数之和，则可以拆成两个行列式
    5. 将行列式某一行（列）乘以某一数后、按位置加到另一行（列）上，行列式不变

* $(i,j)$元$a_{ij}$的**余子式** $M_{ij}$ 是行列式消除$i$行、$j$列后的(n-1)阶行列式，**代数余子式** $A_{ij}=(-1)^{i+j}M_{ij}$  
    - ![](./Linear_Algebra/1-1.png)
* 展开：行列式等于它的任一行（列）的各元素与其对应的代数余子式乘积之和
    - $D=\sum\limits_{j=1}^na_{ij}A_{ij}$ 按第$i$行
    - $D=\sum\limits_{i=1}^na_{ij}A_{ij}$ 按第$j$列
    - 如果是第$i$行的元与第$k \neq i$行的代数余子式：$\sum\limits_{j=1}^na_{ij}A_{kj}=0$

### 矩阵

$$A_{m \times n}=
\begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\\\
a_{21} & a_{22} & \dots & a_{2n} \\\\
 \dots & \dots & \dots & \dots  \\\\
a_{m1} & a_{m2} & \dots & a_{mn} 
\end{bmatrix} = 
\begin{bmatrix}
B_{r \times c} & B_{r \times (n-c)}  \\\\
B_{(m-r)  \times c} & B_{(m-r) \times (n-c)} 
\end{bmatrix}
$$



**单位矩阵** $E$ 或者 $I=
\begin{bmatrix}
1 & 0 & \dots \\\\
0 & 1 & \dots \\\\
 \dots & \dots & \dots 
\end{bmatrix}$
**零矩阵** $O=
\begin{bmatrix}
0 & 0 & \dots \\\\
0 & 0 & \dots \\\\
 \dots & \dots & \dots 
\end{bmatrix}
$  

<details>
  <summary>克拉默法则求解方程组</summary>

有$n$元线性方程组 $Ax=b$：若 $R(A) \lt R(A,b)$  无解；若 $R(A)=R(A,b)=n$ 有唯一解；若 $R(A)=R(A,b) \lt n$ 有无穷多解  (特别的，$AX=0$有非零解的充分必要条件是$R(A) \lt n$)

$$\begin{cases} 
a_{11}x_1 + a_{12}x_2 + \dots +  a_{1n}x_n = b_1 \\\\ 
a_{21}x_1 + a_{22}x_2 + \dots +  a_{2n}x_n = b_2 \\\\ 
\dots \\\\ 
a_{n1}x_1 + a_{n2}x_2 + \dots +  a_{nn}x_n = b_n
\end{cases} $$

如果 $|A|=
\begin{vmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\\\
a_{21} & a_{22} & \dots & a_{2n} \\\\
 \dots & \dots & \dots & \dots  \\\\
a_{n1} & a_{n2} & \dots & a_{nn} 
\end{vmatrix} \neq 0
$，则有唯一解 $x_i = \frac{|A_i|}{A}$，其中 $|A_i|$ 表示用 $[b_1,b_2,\dots,b_n]$ 取代$|A|$中第$|i|$列  
</details>


* $n$阶矩阵意味着 $n \times n$ 的方阵
* 元素都是实数的矩阵称为**实矩阵**，含复数的矩阵称为**复矩阵**
* 两个矩阵的行数、列数都相等，称为**同型矩阵**
* **对角矩阵** $\Lambda = diag(k_1,k_2,\dots,k_n) = 
\begin{bmatrix}
k_1 & 0 & \dots& 0  \\\\
0 & k_2 & \dots& 0  \\\\
 \dots & \dots & \dots & \dots  \\\\
0 & 0 & \dots& k_n  
\end{bmatrix}
$
    - $\Lambda^k = diag(k_1^k,k_2^k,\dots,k_n^k)$

#### 矩阵运算

*  $A_{m \times n} + B_{m \times n} = C_{m \times n}$ 每个位置的元相加：$c_{ij}=a_{ij}+b_{ij}$
* $A_{m \times n}B_{n \times k} = C_{m \times k}$，其中$c_{ij}=\sum\limits_{k=1}^s a_{ik}b_{ki}$，即 $A$的第$i$行、$B$的第$j$列 元素依次相乘后的和 相加
    - $A^k_{n \times n}=AA...A$，即 $k$个方阵$A$连乘
    - $PA$是$P$**左乘**$A$，$AQ$是$Q$**右乘**$A$
    - $\begin{bmatrix} cos(\theta)  & -sin(\theta)  \\\\ sin(\theta) & cos(\theta)  \end{bmatrix} \begin{bmatrix} x    \\\\ y    \end{bmatrix}$ 意味着将向量$(x,y)$逆时针旋转 $\theta$ 一次
    - 矩阵**分块**后运算法则不变：$AB=\begin{bmatrix} A_{11} & A_{12} \\\\ A_{21} & A_{22} \\\\ A_{31} & A_{32} \end{bmatrix}\begin{bmatrix} B_{11} & B_{12} & B_{13} \\\\ B_{21} & B_{22} & B_{23} \end{bmatrix} = \begin{bmatrix} A_{11}B_{11}+A_{12}B_{21} & \dots & \dots \\\\ \dots & \dots & \dots \\\\ \dots & \dots & \dots \end{bmatrix}$
* 转置：
    - $(A^T)^T=A$
    - $(A+B)^T=A^T+B^T$
    - $(AB)^T=B^TA^T$
    - 如果 $A^T=A$，说明$A$是**对称矩阵**

* 如果 $A^TA=I$，即 $A^{-1}=A^T$，可称 方阵$A$ 为**正交矩阵** 
    - 其行列式 $|A|=1$ （见下文）
    - 如果 $A$、$B$都是正交矩阵，则$AB$也是正交矩阵
    - 正交变换：$\vec{y}=P\vec{x}$，其中$P$是正交矩阵

#### 逆矩阵    

* 方阵$A$的行列式记为 $det A$ 或 $|A|$，当 $|A|=0$ 时 $A$称为**奇异矩阵**，否则称为非奇异矩阵
* 由行列式$|A|$各元素的代数余子式$A_{ij}$组成**伴随矩阵** $A^{\ast}$
    - $A^{\ast}=\begin{bmatrix} A_{11} & A_{21} & \dots \\\\ A_{12} & A_{22} & \dots \\\\  \dots & \dots & \dots  \end{bmatrix}$，$AA^{\ast}=A^{\ast}A=|A|E$


* **逆矩阵**$A^{-1}$
    - $AA^{-1}=A^{-1}A=I$
    - $A^{-1}=\frac{1}{|A|}A^{\ast}$ (使用伴随矩阵求逆矩阵)
    - 大型矩阵可以分块成 **分块对角矩阵**(i.e.除对角线外为零矩阵) 后求小矩阵的逆
* 可逆性
    - 方阵$A$可逆的充分必要条件是：$|A| \neq 0$，即可逆矩阵是非奇异矩阵
    - (方阵$A$可逆的充分必要条件是：存在有限个初等矩阵$P_i$，使$A=P_1P_2...P_n$，即$A$与单位矩阵$I$ 行等价)
    - 可逆矩阵是满秩矩阵

<details>
  <summary>逆矩阵应用示例1</summary>
$AXB = C$，求$X$  <br>
$$A^{-1}AXBB^{-1} = A^{-1}CB^{-1}$$ 
$$IXI = A^{-1}CB^{-1}$$ 
$$X = A^{-1}CB^{-1}$$ 
</details>
<details>
  <summary>逆矩阵应用示例2</summary>
$AP = P\Lambda$，求$A^n$  <br>
$$APP^{-1}=P\Lambda P^{-1}$$
$$A=P\Lambda P^{-1}$$
$$A^n=P\Lambda P^{-1}P\Lambda P^{-1}P\Lambda P^{-1} \dots P\Lambda P^{-1}$$
$$A^n=P\Lambda^nP^{-1}$$
</details>


* **秩**: 任取矩阵$A$中的$k$行、$k$列，得到$A$的$k$阶子式（e.g.取第1,5,6行、1,2,3列，得到3阶行列式）；如果$A$的$r$阶子式是其**最高阶非零子式**，则矩阵$A$的秩为$r$，记为$R(A)=r$
    - **如果两个矩阵等价，则它们的秩相同**
    - Tips：行列式含有零行时，其值=0，所以只有无零行的方阵值不为0；
    - **满秩矩阵（奇异矩阵）** 就是本身无零行的方阵，它的秩等于它的阶数；相对的，**降秩矩阵（非奇异矩阵）** 本身有零行

![](./Linear_Algebra/3-2.png)



#### 初等变换

* 如果矩阵$A$经有限次初等**行变换**变成矩阵$B$，则二者**行等价**，记作$A \overset{r}{\underset{}{\sim}} B$（即$PA=B$）；如果矩阵$A$经有限次初等**列变换**变成矩阵$B$，则二者**列等价**，记作$A \overset{c}{\underset{}{\sim}} B$（即$AQ=B$）；如果矩阵$A$经有限次**初等变换**变成矩阵$B$，则二者**等价**，记作$A \overset{}{\underset{}{\sim}} B$（即$PAQ=B$）
    - $P$，$Q$都可逆
    - 反身性：$A \sim A$
    - 对称性：若 $A \sim B$ 则 $B \sim A$
    - 传递性：若 $A \sim B$、$B \sim C$ 则 $A \sim C$

| 初等行变换r | 同理，初等列变换c | 
| -- | -- |
| 对换 $i$,$j$ 两行 | $r_{i} \overset{}{\underset{}{\leftrightarrow}} r_{j}$ |
| 第$i$行乘$k$ | $r_{i} \times k$ |
| 第$i$行所有元加到第$j$行的对应位置上 | $r_{j} + r_{i} \times k$ |


* 由**单位矩阵**$I$经过**一次**初等变换的矩阵称为**初等矩阵**
    - ($I_rA$)：行变换的初等矩阵$I_r$左乘$A$相当于对$A$施加一致的行初等变换
    - ($AI_c$)：列变换的初等矩阵$I_c$右乘$A$相当于对$A$施加一致的列初等变换



* **行阶梯矩阵** 如下图所示， 
    - ![](./Linear_Algebra/3-1.png)
    - 如果$A$每一行的**首非零元**（红框）值为1、且其所在列其余位置皆为0，则$A$是**行最简形矩阵**
    - 对**行最简形矩阵**施加**列**初等变换，可以将其转换成**标准型** $F=\begin{bmatrix} I & O \\\\ O & O \end{bmatrix}$



<details>
  <summary>求 行最简形矩阵</summary>

已知$A$，求$A$的 行最简形矩阵 $F$，并求一个可逆矩阵$P$，使$PA=F$

$$
(A_{3 \times 3},I_{3 \times 3}) = \begin{bmatrix}
2 & -1 & -1 & 1 & 0 & 0 \\\\
1 & 1 & -2 & 0 & 1 & 0 \\\\
4 & -6 & 2 & 0 & 0 & 1  
\end{bmatrix}

\overset{r}{\underset{}{\sim}}

\begin{bmatrix}
1 & 0 & -1 & -3 & 3 & 1 \\\\
0 & 1 & -1 & 3 & -2 & -1 \\\\
0 & 0 & 0 & 10 & -8 & -3  
\end{bmatrix} = (F_{3 \times 3},P_{3 \times 3}) 
$$
</details>


### 向量

* r个有次序的**数** $[a_1,a_2,\dots,a_r]$ 组成的数组称为 **r维向量**，数 
$a_i$是该向量的第i个**分量**；可以将矩阵$A_{r \times n}$看作为含有n个r维**列向量**的**向量组**
    - 在讨论向量的运算时候，可以将向量看作有向线段
    - 讨论向量集时，可以将单个向量看作一点，则向量集的图形是点的轨迹集合
* 分量全为实数的称为实向量，含复数的称为复向量


#### 向量组

* 给定**n个r维列向量**的**向量组**$A_{r \times n}=[\vec{a_1},\vec{a_2},\dots,\vec{a_n}]$，有一组实数 $\vec{\lambda_{n \times 1}}=[k_1,k_2,\dots,k_n]$ 使得 $\vec{b_{r \times 1}}=A\vec{\lambda}=k_1\vec{a_1}+k_2\vec{a_2}+\dots+k_n\vec{a_n}$，则称向量$\vec{b}$可以由向量组$A$**线性表示**，$\vec{b}$是向量组$A$的一个**线性组合**
    - （$\vec{\lambda}$元素**不全为0时**）如果存在$\vec{\lambda}$使$\vec{b}=0$，则称向量组$A$是**线性相关**的，否则是**线性无关**的 
    - n=2时的线性相关：$\vec{a_1},\vec{a_2}$的分量对应成比例
    -  n=3时的线性相关：三向量共面
    - **线性相关**的充分必要条件是$R(A) \lt n$（$A\vec{\lambda}=0$有**无穷多解**）
    - **线性无关**的充分必要条件是$R(A) = n$（只有**唯一解**：$\vec{\lambda}=0$）
    - 一些结论
        * 若向量组$A=[\vec{a_1},...,\vec{a_n}]$线性相关，则向量组$A'=[\vec{a_1},...,\vec{a_n},\vec{b}]$也线性相关
        * 若向量组$A=[\vec{a_1},...,\vec{a_n}]$线性无关，则向量组$A'=[\vec{a_1},...,\vec{a_n},\vec{b}]$也线性无关
        * 若向量组$A=[\vec{a_1},...,\vec{a_n}]$线性无关 即 $R(A)=n$、向量组$A'=[\vec{a_1},...,\vec{a_n},\vec{b}]$线性相关 即 $n=R(A) \le R(A') = R(A,b)<n+1$，则$A\vec{x}=\vec{b}$有唯一解（$\vec{b}$可以由$A$线性表示）
        * 向量组中，如果向量维度r小于向量个数n，则一定线性相关 即 $R(A) = min(r,n)=r \lt n$     

* 如果向量组$B$中每个向量都能由向量组$A$线性表示，则称向量组$B$能够由向量组$A$线性表示
    - 充分必要条件：$R(A) = R(A,B)$（即 $AX=B$有解）
    - 此时：$R(B) \le R(A)$，因为 $R(AX) \le min(R(A),R(X))$
* 如果向量组$A$、$B$可以相互线性表示，则称两个向量组**等价**
    - 充分必要条件：$R(A)=R(B)=R(A,B)$

* 设有向量组$A$，如果从中**最多**可以选出$r$个向量组成一个线性无关的新向量组$A_0$，则称$A_0$为**最大线性无关向量组**，$r$则是向量组$A$的**秩**，记作$R_A$
    - 任意$(r+1)$个向量的组合都线性相关
    - 向量组$A$的任一向量都可以由向量组$A_0$线性表示
    - 矩阵的秩等于其列向量组的秩，也等于其行向量组的秩


#### 向量空间

* **封闭**：若对某个集合的成员进行一种运算，生成的仍然是这个集合的成员
* 设$V$为r维向量的集合，如果 $V \neq \varnothing$ 且对向量的加法、数乘运算**封闭**，则称$V$为**向量空间**
    - 若 $\vec{a} \in V$，$\vec{b} \in V$，则 $\vec{a}+\vec{b} \in V$
    - 若 $\vec{a} \in V$，$\lambda \in R$，则 $\lambda\vec{a} \in V$
    - 由向量组 $A_{r \times n}=[\vec{a_1},\vec{a_2},\dots,\vec{a_n}]$ 所生成的向量空间 $L=\\\{\vec{x}=k_1\vec{a_1}+k_2\vec{a_2}+\dots+k_n\vec{a_n} | k_i \in \mathbb{R} \\\}$
* 若向量空间 $V_1 \subseteq V_2$，则称$V_1$为$V_2$的**子空间**
* 向量空间$V$内的任一向量都可以由向量组$A$（仅含$r$个线性无关的向量）线性表示，则向量组$A$称为向量空间$V$的**基**，$r$称为向量空间$V$的**维数**，并且称$V$为**r维向量空间**
    - **r维向量空间**也可以理解为：r维向量的全体所组成的集合 $\mathbb{R}^n=\\\{[x_1,x_2,..x_r]^T | x_i \in \mathbb{R}\\\}$ 
* r维向量的集合$\\\{[x_1,x_2,..x_r]^T | a_1x_1+a_2x_2+...+a_rx_r =b \\\}$称为$\mathbb{R}^n$中的(n-1)维超平面
    - 向量集 $\\\{[x,y,z]^T | ax+by+cz=d\\\}$是向量空间$\mathbb{R}^3$中的2维平面

#### 坐标转换

* $A_{r \times ?}\lambda_{? \times l}=x_{r \times l}$，其中 $\lambda_{? \times l}$ 称为 $x_{r \times l}$ 在基 $A$ 中的**坐标**
* 示例：在向量空间$V=\mathbb{R}^3$中取一个基 $A_{3 \times 1}$，再取一个新基 $B_{3 \times 1}$；某向量$\vec{x}$在旧基$A$中坐标为$\vec{o}=[o_1,o_2,o_3]$，在新基$B$中坐标为$\vec{n}=[n_1,n_2,n_3]$
    - 由基变换公式 $AP=B$ 推导出 $P=A^{-1}B$，称为从旧基至新基的**过渡矩阵**
    - 由 $\vec{x}=A\vec{o}=B\vec{n}$ 推导出 **坐标变换**公式：$\vec{n}=B^{-1}A\vec{o}=P^{-1}\vec{o}$



#### 正交

* $||\vec{x}||=1$时，即长度（范数）为1时，称$\vec{x}$为**单位向量**
* 向量的数量积 $\vec{x} \cdot \vec{y} = |\vec{x}| \cdot |\vec{y}| \cdot \cos\theta$
    - 直角坐标系中数量积的计算公式：$[x_1,x_2,x_3] \cdot [y_1,y_2,y_3] = x_1y_1+x_2y_2 +x_3y_3$
    - $\theta=\arccos\frac{\vec{x} \cdot \vec{y}}{||\vec{x}|| \cdot ||\vec{y}||}$，当 $\vec{x} \cdot \vec{y}=0$ 时两向量**正交**

* 若向量组$A$是由两两正交的非零向量组成，则向量组$A$线性无关

* 若从向量空间$V$取单位向量 $\vec{e_1},\vec{e_2},\dots$ 为基，可称为**自然基**；如果这些单位向量两两正交，则称为**标准正交基**


<details>
  <summary>施密特正交化</summary>

从线性无关向量组$A$中导出正交向量组$B$，二者等价: <br>

$$\vec{b_1}=\vec{a_1}$$

$$\vec{b_2}=\vec{a_2}-\frac{\vec{b_1} \cdot \vec{a_2}}{\vec{b_1} \cdot \vec{b_1}}\vec{b_1}$$

...

$$b_r=\vec{a_r}-\sum\limits_{i=1}^{r-1}\frac{b_i \cdot \vec{a_r}}{b_i \cdot b_i}b_i$$


</details>




## 常见矩阵分解

### 特征值分解 Eigen

假设对于$n$阶方阵 $A \in R^{n \times n}$，存在非零列向量 $\vec{x} \in R^{n}$ 使得 $A\vec{x}=\lambda\vec{x}$，则 $\lambda \in R$ 为矩阵$A$的一个**特征值**，$\vec{x}$ 为为矩阵 $A$ 的一个**特征向量**

可以写作 $(A - \lambda I)\vec{x}=0$，其有非零解的充分必要条件是 行列式 $|A - \lambda I|=0$

**一般求解过程**


$$A\vec{x}-\lambda\vec{x}=0$$
$$A\vec{x}-\lambda I \vec{x}=0，(\because \vec{x}=I\vec{x})$$
$$(A-\lambda I)\vec{x}=0$$
其有非零解的充分必要条件是 $A-\lambda I=0 $，$(\because \vec{x}非零)$，展开：


$$
\begin{bmatrix}
a_{11}-\lambda & a_{12} & ... & a_{1n} \\\\
a_{21} & a_{22}-\lambda & ... & a_{2n} \\\\
... & ... & ... & ... \\\\
a_{n1} & a_{n2} & ... & a_{nn} 
\end{bmatrix} = 0
$$ 

可求得特征值的多个解 $\lambda_1,\lambda_2,...$    
随后，将$\lambda_i$代入原式，计算对应的特征向量 $\vec{v_i}$



### 奇异值分解 SVD

$$
\begin{bmatrix}
a_{11} & ... & a_{1n} \\\\
a_{21} & ... & a_{2n} \\\\
... &  ... & ... \\\\
... &  ... & ... \\\\
a_{m1}  & ... & a_{mn} 
\end{bmatrix} = 
\begin{bmatrix}
| & | & ... & ... & ... & | \\\\
| & | & ... & ... & ... & | \\\\
\vec{u_1} & \vec{u_2} & ... & ... & ... & \vec{u_m} \\\\
| & | & ... & ... & ... & | \\\\
| & | & ... & ... & ... & |
\end{bmatrix}
\begin{bmatrix}
\sigma_1 & 0 & ... \\\\
0 & \sigma_2 & ... \\\\
0 & 0 & ...  \\\\
... & ... & ...  \\\\
0 & 0 & ...  
\end{bmatrix}
\begin{bmatrix}
.- & \vec{v_1} & -. \\\\
... & ... & ... \\\\
.- & \vec{v_n} & -.
\end{bmatrix}
$$

任意实矩阵 $A \in R^{m \times n}$ 都可以分解为 $A=U \Sigma V^T$，其中

* $U \in R^{m \times m}, U^TU=I$
* $\Sigma \in  R^{m \times n}, (\Sigma)_{ii}=\sigma_i$ 依次增大，其余部分为0
* $V \in R^{n \times n}, V^TV=I$


**一般求解过程**

* $(A^TA)\vec{v_i}=\lambda_i\vec{v_i}$，对$(A^TA) \in R^{n \times n}$ 求特征值得$\vec{v_i}$与$\lambda_i$

* $(AA^T)\vec{u_i}=\lambda_i\vec{u_i}$，对$(AA^T) \in R^{m \times m}$ 求特征值得$\vec{u_i}$与$\lambda_i$

* $A\vec{v_i}=\sigma_i\vec{u_i}$ 求解奇异值 $\sigma_i = \sqrt{\lambda_i}$


**用法**

可以用$\Sigma$中最大的k个奇异值来近似表达原矩阵：$A_{m \times n} \approx A_{m \times k} = U_k\Sigma_kV^T_k$

SVD分解后的右奇异矩阵$V$，对应着PCA所需的主成分特征矩阵


### QR Decomposition


将矩阵$A$分解：$A=QR$，$QQ^T=I$为正交矩阵，R 是 upper triangle 矩阵
（TBA）





## 其它方阵相关
### 相似对角化





### 二次型化简









## 参考

特征值与特征向量： [参考1](https://zhuanlan.zhihu.com/p/625791671), [参考2](https://zhuanlan.zhihu.com/p/104980382)   
奇异值分解 SVD： [参考1](https://zhuanlan.zhihu.com/p/29846048),[参考2](https://zhuanlan.zhihu.com/p/629013736)    
QR Decomposition： [参考1](https://zhuanlan.zhihu.com/p/47251888)，[参考2](https://zhuanlan.zhihu.com/p/112327923)





