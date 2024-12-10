
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
  src="http://127.0.0.1:8000/Statistics/Basis/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://github.com/Jiarong-L/notes/blob/main/docs/Statistics/Basis/tex-svg.js">
</script>

<style>
img{
    width: 60%;
}
table th:nth-of-type(5) {
    width: 20%;
}
</style>



Meta分析教程[(需登录)](https://training.cochrane.org/handbook/current/chapter-10)/[(R)](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/intro.html)：整合多个studies的结果


注：IPD Meta分析整合各研究的原始数据，普通Meta分析整合各研究的效应量（e.g.均值/比值/...）


## 流程

1. 汇总每项研究的统计量，例如：风险比、均值之差、...
2. **综合统计量**可以是各研究统计量的加权平均，study_i 的贡献权重一般是 1/variance_i
3. 异质性检验(I2/Q)：根据[不同研究中统计量x的齐性检验(I2)/...](https://blog.csdn.net/m0_37228052/article/details/134138794)，选择 Fixed-Effects Model (I2 < 50%) 或 Random-Effects Model (I2 > 50%)
    - （同质/单一群体）Fixed-Effects Model $\hat{y_{i}} = y + \epsilon_{i}$ 假设每一个y_i都来自真值，因此根据y的真值拟合y_i
    - （异质/分布采样）Random-Effects Model $hat{y_{i}} = y_i + \epsilon_{i} = \mu + \zeta_{i} + \epsilon_{i}$ 假设每一个y_i都是从一个总体正态分布中获得的取样，因此以总体分布的均值为真值拟合y_i
    - （上述$\epsilon_{i}$为Sampling Error）
4. 展示综合统计量及其权重、置信区间，e.g.森林图

目的是探讨：不同研究所得的结果差异是否仍可归于随机误差？差异太大的话，表明不同研究之间的干预效果不一致

此外还需要考虑数据丢失的问题, [参考Survival](./Survival.md)


### 确定研究计划

确定研究问题后，为了防止研究手段被数据影响，必须先行确定计划。按照 [PRISMA 原则](https://www.prisma-statement.org/translations)从 PubMed/Reviews 上筛选符合条件的研究/效应量。注意使用 [Risk of Bias Tools](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/risk-of-bias-plots.html) 来评估 Study quality

更基本的PICO原则：

1. 研究的对象包括：年龄、性别、招募来源、etc.
2. 研究的干预措施/自变量是？持续多长？etc.
3. 对照组的设计，安慰剂？随机人群？etc.
4. 研究的效应量是？具有可比性、可计算、可靠、可解释

如果必须排除某效应量的某些研究，必须说明充分的理由：无法获取数据/根据异质性检验去除离群的研究/某研究SE太大/[Publication Bias](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/pub-bias.html)...

### 效应量 & 其SE

效应量及相应的矫正公式参考[此处](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/effects.html)

1. 从各个研究中选取效应量(effect size) & 其标准误(SE)，如果作者公布原始数据，也可自行计算
    - in Observational Designs: Means, Proportions, Correlations
    - in Experimental Designs: standardized mean difference (SMD or Cohen’s d), Risk & Odds Ratios, Hazard Ratios

2. 对效应量进行矫正
    - Small Sample Bias（当某个研究中n<20）：将SMD修正为hedges_g
    - Measurement error（测量手段是否可靠）：对同一个样本$x$多次测量效应量，对此数据计算相关性 reliability coefficient $r_{xx}$。在知道效应量的 reliability coefficient 后，可以用于矫正数据 $SMD_{Corrected} = \frac{SMD}{r_{xx}}$
    - Range restriction $U = \frac{SD_{unrestricted}}{SD_{restricted}}$：变量在研究中的variation小于在目标人群中，即研究(Restricted)不能代表全体人群(Unrestricted)。Unrestricted 数据可以从目标人群的其它代表性研究中选取相应的变量进行计算。得到U后，即可对本研究中的次变量进行矫正。**等一下，这不就相当于直接用其它研究中的变量数据替换了此研究中的数据？？？**

3. unit-of-analysis problem: 我们假设 effect size in a meta-analysis is independent，但以下两种状况违反此假设
    - 分组大于二，例如ABC三组，则若选取效应量$\theta_{A-C}$、$\theta_{B-C}$，C组被包含了2次(double-counting)。解决：将C组拆分为二/不使用$\theta_{B-C}$/整合AB后再引入C
    - a study measured an outcome using two or more instruments，解决：只使用其一/整合所有instrument/[“Multilevel” Meta-Analysis](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/multilevel-ma.html)


### Effect Size Pooling Models

预处理完毕效应量 & 其SE后，根据不同研究中统计量x的异质性检验结果（齐性检验）决定 Pooling Models 为 Fixed/Random-Effects。实际使用时，扔给[meta包-metagen()函数](https://rdrr.io/cran/meta/man/metagen.html)后自动进行输入效应量的异质性检验(Q/I2/H2/tau/...)和 average effect ，[各统计量的参数示例--见目录](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/pooling-es.html#pooling-es-r)：

```R
m.gen <- metagen(TE = TE,             ## effect size -- column name of df 'ThirdWave'
                 seTE = seTE,         ## SE
                 studlab = Author,
                 data = ThirdWave,    ## df
                 sm = "SMD",          ## Type of data
                 fixed = FALSE,       ##  Pooling Model to use
                 random = TRUE,
                 method.tau = "REML",  ## method to estimate the between-study variance / heterogeneity
                 method.random.ci = "HK",
                 title = "xxx")

## e.g. 最简单的 Fixed-Model 的 average effect 其实就是加权均值...
```

[异质性检验](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/heterogeneity.html#het-measure-which)中，Q随着引入研究数量的增加而增加，I2/H2随着研究中样本数的增加而增加，tau则难以解释。建议不要使用单一指标，且结合效应量的预测区间进行判断。


[dmetar包-InfluenceAnalysis()函数](https://dmetar.protectlab.org/reference/influenceanalysis)对上述m.gen对象进行 **influence analysis** 分析，即寻找对综合效应/异质性影响巨大的研究


其它：[metafor包-rma()函数](https://wviechtb.github.io/metafor/reference/rma.uni.html)提供 **Mixed-Effects Models ???**，[其gosh()函数](https://wviechtb.github.io/metafor/reference/gosh.html)/[dmetar包](https://dmetar.protectlab.org/reference/gosh.diagnostics.html)提供各种图像化的异质性分析


其它：之后对上述m.gen对象进行 forest() plot，或者updata()一下其subgroup参数（e.g.RiskofBias=High/Low），或者


其它：[metareg()函数](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/metareg.html)对上述m.gen对象进行回归分析，e.g.对 Publication Date 进行回归





## 参考
```
Fixed/Random模型的区别   https://wviechtb.github.io/metafor/reference/misc-models.html
CMH检验      https://blog.csdn.net/nixiang_888/article/details/117842865
Meta分析     https://www.sciencedirect.com/science/article/pii/S2772594422001169  
Meta示例     https://blog.csdn.net/m0_37228052/article/details/133026057
meta/metafor R包  https://blog.csdn.net/Dunaichuanyi/article/details/130458667
R包-esc   hedges_g(SMD,n)
```
