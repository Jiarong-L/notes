

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

## bulk RNA-seq deconvolution using scRNA
https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-03016-6



## 多模态机器学习
* https://zhuanlan.zhihu.com/p/53511144
* 狗的图片特征向量 - 狗的文本特征向量 + 猫的文本特征向量 = 猫的图片特征向量



## 肺部类器官提供机器学习数据
* https://www.nature.com/articles/s41598-024-73725-w

1. 获取**类细胞图像的表示**（DNN似乎比AotoEncoder更能区分肿瘤间的异质性，AE太详细），类器官培养自不同患者的捐赠
2. 以图像表示为输入，预测各细胞的基因表达（回归模型）
3. 选取与图像表示最‘correlated’的基因：10次训练‘图像表示->基因表达’，选取预测结果更准确、更稳定（SD小）的基因

这样选取的基因、模型或许可以用来区分肿瘤来源？为了**验证**‘仅使用选择基因’所获取的表示中是否保留了异质性的信息，作者提供类器官对药物的反应曲线AUC（是否抑制肿瘤生长），估算了不同类器官系间‘图像所选基因表达-药物反应’之间的相关性（大于随机，形态相关基因也影响药反？），发现单一药物相关性的SD大于组合药物（意味着患者对单个药物的反应存在异质）--所以也可以依据以上SD、辅助选取基因？目标是保留representation中的异质性信息


类细胞图像表示 ==> 筛选Marker基因 ==> 药反相关性验证异质性 ==> 获取保留了**肿瘤类别间异质性**信息的representation，至少是形态/药反方面的



## 单细胞组学 & 大模型 (Large Cellular Model)
* [Single-Cell Omics 中的 Perturbation (模拟微扰)](https://zhuanlan.zhihu.com/p/510952792)可以是各种形式的操作：加入外部分子/基因knockdown/基因表达变化...
* [Current opinions on large cellular models](https://www.jiqizhixin.com/articles/2024-07-25-7)!!!
* [GeneCompass](https://www.nature.com/articles/s41422-024-01034-y)基于**人类/小鼠**单细胞数据进行预训练，整合先验知识（启动子序列、基因家族、基因调控网络、共表达关系），可用于：**跨物种**细胞类型注释（**同源比对映射基因**）、基因调控网络预测、药物剂量反应预测、高维Embedding空间中进行基因扰动以寻找影响细胞命运的关键调节因子
* [Geneformer](https://zhuanlan.zhihu.com/p/634446380)基于单细胞数据进行预训练（Cell->Embed），所学习的表征包含了基因上下文信息，可用于
    - 基因剂量敏感性预测：预测基因B是否会对基因A的CNV（剂量）敏感
    - 染色质动力学：TF结合对下游基因的影响范围
    - 基因网络：基于attention，基因A关注哪些基因？或输入中缺失哪个基因，对细胞的表示向量影响最大？（cosine similarity）
    - 模拟微扰：训练模型以区分A/B/C，缺失某基因后，预测结果会转移向Class A？


依旧是，预训练获得单细胞的表示向量（输入单细胞中各基因的表示向量），然后进行各种预测过程

关键词：迁移学习，上下文

Q：为什么要微扰而不是通过反向梯度确定重要因子？


## Cell Type 定义
* [What is a cell type, really?](https://www.nature.com/articles/d41586-024-03073-2)

基于研究需求的分类，没有定论？可以是按照部位/功能/state/...区分，e.g.按照肺部/肠道分类细胞，但它们之间有相似性（含有同一款药物的靶点），肺部药物公司发现了这一状况，可对此设计针对性的测试

个人猜测：RNA/基因表达决定的是细胞的现状，其余调控方面蕴含了细胞的潜力/命运？



## AI是否拥有常识
* [Can AI have common sense?](https://www.nature.com/articles/d41586-024-03262-z)
    - 人类擅长模糊的、并非最优的决策，这不是 rule-based 模型的长项？
    - 一些微妙的上下文语境：A在节食/但他有放松日，人类会因为‘放松日’而犹豫是否应该准备蛋糕（两种情形间犹豫），AI可能只是简单的下调‘准备蛋糕的probability’
    - 如何衡量常识？知识/常识：水会变冷；推理：热力学

AI也许会在达成目标的途径中做出一些违反常识的决策





## ADHD 

ADHD是由多种生物学因素、心理因素及社会因素单独或协同作用造成的一种综合征。表现为注意力缺失、易冲动（不能抑制冲动），儿童时期的多动似乎在成年期会改善

* [一个图片识别测试示例：不同种类任务耗费的时间](https://pmc.ncbi.nlm.nih.gov/articles/PMC6987009/)
    - Information processing demands: 不同难度的推断Task，无需记忆，即 recognition
    - Working Memory: counting，难度=广度，即 span

* [药物治疗](https://zhuanlan.zhihu.com/p/230979308)：增加前额叶皮层（PFC）中 DA NE 水平 --- DA药物容易上瘾！
    - [心理行为治疗](https://psych.dxy.cn/article/495042)
    - [应对 Working Memory 受损这个问题](https://www.psychologytoday.com/us/blog/on-your-way-with-adhd/202402/understanding-adhd-working-memory-challenges)


* [ADHD 共病抑郁障碍](https://pediatr.dxy.cn/article/518873) comorbidity 可能来自挫折，不过生理机制都是神经递质的不平衡


* 数据集/Atlas
    - [ADHD-200](http://preprocessed-connectomes-project.org/adhd200/index.html): MRI 数据，[fMRI处理流程示例（AthenaPipeline）](https://www.sciencedirect.com/science/article/abs/pii/S0925492723000999)
    - [Neurosynth](http://neurosynth.org/) fMRI 数据库，在线进行 meta-analysis
    - [BrainSpan](https://www.brainspan.org/) 健康人，Developmental Atlas 
    - [Brain Map](https://portal.brain-map.org/) 健康人


* [Nature Portfolio / 论文速览](https://www.nature.com/subjects/adhd)
    -  GWAS/meta-analyses 发现 aggressive behavior 相关基因，用 BrainSpan Atlas 展示这些基因的定位：特定的大脑区域（额叶，前额叶，初级感觉皮层，杏仁核）、细胞类型和发育时间点 [link](https://www.nature.com/articles/s41380-020-00903-3)
    - **iPSYCH cohort** 寻找多基因评分特征(PGS)、预测认知表现: ADHD中 自闭症 v.s. 非自闭症 [link](https://pmc.ncbi.nlm.nih.gov/articles/PMC11439085/)
    - ADHD风险之一：Epigenetic age acceleration (EAA)，即实际年龄与（妊娠）表观遗传预测年龄之间的差异 [link](https://www.nature.com/articles/s41380-024-02544-2)
    - 其它：
        * AutoMorph管道提取视网膜特征：为什么眼部血管密度可以用来预测ADHD？视网膜多巴胺受体 [link](https://www.nature.com/articles/s41746-025-01547-9) 
        * Med23是转录中介体(Mediator complex)的一个亚基，与包括小头畸形、癫痫和智力残疾在内的几种脑部疾病有关，敲除它的小鼠表现ADHD症状、且可用ADHD药物治疗改善 [link](https://www.nature.com/articles/s41386-025-02088-1)
        * 无创脑刺激（NIBS）治疗ADHD的新靶点（刺激部位）：Neurosynth fMRI 荟萃分析（overlapped ROI） [link](https://www.nature.com/articles/s41398-025-03303-9)
        * 当发生被动控制（检测到干扰时抑制自动反应）/主动控制（基于先验信息实施准备策略）时出现的信号即 stop-signal，用 fMRI 检测发现：相比正常儿童，ADHD儿童信号出现的空间飘忽不定（variance大），提示相关回路被破坏 [link](https://www.nature.com/articles/s41467-025-57685-x)
        * cohort 评估孕妇饮食与神经发育障碍关联时候发现饮食模式与ADHD和自闭症显著相关，西方饮食模式代谢物评分（适用多个时间点）、 15种孕期代谢物可以用于改善ADHD的预测 （此文数据不公开）[link](https://www.nature.com/articles/s42255-025-01230-z#)


[功能连通性MRI](https://blog.csdn.net/cc1609130201/article/details/120502328)：RS-FC 即当被试躺在扫描仪中休息而不执行任何特定任务时，测量大脑区域之间的rs-fMRI信号的同步
        
        

## Treatment-resistant depression (TRD)

* [抑郁症](https://www.msdmanuals.cn/home/mental-health-disorders/mood-disorders/depression)药物似乎是提高 5-HT / NE  / DA 水平，不过会受代谢影响


* [难治性抑郁症是抑郁症导致疾病负担沉重的重要原因之一](https://rs.yiigle.com/CN2021/1342734.htm)
    - 指抑郁症患者在接受足量足疗程（至少>6周）的两种不同作用机制的抗抑郁治疗后，仍未达到临床缓解（remission）标准
    - 

* [氯胺酮](https://www.x-mol.com/paper/1704030464102912000/t?adv)
    - [Ketamine and esketamine](https://www.nature.com/articles/s41591-024-03063-x)












