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

教材：《Numerical Ecology》        ![](./Ecology/)

R示例: [David Zelený: Analysis of community ecology data in R](https://davidzeleny.net/anadat-r/doku.php/en:start)

参考: [Linear_Algebra笔记-常见矩阵分解](../Course/Linear_Algebra.md#_12)


| Condition -> Observation | 根据数据的不同特征，选择不同Model |
| -- | -- |
| Deterministic | 确定性的观测结果 |
| **Random**（本书） | 个体结果无法预测，其可计算其出现的probabilities |
| Strategic | 结果同时受个体策略与所处环境的影响 |
| Chaotic | 短期可预测，但长期无法预测；e.g.蝴蝶效应 |
| Uncertain | 完全无法预测 |



## 概览

生态系统是动态的，持续发生着各种process，一个相对稳定的系统一般是分层的（由于能量/地理隔离/生态位/...）；并且一直保持 spatial heterogeneity（个体需要聚集以繁殖/自卫/采食/..）


因此在生态学数据中，考虑到[周边环境、周边族群的影响](./Ecology/f1_5.png)，各采样(y) 很有可能并不是相互独立的：对于正相关的数据(r>0)，直接使用可能会造成 Type I error 上升 (i.e.置信区间比实际窄、过多显著结果)，因此可以：

1. 去除强关联的样本（不推荐）
2. detrending（通过回归去除空间趋势造成的关联）
3. Corrected tests (基于修正后的variable estimates 或 df 进行分析) ； ...


## 一般统计

生态学描述类型常见：
```
intensive/extensive（抽样unit增大，其值不变/等比例增，例如：水温/个数）
additive/non-additive（统计时数值可否相加后取均值，例如：密度/PH） 
```
![](./Ecology/t1_2.png)



| [**统计方法概览**](./Ecology/t5_1.png) | Quantitative | Semiquantitative | Qualitative |
| -- | -- | -- | -- |
| [**假设检验 H0:无差异**](./Ecology/t5_2.png) | 参数检验（假定数据符合某种背景分布） | rank statistics | -- |
| Correlation(2 var) | [Pearson r](./Ecology/Pearson_r.png) | [Spearman r](./Ecology/Spearman_r.png) (without tie), [Kendall Tau](./Ecology/Kendall_Tau.png) | [Fisher 精确检验](Basis_Categorical.md#_6)，[Entropy](./Ecology/Entropy.png)，[二维列联表的 $\chi^2$ ](./Ecology/Contingency.png) 与 [Contingency Coefficient](./Ecology/Contingency_coeff.png)） |
| Concordance(m var) | -- |  [Kendall W](./Ecology/Kendall_W.png) | [多维列联表的 Log-linear model](./Ecology/Contingency.png) |



### Quantitative 数据预处理

一些操作可以令数据转换为正态分布/方差齐次，包括：
```
Linear transformation          y'= ay+b
non-Linear transformation      y'= a^y     y'= log(y)    y'= sqrt(y)
Ranging (将y'限制在某个区间内)：    
        y'= y/max(y)  in [0,1]       
        y'= [y-min(y)]/[max(y)-min(y)] in [0,1]   
        z = [y - mean(y)]/SD(y)         Standardization
-----------------------常见---------------------------------
Box-Cox method
Taylor’s power law
omnibus normalizing procedure     p51
------------------------------------------------------------
pi theory：不同量纲的数据可以用基本量重新表达为无量纲形式
```

可以通过直方图或参数大致估计数据分布的形态：
```
Skewness for asymmetry                   公式 p188
Kurtosis for flatness/peakedness
```


满足统计检验的假设（正态性检验/方差齐次性检验/...）后可以计算置信度或进行假设检验，需要注意多重比较的矫正；此外，也可通过permutation得到某统计量的随机分布
```
用例：n个样本var1-var2之间的相关性r是否显著区别于随机？
 - 可通过permutation获取随机分布，也可以假设它遵循F分布
```

| 常见统计量 | 本书中符号 | Matrix一般大写表示 |
| -- | -- | -- |
| 样本$i$ 特征$j$ | $y_{ij}$ | 原始matrix中，一行是一个样本，一列是一特征 |
| Mean $\mu$ | $\overline{y_j}$ | -- |
| Normalized $y_{ij}$ | $z_{ij} = y_{ij}-\overline{y_j}$ | -- |
| Variance | $s_j^2=s_{jj}$ | -- |
| Standard Deviation | $s_j=\sqrt{s_j^2}$ | -- |
| Covariance $\sigma$, $cov$ | $s_{jk}=\frac{1}{n-1}\sum\limits_{i=1}^n(y_{ij}-\overline{y_j})(y_{ik}-\overline{y_k})$  |  [Covariance Matrix](./Ecology/covariance.png) |
| Coefficient of Variation | $CV_j=s_j/\overline{y_j}$ | 消除均值大小不同/单位的影响 |


**如果数据中有缺失值，可以在算法中进行设定，或填充预测值**

## Biodiversity

* **Alpha** diversity is the diversity in species composition at individual sites i
* **Gamma** diversity is the diversity of the whole region of interest in a study
* **Beta** diversity is the variation in species composition among sites in the geographic area of interest


| Alpha | -- | -- |
| -- | -- | -- |
| **Diversity** 常用 [Renyi entropy](./Ecology/Renyi_entropy.png) 的三个度量 | Number of species ($N_0$) | $q$ |
| -- | Shannon’s entropy ($H_1$) | $ H= -\sum p_i\log(p_i)$ |
| xx | Simpson’s concentration index ($N_2^{-1}$): 随机选的2样本属于同一species的几率 | $\lambda=\sum\frac{n_i(n_i-1)}{n(n-1)}$ |
| -- | Simpson’s Diversity index | $1-\lambda$ |
| **Evenness** | Pielou’s evenness 对比假想完全平均群体的Shannon’s entropy | $J=H_{real}/H_{even}$ |
| -- | Hurlbert’s evenness 假想 min Diversity (一个site只包含一个物种，若sites有多余则用同一种物种填充) 和 max Diversity | $J = (D-D_{min})/(D_{max}-D_{min})$ |
| xx | Patten’s redundancy | $1-J_{Hurlbert}$ |
| -- | 用 Broken stick model 将n个体随机切割给q物种，得到均匀的模拟数据 | $J=H_{real}/H_{model}$ |
| -- | [Functional evenness](./Ecology/Functional_evenness.png) | -- |


但目前，Alpha分析常用 Shannon，Ace，Simpson，Pielou_J 等 Mothur 提供的计算；Beta分析一般是计算Bray-Curtis，Weighted Unifrac，Weighted Unifrac距离后进行聚类分析或差异检验


## Modes

![](./Ecology/f7_1.png)

* 关键词：Similarity(Q), Distance(Q), Dependence(R) coefficients
  - R mode: 寻找 descriptors 间的关系，例如 Pearson's r
  - Q mode: 寻找 objects/samples 间的关系

* 物种会更倾向于分布在某种Niche中：have unimodal distributions along environmental variables；故物种分布相似说明两个site相似
* Double zero problem: 假如有2个site，Species_A 在二者中都是0；则此数据不能提供关于这两个site的生态学信息
  - Skip Double zeros when computing coefficients（Asymmetrical）
  - Not Skip（Symmetrical）

（p273-p350 & [Ch8_Clustering](./Ecology/Clustering.png) 略 TBA），其中常用的是 UPGMA (p354，根据进化树距离)

* A-space: The descriptor, or attribute space


## Ordination


<details>
<summary> 概览 </summary>


| Matrix Type | -- |
| -- | -- |
| Raw | L = sample $\times$ species |
| Raw | R = sample $\times$ environmental variables |
| Raw | Q = species $\times$ traits |
| Distance | D = sample $\times$ sample |


| -- | Raw | Raw | Transformation-based | Distance-based |
| -- | -- | -- | -- | -- |
| [Assumption](./Ecology/Ordination_Assumption.png) | **Linear** | **Unimodal** | -- | -- |
| **Unconstrained** <br> L or D only | PCA | CA, DCA | tb-PCA | PCoA, NMDS |
| **Constrained** <br> plus R/Q | RDA | CCA | **tb**-RDA | **db**-RDA |
| -- | -- | 通过 DCA 第一轴轴长，选择 Unimodal（> 4 SD）或 Linear（< 3 SD）方法 | 一般用 Hellinger 处理后的数据作为输入 | 常见 Jaccard, Bray-Curtis, Unifrac 距离 |


</details>



| [Unconstrained Ordination](./Ecology/UnC_Ordination.png) | 解说 |
| -- | -- |
| [PCA](https://nbviewer.org/github/Jiarong-L/notes/blob/main/docs/Statistics/Ecology/NumEco_PCA.ipynb) | 一般直接用于丰度矩阵，但也可以用于correlation matrix；保留输入中的欧式距离信息，注意 [U 的 Scaling](./Ecology/PCA.png) |
| [Correspondence analysis (CA/DCA)](https://nbviewer.org/github/Jiarong-L/notes/blob/main/docs/Statistics/Ecology/NumEco_CA.ipynb) | 对频率矩阵进行SVD，对稀有物种敏感；CA-axis中的欧式距离对应输入中的$\chi^2$距离 |
| [MDS/PCoA](https://nbviewer.org/github/Jiarong-L/notes/blob/main/docs/Statistics/Ecology/NumEco_PCoA.ipynb) | 对距离矩阵进行特征值分解，Scaling同PCA |
| [nMDS](https://nbviewer.org/github/Jiarong-L/notes/blob/main/docs/Statistics/Ecology/NumEco_nMDS.ipynb) | nMDS空间中保留了距离的秩次信息；stress < 0.2 较为合适 |










