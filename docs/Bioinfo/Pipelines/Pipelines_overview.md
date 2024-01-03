---
title: Pipelines overview
---

<style>
img{
    width: 80%;
}
</style>


[]() 


* 在需要准确定量的项目如ATAC、转录组中，可以加入去除PCR重复的步骤。例如scRNA使用的UMI技术，或者通过samtools/picard去除duplicate
* RNA项目可以使用RSeQC进行测序饱和度分析，以确保有效检测
* 定量单位可以有TPM、FPKM... （TBA）
* 简化xxx：缩小测序范围，e.g. WES,RRBS


## Basic
不同数据的基本流程，暂时还没想好分配给哪个主题

| -- | -- | -- |
| -- | -- | -- |
| [Genome](./Basic/Genome.md) | 组装基因组，并且预测基因；准备上传NCBI的格式 | 其它：Haplotype-based组装；结合HiC数据的组装 |
| Transcriptomics | 转录组 | Bulk：[RNA-seq](./Basic/RNA.md)<br>Single Cell：[scRNA-seq](./Basic/scRNA.md)<br>Spatial：[Spatial_RNA](./Basic/Spatial_RNA.md) |
| Proteomics | -- | -- |
| [Metabolomics](./Basic/Metabolomics.md) | 代谢组 | -- |
| [HiC](./Basic/HiC.md) | 细胞内3D空间距离信息 | 可能Epi也常用？ |
| Re-seq | 获取SNP、InDel、SV等信息 | 群体遗传-重测序 |




## Metagenomics
[![Meta](./Pipelines_overview/img/Meta.png)]()

关注环境中物种组成，或者功能基因的比例；病毒由于含量少，另有工具（TBA）


## Epi

常见的[表观遗传修饰](https://zhuanlan.zhihu.com/p/616493908)包括：DNA甲基化、组蛋白修饰（影响染色质的暴露）、RNA甲基化...

表观修饰可能是影响基因表达的潜在因素，一般与转录起始位点的3D空间距离一起分析；此外，挖掘这些信息可以得到 发育、疾病、衰老的 marker


| DNA水平 | -- | -- |
| -- | -- | -- |
| [ATAC-seq](./Epi/ATAC-seq.md) | 所有开放染色质 | -- |
| [Chip-seq](./Epi/Chip-seq.md) | 常用于寻找某一个TF结合位点/Histone修饰位点 | 免疫共沉淀：寻找某一种修饰的位点信息 <br> e.g.MeDIP-seq：6mA特异性抗体富集含6mA的DNA片段 |
| [BS-seq](./Epi/BS-seq.md)  | 甲基化位点信息 | -- |



RNA水平：免疫共沉淀（MeDIP-seq for m6A）；也可以 RNA-BS-seq（原理同）



