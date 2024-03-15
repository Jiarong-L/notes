

有趣的论文话题，留待借一步学习


## NTAR
* N-terminal alanine-rich (NTAR) sequences drive precise start codon selection resulting in elevated translation of multiple proteins including ERK1/2
* https://doi.org/10.1093/nar/gkad528
* kozak序列，引物设计要素: https://zhuanlan.zhihu.com/p/24415751

N-terminal alanine-rich (NTAR)序列有助于选择正确的start codon，它们可能有助于精确控制关键转录物(如潜在致癌基因)的翻译。许多管家基因含有它，例如ERK


## i-Motifs
* Genome-wide mapping of i-motifs reveals their association with transcription regulation in live human cells
* https://doi.org/10.1093/nar/gkad626
* ChipSeq，CUT&RUN/CUT&Tag，iM-recognizing antibody (iMab)

四链DNA结构i-motifs (iMs, C-rich)与 G-quadruplexes (G4s, G-rich)分别主要存在于转录率低和转录率高的基因上。细胞中的iMs主要存在于活跃转录的基因启动子上，与R-loops重叠。iMs和G4s可于不同区域独立存在，但于同一genomic tract出现可增强它们的形成。  

iM-recognizing antibody (iMab) that selectively targets iMs over G4s and duplex DNA + CUT&RUN 和 CUT&Tag 以在生理的条件下检测核酸折叠



## Gene Context
* Assessing in vivo the impact of gene context on transcription through DNA supercoiling
* https://doi.org/10.1093/nar/gkad688
* E. coli

Gene Context可能以不同的方式影响基因表达，例如：1. 转录通读(下游共向基因与上游基因共转录)；2. RNA polymerases (RNAPs) 转录时，它会对DNA双螺旋施加机械应力，导致基因上游under-wound、下游over-wound，其影响可延申至several kilo-bases，影响相邻基因或随后的转录起始/延长；3. Topoisomerases、nucleoid-associated proteins等可通过调节supercoiling来影响转录。 

本文使用双转录环模型(单个基因两侧各有拓扑屏障 to prevent the diffusion of supercoiling)定量测量基因表达如何随启动子和拓扑屏障距离的变化而变化，弥合了理论和体内特性之间的差距；基因的表达取决于与上游屏障的距离，而不是下游屏障的距离，其程度取决于启动子



## Ploidy 
* [scAbsolute: measuring single-cell ploidy and replication status](https://doi.org/10.1186/s13059-024-03204-y)
* [Tools for CNA detection from scDNA data](https://doi.org/10.1371/journal.pcbi.1008012)
* CIN: https://news.bioon.com/article/5172e3412434.html
* [Dirichlet Process](https://zhuanlan.zhihu.com/p/76991275)


Cancer 中，chromosomal instability (CIN) 可能体现在大量基因发生 copy number aberration (CNA)，有时甚至是 whole genome doubling (WGD)。准确计算 Ploidy 是许多任务的先决条件：量化intratumour异质性、建立肿瘤进化的系统发育、SNV探测、CNA detection。 e.g.[SNP芯片检测CNV的原理](https://cloud.tencent.com/developer/article/1556077)：比较每个位点的两个Allel（A-ref，B-alt）的荧光强度的比值 B_Allel_Frequency = B/A 即 (AA=0/AB=0.5/BB=1)

难点：与bulk方法不同，sc 数据中 cell cycle states 造成 DNA content 与 copy number的变化（因此建议将 S phase 与 G1/G2 phase 分开处理）。现有 CNV 预测工具对部分 sc 数据的处理效果不好（例如：当缺少 odd or intermediate copy number states 时准确度降低）。此外，区区 100-1000个细胞的 SNP 状态不能支持最新 WGD 的预测（CHISEL；因为突变数量不够）

除此之外，实验手段如 fluorescence-activated cell sorting 可以用来计算 Ploidy。

**scAbsolute 原理**：

* 处理一个Cell时，将其基因组切成许多小bins；假设单个 Bin 的 ReadCounts 的分布可视为一组不知数目的 Gaussian distributions
* 使用 Dirichlet Process 求得每个分布的 (var,mean)、限制每个分布 mean 之间的距离为常数（即 per-cell scaling factor **Rho**：因 ReadCounts = copy_number * per-cell_read_depth）
* 会有多个备选Rho值，根据ploidy范围(by default 1.1–8.0)选出最接近的值。

随后，根据上述ploidy计算 genomic read density，将之与经验数据对比，若有异常则重新计算ploidy（常见于G2 phase or WGD cells）


![](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs13059-024-03204-y/MediaObjects/13059_2024_3204_Fig1_HTML.png?as=webp)



## Knowledge-primed neural networks
* [Knowledge-primed neural networks enable biologically interpretable deep learning on single-cell sequencing data](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02100-5)
* e.g. [Modeling transcriptomic age using knowledge-primed artificial neural networks](https://doi.org/10.1038/s41514-021-00068-5)

训练NN的时候加入了一些先验信息（可以是列表、也可以是另一个NN）：设定每个网络节点对应为某种生物等量，比如说一个node代表一个蛋白/pathway，通过训练过程获得其权重，如此才可以从生物角度解释模型结果。

根据皮肤转录组数据预测Age时（用n = 887训练网络），已知50个 ‘Hallmark’ genesets（pathway），定义第一层的nodes是pathway（与input gene 全连接），于是相当于关于每一个pathway训练网络（中间层：a minimal size of 5 neurons per layer for each pathway），最后一层整合每个网络的预测结果（这一步中每个pathway的权重---即评估其对于Age的作用）。此外还可以通过删除某基因的数据，来评估其对于预测Age的贡献。

TCR KPNN：
```
    - 输入 Gene expression data，输出 TCR 是否被刺激
    - 已知关联： target genes --(gene-regulatory interactions DB)-- transcriptionfactors --(signaling pathways DB)-- TCR
    - 根据关联设计模型框架：Input Gene Expr -- transcriptionfactors -- signaling Protein -- TCRs -- Output 0/1
    - 其中，仅有相关联的不同层nodes间才有path（根据DB提供的先验知识确定），这个edge可以由几层小hidden layer组成
```


## 评估基因编辑的效果
* [Precise fine-turning of GhTFL1 by base editing tools defines ideal cotton plant architecture](https://doi.org/10.1186/s13059-024-03189-8)

对比野生型（for 背景突变）和对照组（for 组织培养和转化过程中发生的突变）

On-target mutation detection: 采用特异性引物扩增对应的编辑区域

Detection of off-target mutations: GWAS

```
基因编辑中，sgRNA（向导RNA）识别靶DNA序列中保守的PAM（Protospacer Adjacent Motifs），引导Cas9核酸内切酶定点切割靶向DNA；若其特异性不足/不高效，会造成脱靶

sgRNA library design：Cas-Offinder，BEsgRNADe
```


## 多模态机器学习
* https://zhuanlan.zhihu.com/p/53511144
* 狗的图片特征向量 - 狗的文本特征向量 + 猫的文本特征向量 = 猫的图片特征向量



## ST/ISS/FISH
* https://zhuanlan.zhihu.com/p/491377252

* FISH 是用荧光探针进行原位杂交，高度精确定位RNA在细胞中的位置；MERFISH使用多轮杂交的信号组合（一组二进制vector）为身份标识，最多可以同时支持上万个基因的探测
* ISS  用四种颜色荧光各代表一种核苷酸，根据荧光信号记录序列信息；然后需要将这些荧光reads分配给细胞：可以assign给最近的细胞核，也可以根据 k-hoop neighbor 信息进行embedding
* ST 就是 10x Visum，将样本平铺在一片Spot上；每个Spot可能跨越几个细胞，也可能切割一些细胞，故而如何将spots中reads分配给单个细胞也是一种挑战（也许可以模仿ISS的处理方式？）




