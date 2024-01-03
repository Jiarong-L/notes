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


<style>
img{
    width: 60%;
}
</style>

教材：《线性代数（同济）》



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
\end{bmatrix}
$$


对角矩阵 $\Lambda = diag(\lambda_1,\lambda_2,\dots,\lambda_n) = 
\begin{bmatrix}
\lambda_1 & 0 & \dots& 0  \\\\
0 & \lambda_2 & \dots& 0  \\\\
 \dots & \dots & \dots & \dots  \\\\
0 & 0 & \dots& \lambda_n  
\end{bmatrix}
$，$\lambda=1$时就是**单位矩阵** $E$ 或者 $I$ 


$$零矩阵O=
\begin{bmatrix}
0 & 0 & \dots \\\\
0 & 0 & \dots \\\\
 \dots & \dots & \dots 
\end{bmatrix}
$$   



* $n$阶矩阵意味着 $n \times n$ 的方阵
* 元素都是实数的矩阵称为**实矩阵**，元素是复数的矩阵称为复矩阵
* 两个矩阵的行数、列数都相等，称为**同型矩阵**










### 向量





























