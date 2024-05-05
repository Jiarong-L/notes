---
title: Pipelines overview
---

<style>
img{
    width: 80%;
}
</style>



* 在需要准确定量的项目如ATAC、转录组中，可以加入去除PCR重复的步骤。例如scRNA使用的UMI技术，或者通过samtools/picard去除duplicate
* RNA项目可以使用RSeQC进行测序饱和度分析，以确保有效检测
* **简化xxx**：缩小测序范围，e.g. WES,RRBS
* 当部分样本直接具有关联性时，就不能简单的考虑 Sample Size。假设有一部分样本(N=2)的Correlation可以计算，则着部分样本的 Effective_Sample_Size = N/[1+corr*(N-1)]

## Bulk

### Basic Pipelines
| Basic Pipelines | 说明 | -- |
| -- | -- | -- |
| [Genome](Bulk/Genome.md) | 组装基因组，并且预测基因；准备上传NCBI的格式 | 其它：Haplotype-based组装；结合HiC数据的组装 |
| Transcriptomics | [RNA-seq](Bulk/RNA.md) | -- |
| Proteomics | -- | -- |
| [Metabolomics](Bulk/Metabolomics.md) | 代谢组 | -- |
| [HiC](Bulk/HiC.md) | 细胞内3D空间距离信息 | 可能Epi也常用？ |
| [Re-seq](Bulk/Re-seq.md) | 对已知基因组序列信息的个体进行测序，获取SNP、InDel、SV等信息 | 群体遗传 |

### Metagenomics
关注环境中物种组成，或者功能基因的比例；病毒由于含量少，另有工具（TBA）

[![Meta](./Pipelines_overview/Meta.png)]()


### Epi & Regulome

常见的[表观遗传修饰](https://zhuanlan.zhihu.com/p/616493908)包括：DNA甲基化、组蛋白修饰（影响染色质的暴露）、RNA甲基化...

表观修饰可能是影响基因表达的潜在因素，一般与转录起始位点的3D空间距离一起分析；此外，挖掘这些信息可以得到 发育、疾病、衰老的 marker


| DNA水平 | 说明 | -- |
| -- | -- | -- |
| [ATAC-seq](Bulk/ATAC-seq.md) | 所有开放染色质 | -- |
| 免疫共沉淀 | 寻找某一种修饰的位点信息 | [Chip-seq](Bulk/Chip-seq.md)：目标蛋白与DNA的互作位点 <br> MeDIP-seq：6mA特异性抗体，富集含6mA的片段 <br> PRO-seq：激活状态下RNA聚合酶的位置 |
| [BS-seq](Bulk/BS-seq.md)  | 甲基化位点信息 | -- |



RNA水平：免疫共沉淀（MeRIP-seq for m6A）；也可以 RNA-BS-seq（原理同）

## Single-Cell & Spatial

| -- | 说明 | -- |
| -- | -- | -- |
| [SingleCellOmics](SingleCellOmics.md) | Reads 带有 Cell Barcode 和 UMI | -- |
| [SpatialOmics](SpatialOmics.md) | Reads 带有空间信息 | -- |











