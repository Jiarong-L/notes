

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

大模型只是训练数据的cache？



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

* [氯胺酮](https://www.x-mol.com/paper/1704030464102912000/t?adv)
    - [Ketamine and esketamine](https://www.nature.com/articles/s41591-024-03063-x)


## [母-婴 微生物](https://www.oaepublish.com/articles/mrr.2024.51)

原文简单提到 MGEs 类型对应的传递方式，值得一读

婴儿初期肠道微生物接收母亲肠道的微生物，并经历 'colonization bottleneck' 这一 selective event；初期，暴露在空气的环境有利于有利于兼性厌氧菌、母乳也会选择相关代谢菌种，MGEs 可能会搭乘任何成功通过瓶颈的细菌

此过程中，可移动元件(MGEs:质粒和噬菌体)或许影响婴儿肠道微生物群的定植。水平传播的 MGEs 对宿主的影响可能是负面的（也许感染力强的噬菌体即使牺牲宿主的成活率也可以成功存续），而垂直传递的 MGEs 需要与宿主互利共生（增加某方面的适应性以代偿其产生遗传负担）

挑战：在宏基因组数据集中确定 MGE 的宿主是技术上的难题（可移动原件数据库扫描contig？-- 新型P-Ps最近才被实验确认；或者扫描宿主基因组中的病毒序列 -- PlasX/VirSorter/VirFinder/geNomad），可考虑使用长读段的测序技术，或HiC进行空间定位

未来：更加关注涉及代谢、拮抗和 MGE 防御的基因，而计算机模拟/合成菌落/动物模型进行的控制实验可以帮助阐明环境应激因素对 MGE 传播动态的影响以及它们可能给宿主带来的相对适应优势和成本



## [Mathelier Lab](https://mathelierlab.com/publications/) 表观研究相关

* [综述：Regulatory and systems genomics](https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf106/8128179?login=false)

* [包：序列模拟](https://arxiv.org/html/2506.20769v1)：提供需要呈现的 motifs、描述如何生成，模拟生成 DNA 调控序列（e.g.以比较自然的方式生成cis元件？）；也可以对真实序列进行修改

* Snakemake pipeline：检测 FI variants 在相关基因区域的富集，using all region-score combinations and two enrichment detection methods

* 人白色脂肪细胞中，瞬时 SUMO 化的抑制诱导 Stable Epigenetic Beiging Fate [...](https://www.biorxiv.org/content/10.1101/2025.03.07.642034v2.full)


### [(单样本水平 GRN + multiomics Mtx) 进行 JDR 可以更好地识别 survival 相关因素](https://academic.oup.com/bib/article/26/4/bbaf315/8188241)

* 多组学的整合时机
    - Late -- 各自分析，然后基于相关性整合：忽略分子层之间的相互作用
    - Intermediate -- **联合降维(JDR)**重建 latent space（假设所有组学数据共享隐变量/某种特征）：**MOFA / JIVE / MCIA / RGCCA** 但可能bias向高维的组学数据
    - Early -- 将所有组学层连接成一个矩阵再分析：能够捕捉相互作用，但会引入高维度和噪声

* PANDA 使用如下三个先验信息推断群体水平的 GRN
    - 先验信息：TFs间的PPI  --- 假设 cooperate TFs 可能靶向同一个基因
    - 先验信息：gene co-expressed  --- 假设共表达的靶基因可能受相似TFs调控
    - 先验信息：TFs的序列

* lionessR（线性插值以获取**单样本水平GRN**），其假设：群体网络是N个单样本网络的线性组合，移除1个样本后，网络的变化反映了该样本的贡献
    1. 使用N个样本，构建群体网络 e(N) --- 这里指：基因对的关联强度（如相关系数）
    2. 移除1个样本q，构建群体网络 e(-q)
    3. e(q) = N * e(N) - (N-1) * e(-q)
    4. 把q放回，loop


### [how TFs cooperatively bind DNA](https://academic.oup.com/nar/article/52/18/e85/7747208?login=false)

co-binding：多个TF同时或顺序结合到同一调控区域

67% of the TFs shared a co-binding motif with other TFs from the same structural family


* seqArchR 非负矩阵分解 V = WH  得到对应多种信息的矩阵
```bash
输入X --- ATAC-seq 信号矩阵（值：peak中reads计数）
RegionID × SampleID   =>   RegionID × LatentFactorID    LatentFactorID × SampleID

输入S --- 序列特征矩阵（值：Motif匹配计数）
RegionID × MotifID   =>   RegionID × LatentFactorID    LatentFactorID × MotifID

LatentFactor 此处指共开放模式，可以是一组协同开放的调控元件（增强子/启动子/..）

协同NMF模型： min( ||X - WH||² + α||S - WC||² )         

如何使用这些矩阵？ 假如 LatentFactor1 设置为 TF 协同作用（CTCF + RAD21），其对应的 Motif 信息可以从 C 矩阵中获得
```


* 本文：发现高质量TFBS（Anchors）周围的 TF co-binding patterns，即**寻找TFBS的上下游motif**
    1. 提取 Anchors 上/下游各 nbp 序列，分别形成2个矩阵，形状  ```AnchorID × Seq```
    2. 原位将ATCG改成4位独热编码，现在矩阵有 4n 宽
    3. 非负矩阵分解(NMF)  ```LatentFactor(Len=4k) × Seq``` 可拆成 k 个 PMF 矩阵，即 k 个 序列组合 / Motif
    4. 过滤掉信息含量（IC）小于 2 的 Motif
    5. Trim Motif
    6. 对于使用不同k值得到的Motif，基于序列相似性聚类去重

示意 Step3
```bash
H矩阵（pattern matrices）有 4k 行，可以拆成 k 个 PMF 矩阵

而 Motif 可以从 PFM 统计中总结出      
     pos1   pos2   pos3   pos4 ....
A    freq   freq   freq   freq   
T    freq   freq   freq   freq   
C    freq   freq   freq   freq   
G    freq   freq   freq   freq   
```




## [paulsen-group](https://www.mn.uio.no/bils/english/groups/paulsen-group) /  [HiC研究相关](https://www.lifeomics.com/?p=36533)

* Chrom3D：基于Hi-C数据模拟染色体在细胞核中的位置（3D结构），可加入 lamin ChIP-seq data（核包膜距离信息）
    - 核外围：被抑制，更中心：有活性

* Manifold Based Optimization：减少结构冲突
    - 从 3C 数据中重建"consensus"三维基因组是一个具有挑战性的问题，因为数据是跨越数百万个细胞的聚合数据

* [综述/挑战：单细胞 4D nucleomes (3D + 时空信息)](https://link.springer.com/article/10.1186/s13059-016-0923-2)
    - 获得群体 HiC 构象图
    - HiC Map Deconvolution: bulk -> single cell  但理论上可能的总连接数中大约只有 2.5%被恢复，稀疏性可能会妨碍高置信度的 3D 结构重建
    - 二倍体细胞：或许可区分XY，但常染色体...
    - 4D：伪时间 3D 构象轨迹？活细胞中追踪？


## TCR库

CDR3是TCR中变化最大的区域、也是抗原的重要识别区域。一个独特的CDR3序列即代表一个独立的T细胞克隆（Unique Clones），反映库多样性。Expanded Clones 指部分T细胞克隆识别了某种特定抗原而被激活、分裂，因而频率显著高于背景，反映原特异性免疫应答的强度。

目前有许多工具可以输入（CDR3，抗原片段）预测结合，可用于：临床病毒筛选（病毒数据库-人群CDR3），计算结合位点的贡献（CDR3上的每个位点进行突变）



## 肠-脑轴

一个由神经、激素、免疫和代谢信号构成的复杂网络

1. 迷走神经是一条从脑干直通腹部（包括肠道）的颅神经。肠道中的感受器将信息（如炎症、营养状态、菌群代谢产物、饱腹）通过上行传达到大脑；大脑的应激、情绪信号也可以下行影响肠道的运动、分泌和通透性

2. 肠道菌群产生/影响神经递质的生成：菌群可直接生产 γ-氨基丁酸（GABA）、多巴胺（DA），或刺激肠嗜铬细胞分泌血清素（5-HT）
    - 无法直接通过血脑屏障进入大脑，作用于肠道迷走神经（GABA/DA甚至可能不能穿过肠道上皮）
    - 部分前体可以穿过BBB

3. 短链脂肪酸（SCFAs）：丙酸、丁酸、乙酸
    - 可以穿过BBB！但浓度太高可能造成毒性，作为备用能源或炎症抑制
    - 刺激肠道L-cell生成GLP-1、PYY，作用于脑/肠/胰岛、抑制食欲/抑制肠道蠕动/降血糖
    - 作为结肠表皮细胞的能源、让细胞链接得更紧密、抑制 Zonulin (上皮通透性)，避免 **gut leak** 及后续感染

4. 感染造成的小分子炎症因子（如IL-1β）可以通过主动运输进入大脑，全身炎症可导致BBB通透性增加、渗入更多因子，炎症可能影响特定功能的脑区（与脑血管上的受体结合）


## 更年期 menopause

[WHO - 更年期是如何发生的](https://www.who.int/zh/news-room/fact-sheets/detail/menopause)

[卫健委 - 更年期综合征](https://wsjkw.sh.gov.cn/nsbj1/20250815/2d74b5bc6df043ad8b00e34f062e555f.html)：绝经前后出现**雌激素波动或减少**所导致的一系列躯体及精神心理症状

**雌激素(Estrogen,E)如何影响情绪？** 作为类固醇激素，内源性的E可以穿越BBB到达大脑（边缘系统-情绪/压力），作用于细胞内/外的各种受体、促进血清素（快乐感、平静感）/多巴胺（动力、愉悦）/GABA（缓解焦虑）的合成与释放、抑制皮质醇（压力激素、下丘脑->肾上腺）的过度分泌

**调节雌激素？补充植物雌激素** 豆类饮食、[编码特定酶的微生物组](https://onlinelibrary.wiley.com/doi/10.1002/mnfr.202300688)

**Risk？** 过量补充可能增加乳腺癌风险


## 甲基化 - 衰老时钟

衰老的甲基化特征变化不是一个平缓的过程，而是突然进入下一个阶段（所谓非线性：直接分为年轻、中年、老年）

[STageR](https://www.nature.com/articles/s41467-024-47316-2)

```bash
1. 位点的聚类（基于不同的年龄段的甲基化模式）

2. 选取模式最明显的三个簇 C2、C3、C4 --- 确定了在衰老过程中突然发生高甲基化的位点 & 可能也富集了衰老标志物

3. 根据 C2、C3、C4 中位数甲基化水平，预测 年轻、中年、老年 (Elastic Net)

另外，转录组验证这些了二者相关：甲基化位点、这些位点附近的基因的表达
```

## 微生物代谢-宿主生理

一个示例：[小鼠中，宿主-微生物群代谢相互作用随年龄的变化](https://www.nature.com/articles/s41564-025-01959-z)

```bash
DNA 鼠肠道菌群

    组装MAGs后、用PTR来估计样本中MAGs的生长（即复制起始位点和复制终止位点附近的测序覆盖度之比，与相对丰度弱相关）

    建立GEM、各样本中，计算六种生态关系在每种微生物群落中的频率（EcoGS&比较单菌生长速率）  交互类型与年龄、建立线性模型


RNA  鼠器官（结肠、肝脏和大脑）

    每个宿主转录本（GO注释）、与每个微生物反应（MetaCyc），成对进行Spearman相关性分析；查看强烈正/负相关在GO条目中的富集情况（超几何富集检验）
    （以上过程  stratified by organ and age group --- 可以统计 ‘强烈正/负相关’ 在 age groups 之间是否有显著差异）

    三个器官中，各有一部分转录本同时 microbiomeR-associated and aging-associated
    !!!!!!存在 宿主转录水平、菌群功能 之间的全局关联


每只小鼠的各个器官都有特定的 context-specific metabolic models，向 fastcore 输入以下二者：
    -- StanDep基于转录本丰度/反应丰度，识别高置信度的 context-specific 反应 (core)
    -- 通用 metamodel (host + microbiome) 包含两个 Compartment
        Host organ metabolic model (Recon 2.2)
        Microbiome GEMs 

遍历宿主和微生物群之间交换的代谢物，（由各个小鼠的模拟结果综合决定、可以比对下三个器官间的不同
    - 阻断微生物群吸收某个（宿主分泌的）化合物的通路，进行FVA、若其通量范围减少至小于10%、认为这个交换反应是微生物群所依赖的 ‘dependency’
      反之，得到宿主所依赖的（微生物群生成的）化合物


再细化一下，为确定 单个反应-对-单个反应 的相互作用、即两个反应是否经常出现在同一个通量中（注意，这里是 metamodel，宿主、微生物群 视为一体） 
    - 以某个反应为‘提示’，在通量空间中进行随机采样（EFMSampler ElementaryFluxModes）、计算‘提示’在这些通量样本中的出现概率

        Host_R1  ...  Microb_R1 
Host_R1              (co_exist_freq_Mtx)
Host_R2              包含Host_R2的EFM中，Microb_R1出现的频率

    - 选取上文所述 ‘强烈正/负相关’的（宿主转录本-微生物反应）在这个矩阵中的得分状况
      生成100个随机配对的（宿主转录本-微生物反应）在这个矩阵中的得分状况
      Wilcoxon rank-sum test 可以证明 强烈/随机对的得分状况是否显著不同 --- 肝、结肠中是，脑中不是，宿主代谢-微生物组代谢 可能存在功能耦合？？？

    - 查看其中 单个HostR-单个MicrobR 相互作用在各器官中的富集情况（所有metamodel中，co_exist > 0.5，则认为存在相互作用 !!!!!!

    - 选取某个R的关联反应模块（行内 co_exist > 0.2，不限定来自Host/Microb），查看模块中是否富集了衰老诱导/抑制反应（注释自衰老基因）
      对富集了衰老反应的模块，若其中包含至少20个MicrobR，则认为它依赖于微生物群


以下二者也有 Spearman’s ρ = 0.43
model-predicted microbiome dependence(XX, 微生物群所依赖的宿主代谢物) 与
microbiome-driven variance of (XX) in an independent human metabolomics cohort ？？(XX)在另一代谢组研究数据中、由微生物活动解释的方差


结局：
随着年龄增长，菌群代谢活性显著降低（代谢物的消耗和生产均显著减少）
衰老调控的基因网络显著富集了菌群依赖基因和菌群依赖的宿主功能
代谢组水平上也观察到与年龄相关的代谢衰退的主要因素，从而确定了微生物群可能通过影响宿主衰老的代谢途径
```

用转录组数据获取 core Reaction (基于酶的表达量、AND/OR rules)：[IBD ](https://www.nature.com/articles/s41467-025-60233-2) - 'Reconstruction of context-specific models'(上文使用 StanDep)

