<style>
img{
    width: 30%;
}
</style>

# Genome *de novo*





## Survey分析



## 组装

| 软件 | 数据 | 适用场景 | 其它 |
| ----------- | ----------- | ----------- | ----------- | 
| [SPAdes](../Blocks/SPAdes.md) | 二代 / 二代+三代 | GC分布均匀，测序深度均匀 | 线性/环状基因组 |
| [MaSuRCA](../Blocks/MaSuRCA.md) | 二代 / 二代+三代 | GC分布不均匀，测序深度分布不均匀 | 消耗资源少，适合放线菌、真核生物 |
| [Unicycler](../Blocks/Unicycler.md) | 二代 / 二代+三代 | GC分布均匀，测序深度均匀 | 线性/环状基因组 |
| [GetOrganelle](../Blocks/GetOrganelle.md) | 数据？？ | 高度污染的情况下 | Meta组装找找可能存在的片段，以此为seed |
| [MECAT2](../Blocks/MECAT2.md) | 三代 | -- | -- |
| [Canu](../Blocks/Canu.md) | 三代 | -- | 资源消耗大 |



vecscreen去除载体序列


## 注释



## 下游分析


