
[QC 示例: cfDNAPro](https://bioconductor.org/packages/release/bioc/vignettes/cfDNAPro/inst/doc/cfDNAPro.html)


## [背景](https://www.nature.com/articles/s41416-021-01635-z)


cell-free DNA 是细胞 apoptosis, necrosis, or active secretion 后释放到外周血、尿液等体液中的游离DNA，约167nt，半衰期约为 5~150 min。血浆中的cfDNA主要来源于造血系统或病变组织，孕期则有 2-20% 来自胎盘。移植排斥反应、自身免疫性疾病、感染、心肌梗死、中风等皆有可能改变cfDNA谱。

一般可以研究cfDNA中的遗传畸变（SNP/CNV），也可以研究其共价DNA修饰（甲基化）。cfDNA片段化模式在整个基因组中分布不均，DNA甲基化与核小体占用密切相关，而[核糖体的可及性影响cfDNA片段的最终切割偏好](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9849216/)。




**[关联 Table: 不同分辨率下cfDNA应用于IVD](https://www.nature.com/articles/s41416-021-01635-z/tables/1)**，其中常用：

* **WPS** = 完全跨越窗口A的DNA片段数 - 终点在窗口A的DNA片段数。反应了该窗口内的 coverage/peak 信息。测序深度足够时，可以：
    - 基于L-WPS(window=120 bp) **鉴定 nucleosome-occupied regions**，结果与核小体图谱分布相似
    - 基于S-WPS(window=16 bp) **鉴定 transcription factor binding**，如CTCF。
    - 通过对 L-WPS 进行快速傅里叶变换（FFT）推断**核小体间距**，它与造血细胞的 A/B compartments（染色质互作）、开放染色质区域、特异性基因表达相关，也许可用以**回溯 cfDNA 的来源组织**

* Fragmentation/ Patterns: [(碎片化模式+甲基化测序)训练癌症早筛模型](https://www.nature.com/articles/s41467-023-41774-w)
```
Methylated Fragment Ratio (MFR)
Fragment Size Index (FSI)
Chromosomal Aneuploidy of Featured Fragments (CAFF),
Fragment End Motif (FEM)
...
```


## [回溯 cfDNA 的来源细胞类型 (2024)](https://www.nature.com/articles/s41467-024-46435-0)

cfDNA的溯源受困于来源组织之间的遗传差异，例如：胎儿与母体基因组之间，肿瘤突变DNA与健康组织DNA之间。目前，可以基于其甲基化谱进行细胞类型的deconvolution，如 [methylDeConv](https://doi.org/10.1093/bib/bbac449)。也可以基于 cfDNA fragmentation patterns 预测其CpG甲基化，进一步进行来源回溯，如 [FinaleMe](https://www.nature.com/articles/s41467-024-47196-6)。

作者整合了公开的单细胞数据集，获得了450多种潜在细胞类型中20k个基因的表达量。将cfDNA片段Mapping至人类参考基因组后，对每个基因，通过 FFT 将 L-WPS 信号表示成三角函数积分的线性组合（即变成周期图）。选取位于 193-199bp 间的周期，计算该基因的 mean FFT intensity。随后计算该基因 mean FFT intensity 与 Gene Expression 间的相关性。

完成后，根据相关性对基因进行排序。根据不同组织来源拆分单细胞类型、及其 marker genes。对各组织中基因的 rank 进行 boxplot，以评估‘相关性’在不同组织中的分布是否有所区别（细胞类型对血浆 cfDNA 的相对贡献：健康个体中，肝脏对血浆 cfDNA 的相对贡献最高）。


随后作者对癌患者 cfDNA 与上述单细胞 GE 同样计算 rank，如此得到450多种细胞的rank，以此为SVM的输入特征。由于模型比较成功的区分了疾病个体和对照组个体，我们可以说：癌症患者中，cfDNA 来源异于健康组

SVM的基准分析：各组织的 bulk rna 表达量。


**生物信息操作:** [Shendure lab cfDNA](https://github.com/shendurelab/cfDNA)





## 其它参考


```
https://iivd.net/thread-33875-1-1.html      !!!
https://zyxy.wfmc.edu.cn/2022/0329/c7340a102147/page.htm  cfDNA在癌症诊断中的机遇和挑战(2022)
https://www.nature.com/articles/s41390-022-02448-3        儿科疾病中的应用(2023)
https://www.nature.com/articles/s41416-021-01696-0        当前癌症临床试验中(2022)
https://zhuanlan.zhihu.com/p/494472266      cfDNA的提取方法
```



