
1. LC-MS: HPLC --> MS (一级质谱 MS1) --> MS/MS (二级质谱 MS2) （（[质谱原理](https://www.bilibili.com/video/BV1Vp4y1v7NY/)）

2. MS的原始数据经过 [Proteome Discoverer](https://www.jianshu.com/p/f903f66b5317) 处理后即可获取蛋白组数据。
    - PD内置了SEQUEST搜库方法
    - 鉴于存在误差，建议缩小数据库，乃至于只使用本物种的蛋白
    - 设定UniProt的序列为database的话，就可以获取Accession

3. 对比对照组，选取 DAPs (differentially accumulated proteins) and DEGs (differentially expressed genes)
    - Fold_Change ≥ 2 or Fold_Change ≤ 0.05
    - p < 0.05

4. GO and KEGG Enrichment Analysis ...

[系列讲座(2016)](https://www.bilibili.com/video/BV15741187GW/)

## 定性：全谱鉴定/Label-Free

```
将蛋白组混合物         裂解 --> HPLC初步分离以降低复杂度 --> 获取质谱  \
                                                                    | 对比注释 e.g. match到了数据库蛋白中
将数据库中蛋白质   In silico Digestion & Fragmentation --> 模拟质谱  /      IDALNHGVK、ELCPTPEGK片段的谱峰
```

[Expasy](https://web.expasy.org/peptide_mass/peptide-mass-doc.html)

## 定量：iTRAQ

```
以4plex为例：

SampleA--R114--B31 |             (Loop for proteinA/B/C/D/..) | R114 abd                       
SampleB--R115--B30 |========>MS1======>MS2(e.g.For proteinX)  | R115 abd                  
SampleC--R116--B29 |  proteinA/B/C/D/..                       | R116 abd                       
SampleD--R117--B28 |                                          | R117 abd                       

1. 为每个样本加上同重基团：Total mass of Reporter--Balance is 145
2. 获取混合样本的质谱，知悉其中蛋白种类X
3. 仪器选取信号强的峰，进行MS2（再次断裂），获取这个蛋白中各 ReporterX 的信号强度
```


