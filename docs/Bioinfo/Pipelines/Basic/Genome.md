<style>
img{
    width: 30%;
}
</style>

TBA

## QC

vecscreen去除载体序列


## Survey分析

https://zhuanlan.zhihu.com/p/366933242


## *de novo* 组装

| 软件 | 数据 | 适用场景 | 其它 |
| ----------- | ----------- | ----------- | ----------- | 
| [SPAdes](../../Blocks/SPAdes.md) | 二代 / 二代+三代 | GC分布均匀，测序深度均匀 | 线性/环状基因组 |
| [MaSuRCA](../../Blocks/MaSuRCA.md) | 二代 / 二代+三代 | GC分布不均匀，测序深度分布不均匀 | 消耗资源少，适合放线菌、真核生物 |
| [Unicycler]() | 二代 / 二代+三代 | GC分布均匀，测序深度均匀 | 线性/环状基因组 |
| [GetOrganelle]() | 数据？？ | 高度污染的情况下 | Meta组装找找可能存在的片段，以此为seed |
| [MECAT2]() | 三代 | -- | -- |
| [Canu]() | 三代 | -- | 资源消耗大 |



## 结构注释




## 功能注释








## 其它下游分析

同源物种的共线性分析

多个物种的进化关系分析（OrthoFinder）

Pan-Genome 制作

...






## NCBI Upload

[table2asn](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/#run) 




