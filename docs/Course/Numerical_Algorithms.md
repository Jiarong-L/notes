<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache:   'global'   // 'local',or 'global' or 'none'
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

[CS955 Applied Numerical Algorithms](https://www.bilibili.com/video/BV1UAD4YWEZW/)

虽然各种编程语言的基础包中已包含各种常见算法的实现


## Lecture 1 小数/误差

数值以二进制形式储存，例如 $463 = 2^8 + 2^7 + 2^6  + 2^3  + 2^2  + 2^1  + 2^0 $，即 ```111001111```

**小数的存储**有多种实现。

fixed-point arithmetic 中，会有 $k$ 位负责整数， $l$ 位负责小数，最终获得 $k+l+1$ 位的二进制数。例如 $463.25 = 2^8 + 2^7 + 2^6  + 2^3  + 2^2  + 2^1  + 2^0 + 2^{-2}$，即 ```11100111101```。其缺点是不够灵活，溢出时会造成各种奇怪错误

Scientific Notation 可以应对极大/极小数（乘法时容易获得），只需储存 $\overbrace{\pm}^{sign} \overbrace{(001111..)}^{percision} \overbrace{b^{n}}^{exponent}$。注意，这种方法可表示的数在数轴上0点周围更加密集 ```--2k-----1k-----21012-----1k-----2k--```，而且需要约定 rounding rules 以及special values (NaN,infty)。例如， IEEE 757 Standard 64-bit double 类型即 ```b=2, p=52, n=[-1022,1023]```$。对于一些特定的任务如AI训练，或许只需要几位小数的精度，也可自行设计数据类型。但目前的电路设计适应当前类型，或许需要重新设计，例如：Google TPU 的 bfloat16

为了减少误差，还可以用 Computational Tree 的方法储存小数 $ a = 1/3 = divide(1,3)$，记得简化。

**小数的比较**受限于精度，Bracketing 方法界定一个重合范围，有重合即相等，例如：```(x±e1) + (y±e2) = (x+y) ± (e1+e2+err)```

误差可以来自 Rounding、离散化、模型、数据。假设：需要寻找使得 $f(x)=a$ 的解 $x^{'}$，我们仅可知 **Backward Error** |$f(x)-f(x^{'})$|，基于此尽量减小 **Forward Error** |$x-x^{'}$|


优化公式合理时(well conditioned)，small Backward Error 可保证 small Forward Error。

定义 Condition Number = Forward/Backward，用泰勒展开简化一下：$\frac{(x+e)-x}{f(x+e)-f(x)} = \frac{e}{f(x)+ef'(x) + \frac{1}{2}e^2f''(x) + ... -f(x)} = \frac{e}{ef'(x) + O(e^2)}= \frac{1}{f'(x) + O(e)}$ ,当 $e \rightarrow 0$ 时 =|$\frac{1}{f'(x)}$|


**小数的加法**有时需要注意顺序，例如当几亿个超小数同一个超大数相加时，如果第一个数是超大数，之后的每一次小数相加都可能被 Rounding 掉。但排序非常耗时，Kahan方法是一种取舍：```((a+b)-a)-b ? 0``` 获取每一次操作的误差值

## Lecture 2 Gaussian Elimination

假设有一个 Linear System: $A^{mn}x^{n}=b^{m}$，可以有如下情况：

Solvable -- One Solution (Completely Determined):  

$\begin{bmatrix}
1 & 0 \\\\
0 & 1 \\\\
\end{bmatrix}  \begin{bmatrix}
x \\\\
y \\\\
\end{bmatrix}  = \begin{bmatrix}
-1 \\\\
1 \\\\
\end{bmatrix} 
$


No Solution (Overdetermined):  

$\begin{bmatrix}
1 & 0 \\\\
1 & 0 \\\\
\end{bmatrix}  \begin{bmatrix}
x \\\\
y \\\\
\end{bmatrix}  = \begin{bmatrix}
-1 \\\\
1 \\\\
\end{bmatrix} 
$

Many Solutions (Underdetermined): 

$\begin{bmatrix}
1 & 0 \\\\
1 & 0 \\\\
\end{bmatrix}  \begin{bmatrix}
x \\\\
y \\\\
\end{bmatrix}  = \begin{bmatrix}
-1 \\\\
-1 \\\\
\end{bmatrix} 
$

A可解的前提是**方阵**（且可逆，即 ```det(A) ≠ 0```）。从维度看，m = 方程数量，n = 未知数数量


**Gaussian Elimination**求解时，通过交换/加减/缩放行（利用 Permutation Matrix），一步步构建上三角状的增广矩阵：

$(A|b)  =\begin{bmatrix}
1 & ? & ? & ? & ? & | b?\\\\
0 & ? & ? & ? & ? & | b?\\\\
0 & ? & ? & ? & ? & | b?\\\\
0 & ? & ? & ? & ? & | b?\\\\
0 & ? & ? & ? & ? & | b?
\end{bmatrix} =\begin{bmatrix}
1 & ? & ? & ? & ? & | b?\\\\
0 & 1 & ? & ? & ? & | b?\\\\
0 & 0 & ? & ? & ? & | b?\\\\
0 & 0 & ? & ? & ? & | b?\\\\
0 & 0 & ? & ? & ? & | b?
\end{bmatrix} = ... =\begin{bmatrix}
1 & ? & ? & ? & ? & | b?\\\\
0 & 1 & ? & ? & ? & | b?\\\\
0 & 0 & 1 & ? & ? & | b?\\\\
0 & 0 & 0 & 1 & ? & | b?\\\\
0 & 0 & 0 & 0 & 1 & | b?
\end{bmatrix} 
$

注，Permutation Matrix 是对角矩阵 diag(1,1,1,...)，其第i行表示为 $e_i^T$。使用时，$ce_i^TA$ 即c倍缩放A的第i行，$e_j e_i^TA$ 即将A的第i行挪至第j行，$(I + e_j e_i^T )A$ 即将A的第i行加至第j行

这一系列过程相当于  $\overbrace{E_n...E_3E_2E_1}^{A^{-1}}(A|b)  = (I |A^{-1}b)$



## Lecture 3













## Lecture 4
## Lecture 5
## Lecture 6
## Lecture 7
## Lecture 8
## Lecture 9
## Lecture 10
## Lecture 11
## Lecture 12
## Lecture 13
## Lecture 14
## Lecture 15
## Lecture 16
## Lecture 17
## Lecture 18
## Lecture 19
## Lecture 20
## Lecture 21
## Lecture 22
## Lecture 23
## Lecture 24
## Lecture 25











