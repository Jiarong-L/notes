
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
  },
  svg: {
    fontCache:   'global'   // 'local',or 'global' or 'none'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="http://127.0.0.1:8000/Bioinfo/Statistics/Basis/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://github.com/Jiarong-L/notes/blob/main/docs/Bioinfo/Statistics/Basis/tex-svg.js">
</script>
<!-- src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" -->
<!-- src="http://127.0.0.1:8000/Bioinfo/Statistics/Basis/tex-svg.js" -->


<style>
img{
    width: 60%;
}
</style>


数据降维



## 预备

### 特征值和特征向量

假设对于$n$阶矩阵 $A \in R^{n \times n}$，存在非零列向量 $\vec{v} \in R^{n}$ 使得 $A\vec{v}=\lambda\vec{v}$，则 $\lambda \in R$ 为矩阵$A$的一个**特征值**，$\vec{v}$ 为为矩阵 $A$ 的一个**特征向量**

求解过程：

* $A\vec{v}-\lambda\vec{v}=0$
* $A\vec{v}-\lambda I \vec{v}=0$，$(\because \vec{v}=I\vec{v})$
* $(A-\lambda I)\vec{v}=0$
* $A-\lambda I=0 $，$(\because \vec{v}非零)$
* $
\begin{bmatrix}
a_{11}-\lambda & a_{12} & ... & a_{1n} \\\\
a_{21} & a_{22}-\lambda & ... & a_{2n} \\\\
... & ... & ... & ... \\\\
a_{n1} & a_{n2} & ... & a_{nn}-\lambda 
\end{bmatrix} = 0
$ 可求得多个解 $\lambda_1,\lambda_2,...$
* 将$\lambda_i$代入原式，计算$\vec{v_i}$


[参考1](https://zhuanlan.zhihu.com/p/625791671), [参考2](https://zhuanlan.zhihu.com/p/104980382)

### SVD
（奇异值分解）[参考1](https://zhuanlan.zhihu.com/p/29846048),[参考2](https://zhuanlan.zhihu.com/p/629013736)

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


解法：

* $(A^TA)\vec{v_i}=\lambda_i\vec{v_i}$，对$(A^TA) \in R^{m \times m}$ 求特征值得$\vec{v_i}$与$\lambda_i$

* $(AA^T)\vec{u_i}=\lambda_i\vec{u_i}$，对$(AA^T) \in R^{n \times n}$ 求特征值得$\vec{v_i}$与$\lambda_i$

* $A\vec{v_i}=\sigma_i\vec{u_i}$ 求解奇异值 $\sigma_i = \sqrt{\lambda_i}$


用法：可以用$\Sigma$中最大的k个奇异值来近似表达原矩阵：$A_{m \times n} \approx A_{m \times k} = U_k\Sigma_kV^T_k$


### MDS

假设 $m$ 个样本在原始空间的距离矩阵 $D \in R^{m \times m}$，其 $i$ 行 $j$ 列的元素 $dist_{ij}$ 表示样本 $x_i$ 到 $x_j$ 的距离，多维缩放(Multiple Dimensional Scaling, MDS)的目标是获得样本在 $d'<m$ 维空间的表示，并且**任意样本在低维空间中的距离等于原始空间中的距离**（欧式距离/其它）


* $dist_{i-}^2=\frac{1}{m}\sum\limits_{j=1}^{m}dist_{ij}^2$
* $dist_{-j}^2=\frac{1}{m}\sum\limits_{i=1}^{m}dist_{ij}^2$
* $dist_{--}^2=\frac{1}{m^2}\sum\limits_{i=1}^{m}\sum\limits_{j=1}^{m}dist_{ij}^2$
* 内积矩阵$B$，其元素 $b_{ij} = -\frac{1}{2}(dist_{ij}^2-dist_{i-}^2-dist_{-j}^2+dist_{--}^2)$
* 对内积矩阵$B$进行特征值分解，取 $\Lambda$ 为 $d'$ 个最大特征值构成的对角矩阵，$V$ 为相应的特征向量矩阵
* 得到新矩阵 $\Lambda V^{1/2} \in R^{m \times d'}$，每行是一个样本的低维坐标






## PCA
（主成分分析: 如果一个特征的**方差**很大，则说明这个特征上带有大量的**信息**）[参考1](https://zhuanlan.zhihu.com/p/448641448),[参考2](https://zhuanlan.zhihu.com/p/478417013),[参考3](https://www.cnblogs.com/banshaohuan/p/13308723.html)


1. 预处理矩阵数据 $A_{m \times n}$（标准化/中心化/归一化）
2. 对 $A^TA$ 进行特征值分解，得到特征值 $[\lambda_1\in R,\lambda_2,...]$ 与相应的特征向量 $[\vec{v_1}\in R^{n},\vec{v_2},...]$，即：$PC_i$上保留方差的比例与最大方差的方向
3. 计算原数据集在$PC_i$上的坐标：$A\vec{v_i} = \vec{d_i} \in R^{m}$


## PCoA

关注距离，[示例](https://blog.csdn.net/qq_47369980/article/details/122644823)

1. 对样本集生成距离矩阵 $D$，生态学中常见使用 Jaccard, Bray-Curtis, Unifrac, ...
2. MDS：```cmdscale(D,k=nrow(D)-1,egi=TRUE)```


## NMDS

关注距离的秩次，[示例](https://zhuanlan.zhihu.com/p/559725141)


1. 对样本集生成距离矩阵 $D$，
2. ```metaMDS(D,k=nrow(D)-1)```


## CCA
[参考](https://zhuanlan.zhihu.com/p/52717082)






