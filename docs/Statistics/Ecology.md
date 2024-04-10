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


| Condition -> Observation | 根据数据的不同特征，选择不同Model |
| -- | -- |
| Deterministic | 确定性的观测结果 |
| **Random**（本书） | 个体结果无法预测，其可计算其出现的probabilities |
| Strategic | 结果同时受个体策略与所处环境的影响 |
| Chaotic | 短期可预测，但长期无法预测；e.g.蝴蝶效应 |
| Uncertain | 完全无法预测 |



## 概览

生态系统是动态的，持续发生着各种process，一个相对稳定的系统一般是分层的（由于能量/地理隔离/生态位/...）；并且一直保持 spatial heterogeneity（个体需要聚集以繁殖/自卫/采食/..）


因此在生态学数据中，考虑到相似环境、周边族群的影响，各采样(y) 很有可能并不是相互独立的：对于正相关的数据(r>0)，直接使用可能会造成 Type I error 上升 (i.e.置信区间比实际窄、过多显著结果)，因此可以：

1. 去除强关联的样本（不推荐）
2. detrending（通过回归去除空间趋势造成的关联）
3. Corrected tests (基于修正后的variable estimates 或 df 进行分析) ； ...

![](./Ecology/f1_5.png)




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



