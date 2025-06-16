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


**Gaussian Elimination**时，通过交换/加减/缩放行（利用 Permutation Matrix），利用上方行的主元消解下方行的元素，一步步构建上三角状的增广矩阵(Forward Substitution $O(n^3)$)：--- 随后可回溯求解方程(Backward Substitution $O(n^2)$)

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



## Lecture 3 LU Factorization

LU分解 (A = LU) 将一个矩阵分解为下三角矩阵(L)和上三角矩阵(U)的乘积，PLU指进行了行交换的LU。

想象可以通过 Gaussian Elimination 的一系列步骤将矩阵(A)转换为上三角矩阵(U): $\overbrace{E_n...E_3E_2E_1}^{L^{-1}}A = U $

这些步骤中，可以有 row scaling (Diagnal Matrix) 与 row substitution ($I + c e_j e_i^T$，其逆为 $I - c e_j e_i^T$，由于消元的过程总是 j>i，它们都是下三角矩阵)。易得其乘积 $L^{-1}$、其逆的乘积 $L$ 也都是下三角矩阵。


为何进行LU分解？假设对于 $Ax=b$，A固定，每次根据b求解x。LU分解的过程消耗为 $O(n^3)$，但分解结果可以将 $Ax=LUx=b$ 分解为 $Lz = b$ 与 $Ux = z$ 这两个上三角状的矩阵求解问题，此时每次求解消耗为 $O(n^2)$

不过，考虑到数据中的各种噪音，一般会将这个问题改写为 MSE 优化问题 $\min\limits_{x} ||Ax -b||_2$，可向优化式中加入正则项 $\alpha ||x||_2$ (Ridge) 或 $\alpha ||x||_1$ (Lasso) 或 $\alpha ||x||_2 + \beta ||x||_1$ (Elastic Net)，随后取优化式的导数为 0 时的 x 


## Lecture 4 Cholesky Factorization


如果矩阵 C 是正定的对称矩阵，则可对其进行Cholesky分解 ($C = LL^{-1}$) 


每次求一列，可以递归地求得Cholesky分解：

$C = \begin{bmatrix}
c_{11} & C_{21}^T \\\\
C_{21} & C_{22}
\end{bmatrix} = \begin{bmatrix}
l_{11} & 0 \\\\
L_{21} & L_{22}
\end{bmatrix}  \begin{bmatrix}
l_{11} & L_{21}^T \\\\
0 & L_{22}^T
\end{bmatrix} = \begin{bmatrix}
l_{11}^2 & l_{11}L_{21}^T \\\\
l_{11}L_{21} & L_{21}L_{21}^T + L_{22}L_{22}^T
\end{bmatrix}$

1. 求得 $l_{11} = \sqrt{c_{11}}$
2. 求得 $L_{21} = C_{21}/l_{11}$
3. 求得 $ L_{22}L_{22}^T = C_{22} - L_{21}L_{21}^T$
4. 下一个Loop的 $C = L_{22}L_{22}^T$ ，直到分块不能再变小


<details>
  <summary> 其它过程表示：用第k行分块 </summary>

$C = \begin{bmatrix}
C_{11} & C_{12} & C_{13} \\\\
c_{k.}^T & c_{kk} & C_{23} \\\\
C_{31} & C_{32} & C_{33} 
\end{bmatrix}= \begin{bmatrix}
 / & / & / \\\\
 l_{k.}^TL_{11}^T & l_{k.}^Tl_{k.} + l_{kk}^2 & / \\\\
 / & / & / 
\end{bmatrix}$

于是可得 $l_{kk} = \sqrt{ c_{kk} - ||l_{k.}||_2^2}$ 与 $c_{k.} = L_{11}l_{k.}$ 


</details>



<details>
  <summary> Hint 1 : $x^TCx = x^TLL^Tx = |Lx|_2^2$ </summary>

L2 范数？本章节末介绍了一些常见的范数及其图形 (1:05:25)

</details>



<details>
  <summary> Hint 2 : $ECE^T$ 也是对称矩阵</summary>

对于 $C = \begin{bmatrix}
c_{11} & v^T \\\\
v & \widetilde{C}
\end{bmatrix}$  以及   $E = \begin{bmatrix}
1/\sqrt{c_{11}} & 0^T \\\\
r & I_{(n-1)(n-1)} 
\end{bmatrix}$ ， $ECE^T = \begin{bmatrix}
1 & \sqrt{c_{11}}r^T + v^T/\sqrt{c_{11}} \\\\
0 & rv^T +  \widetilde{C}
\end{bmatrix}$， 由于它是对称矩阵，则 $ECE^T = \begin{bmatrix}
1 & 0 \\\\
0 & rv^T +  \widetilde{C}
\end{bmatrix}$


</details>



稀疏矩阵有节约空间的储存方式（只储存非零值），因此过程中应当尽量使用稀疏的矩阵类型，但高斯消元会破坏矩阵的稀疏性("Fill")


这是一个 NP-complete 命题：最小化Cholesky分解中的非零条目数量



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











