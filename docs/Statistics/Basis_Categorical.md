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
<script type="text/javascript" id="MathJax-script" async
  src="http://127.0.0.1:8000/Bioinfo/Statistics/Basis/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://github.com/Jiarong-L/notes/blob/main/docs/Bioinfo/Statistics/Basis/tex-svg.js">
</script>

<style>
img{
    width: 60%;
}
</style>




教材：《统计学（原书第五版）》  
**关联：[点估计$\hat{\theta}$、置信区间](Basis.md#10)，[离散分布](Basis.md#5)**



对于分类（类型）数据的统计可以制成 单向表 与 双向表（又称：列联表）；此外，分类数据的回归分析见 [Basis_Regression 定性变量](Basis_Regression.md#_14)

## 单向表

### 示例
单向表只有一行；e.g. A，B，C 三条生产线当日生产的产品数分别为 22，19，20

| A | B | C |
| -- | -- | -- |
| 22 | 19 | 20 |

### 类型概率推断

考虑一个多项实验（见），它有$N$次独立试验，每次试验都有$k$个可能结果，得到下表：

| 1 | 2 | 3 | ... | k |
| -- | -- | -- | -- | -- |
| $n_1$ | $n_2$ | $n_3$ | ... | $n_k$ |


将多项实验简化二项实验（一系列0/1试验）：选取 $n_i$ 为S样本，$\sum (其余所有n_j$) 为F样本；于是：

* $i$类型 二项参数 成功率$p_i$ 
  - 点估计 $\hat{p_i}=\frac{n_i}{N}$
  - $E(\hat{p_i})=p_i$
  - $V(\hat{p_i})=\frac{p_i(1-p_i)}{N}$
  - $p_i$ 的置信区间：$\hat{p_i} \pm z_{\alpha/2}\sqrt{\frac{\hat{p_i}(1-\hat{p_i})}{N}}$；随即可以知晓 $n_i=Np_i$ 的置信区间


* 一对类型（$i$,$j$）的概率差： $E(\hat{p_i}-\hat{p_j})=p_i-p_j$，
  - $Cov(\hat{p_i},\hat{p_j})\\=E[(\hat{p_i}-p_i)(\hat{p_j}-p_j)]\\=E[(\frac{n_i}{N}-p_i)(\frac{n_j}{N}-p_j)]\\=\frac{1}{N^2}E[(n_i-Np_i)(n_j-Np_j)]\\=\frac{1}{N^2}Cov(n_i,n_j)\\=\frac{1}{N^2}(-Np_ip_j)\\=\frac{-p_ip_j}{N}$
  - $V(\hat{p_i}-\hat{p_j})\\=V(\hat{p_i})+V(\hat{p_j})-2Cov(\hat{p_i},\hat{p_j})\\=\frac{p_i(1-p_i)}{N}+\frac{p_j(1-p_j)}{N}+\frac{2p_ip_j}{N}$
  - $p_i-p_j$ 的置信区间：$(\hat{p_i}-\hat{p_j}) \pm z_{\alpha/2}\sigma_{(\hat{p_i}-\hat{p_j})}$
  - 即：$(\hat{p_i}-\hat{p_j}) \pm z_{\alpha/2}\sqrt{V(\hat{p_i}-\hat{p_j})}$


* 假设检验
  - $H_0: p_1=p_2=p_3=...=p_k=\frac{N}{k}$
  - $H_a: 至少有一对概率不相等$
  - $n_i,E(n_i)$ 由 $p_i,E(p_i)$求得
  - 检验统计量 $\chi^2=\sum\limits_{i=1}^{k}\frac{[n_i-E(n_i)]^2}{E(n_i)}$，$df=k-1$
  - 如果**离差**$[n_i-E(n_i)]^2$较大，则$\chi^2$的预期将大于期望（理想状态下，观测值与期望值应该相等，离差为0）
  - （上侧检验）拒绝阈：$\chi^2 > \chi^2_{\alpha}$



## 双向表

### 示例
一般的 $r \times c$ 列联表 有$r$行 $c$列 $N=r \times c$单元；e.g. 生产线 W1 当日生产的 V1 产品数为 100

| - | W1 | W2 | W3 |
| -- | -- | -- | -- |
| V1 | 100 | 19 | 20 |
| V2 | 6 | 8 | 7 |
| V3 | 10 | 16 | 12 |
| V4 | 11 | 15 | 13 |

每个单元用 $n_{rc}$ 表示，例如：$n_{12}=19$   
行、列可视为两个变量：W变量有3个类型，V变量有4个类型

### 类型概率推断


* **独立性检验**：
  - （大样本）每个单元的期望计数 > 5
  - $H_0$：W、V 两个变量相互独立
  - $H_a$：W、V 两个变量相关
  - $\hat{E}(n_{ij})=N\times第i行边缘概率\times第j列边缘概率=\frac{(第i行和)(第j列和)}{N}$
  - 检验统计量 $\chi^2=\sum\limits_{j=1}^{c}\sum\limits_{i=1}^{r}\frac{[n_{ij}-\hat{E}(n_{ij})]^2}{\hat{E}(n_{ij})}$，$df=(r-1)(c-1)$
  - 如果**离差**$[n_{ij}-\hat{E}(n_{ij})]^2$较大，则$\chi^2$的预期将大于期望（理想状态下，观测值与期望值应该相等，离差为0）
  - （上侧检验）拒绝阈：$\chi^2 > \chi^2_{\alpha}$



* Fisher 精确检验：对 $2 \times 2$ 或 $2 \times c$ 的双向表进行更加**精确的独立性检验**
  - （小样本）
  - $2 \times c$ 表中可选一列为 Positive，合并其余列，由是等效于$2 \times 2$ 表
  - 超几何 RECALL: 集合N由r个S、(N-r)个F组成；**无放回**地随机抽取n个元素；Y表示n中S的个数
  - $p(y)=\frac{\binom{r}{y}\binom{N-r}{n-y}}{\binom{N}{n}}$
  - 超几何概率 $p=\frac{\binom{S\_{ALL}}{S\_Positive}\binom{F\_{ALL}}{F\_Positive}}{\binom{ALL}{Positive}}$ , S_Positive表示此单元格之值，S_ALL表示S行之和，ALL表示表格总和，Positive表示此列之和
  - 如果$p<\alpha$，拒绝原假设
  



| -- | Positive | Neg1 | Neg2 | Neg3 | Neg4 |
| -- | -- | -- | -- | -- | -- |
| S | -- | -- | -- | -- | -- |
| F | -- | -- | -- | -- | -- |


### 固定边缘和

设计试验时，**固定**双向表的**行和**或**列和**；e.g. 列和都是100   

其独立性检验与普通的双向表相同


## 参考
Fisher 精确检验：https://zhuanlan.zhihu.com/p/434017609

