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
| [SPAdes](../../_Blocks/SPAdes.md) | 二代 / 二代+三代 | GC分布均匀，测序深度均匀 | 小基因组：线性/环状 |
| [MaSuRCA](../../_Blocks/MaSuRCA.md) | 二代 / 二代+三代 | GC分布不均匀，测序深度分布不均匀 | 消耗资源少，适合大基因组：放线菌、真核生物 |
| [Unicycler]() | 二代 / 二代+三代 | GC分布均匀，测序深度均匀 | 小基因组：线性/环状 |
| [GetOrganelle]() | 数据？？ | 高度污染的情况下 | Meta组装找找可能存在的片段，以此为seed |
| [MECAT2]() | 三代 | -- | -- |
| [Canu]() | 三代 | -- | 资源消耗大 |



## 结构注释

动物预测基因： GeneMark, Augustus ,SNAP ,GENEWISE
转录组数据辅助基因预测：minimap2比对reference，再用collapse得到基因结构（pacbio官方推荐）


https://zhuanlan.zhihu.com/p/588761049

https://cloud.tencent.com/developer/article/2351525?areaId=106005


## 功能注释








## 其它下游分析

同源物种的共线性分析

多个物种的进化关系分析（OrthoFinder）

Pan-Genome 制作

...






## NCBI Upload

[table2asn](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/#run) 




