



## Background

* [The Biology of Cancer 中文汇总](https://mp.weixin.qq.com/s?__biz=Mzg4NjA5Mzg2Mw==&mid=2247488659&idx=1&sn=a50c16e1a5bf8ceada311ce2aada047f&chksm=cf9fb5dbf8e83ccd9bf9964fd0d7513fa7e8d2f33456cbe18b1d3e1c4e5b795e47b7c450ba3d&scene=178&cur_album_id=1364329720200085505#rd)，即细胞的无序增殖
    - 原癌基因似乎大都参与细胞内信号通路（细胞生长因子 or TF），e.g.Wnt通路/src/myc/
    - 基因突变、表观遗传修饰、信号通路改变的逐渐积累


* [Cancer & Hallmarks of systemic disease](https://www.bilibili.com/opus/952007216584458248) **值得阅读原文！**
    - 免疫，代谢，衰老，内分泌（性别/昼夜节律/...），微生物，病毒或其它理化刺激
    - 癌症，团在一起-->血栓
    - 临床验证：
        * 基因工程：表达人类基因的小鼠，模拟Gene-Env交互影响
        * 类器官
        * 队列调查
    - 疗法：
        * 人为引导突变，向较少突变表现
        * 异质性--不支持senolytics衰老细胞裂解剂
        * 异质性--多靶点治疗
        * 精准营养，减缓肿瘤生长并使治疗耐药的癌细胞敏感

* 肿瘤发展抗性是指肿瘤细胞在治疗过程中逐渐对治疗手段（如化疗、放疗、靶向治疗和免疫疗法等）产生抵抗的现象，因此这些机制导向治疗药物也不能令人广泛受益
    - **基因突变**导致对某些**靶向药物的抗性**
    - 过表达 **药物外排**蛋白，降低药物在细胞内的浓度
    - **信号通路重编程** -- 药物失去靶点
    - [免疫逃逸](https://zhuanlan.zhihu.com/p/684400279)：肿瘤细胞通过多种机制（如**下调抗原表达**、**分泌免疫抑制因子**等）避免被免疫系统识别和攻击，从而逃避治疗
    - 肿瘤微环境的影响：肿瘤微环境中的成分（如肿瘤相关巨噬细胞、癌细胞外基质等）能够通过分泌生长因子、细胞因子等促进肿瘤细胞的存活及抗药性。
    - 耐药性细胞亚群的存在：在肿瘤中，存在一些细胞本身就具有一定的耐药性，这些细胞在治疗过程中能够存活并繁殖。
    - 干细胞特性获得：某些肿瘤细胞可能获得干细胞特性（如自我更新、分化能力等），这些细胞往往对治疗具有更强的抗性。
    - [代谢重编程](https://zhuanlan.zhihu.com/p/689211973)：肿瘤细胞可能通过改变代谢路径来适应药物压力，进而降低药物的有效性。


感觉就是一场细胞层面的选择进化：突变/少数细胞



## Topics

基本上是单细胞分析的天下，不过WES可用于诊断

* 基因的异常表达，关注其调控模式(GRN/TF)

* [肿瘤干细胞的命运受微环境调节](https://www.sohu.com/a/518732927_121124215)
    - 炎症信号
    - 肿瘤区域内的免疫浸润，e.g. [pan-cancer atlas of myeloid cells](https://www.cell.com/cell/fulltext/S0092-8674(21)00010-6)

* Immune checkpoints 本意防止机体过度免疫，但肿瘤用以逃逸
    - 各种 [Immune checkpoint blockade (ICB)](https://www.cancer.org/cancer/managing-cancer/treatment-types/immunotherapy/immune-checkpoint-inhibitors.html) 疗法的效果因患者和癌症类型而异，[数据库：癌细胞-ICB疗效](https://www.nature.com/articles/s41597-025-04381-6)

* 预后预测，模型一般结合真实世界的数据（生活习惯/年龄/..），可以用[NLP等手段提取非结构化的训练数据](https://blog.csdn.net/m0_59164304/article/details/144443668)

* 工具研究：
    - 准确[计算 Ploidy](../Readings/Interesting_Topics.md#ploidy) 是许多任务的先决条件：量化intratumour异质性、建立肿瘤进化的系统发育、SNV探测、CNA detection


## Glioblastoma (GBM) 胶质母细胞瘤

* GBM [简介](https://my.clevelandclinic.org/health/diseases/17032-glioblastoma)/[2016综述](https://pmc.ncbi.nlm.nih.gov/articles/PMC5123811/)：源于大脑和脊髓中的星形胶质细胞或其它干性细胞，快速侵袭，生长的肿瘤会压迫大脑
    - MRI/CT 扫描肿瘤 + Biopsy 
    - 治疗方式仍然以 手术切除+术后放化疗 为主，尚无治愈方法，五年生存率仅为约 5%
    - 起源于多种干性细胞，从干细胞到神经元再到胶质细胞处于多个分化阶段，其表型变化在很大程度上由信号通路中的分子改变决定，而不是由起源细胞类型的差异决定

* [（2022）GBM侵袭模式](https://www.cell.com/cell/fulltext/S0092-8674(22)00847-9)：类似发育过程中未成熟神经元/神经祖细胞
    - 3D体内成像(颅窗+染料+DeepISTI)
        * 网络特征
            - GBM亚群可通过肿瘤微管链接为功能性、**耐药性的网络**，不连通网络植物的细胞/其余网络，基本保持静止（不是主要的侵袭驱动力）
            - **非网状连接的GBM**似乎接收到来自神经元的信号，步步**侵袭**，定植新的脑区
            - 多个网络最终合并成更大的 heterotypic 网络（IV2PM技术显示，随着定植发生，连接细胞数量逐渐增多 --- 侵袭细胞逐渐转换为定植细胞）
        * 追踪单个GBM细胞的微管(TM)
            - TM运动模式：突起、回缩、分支
            - 更小尺度发现，只有少数丝状伪足可以转换为微管样突起（扫描环境？）
            - TM生长模式遵循 Lévy 运动（小步与大幅步交替），一种捕食者针对稀疏分布目标的优化搜索策略
            - 神经元活动驱动TM形成和生长（钙信号）
    - scRNA
        * 伪时间轴上查看连接/未连接细胞的表达谱，推导侵袭性基因表达特征。该特征富集于肿瘤边缘，且与GO术语中神经元的特征、迁移、侵袭呈正相关
        * 功能细胞状态
            - 未连接细胞富集于神经元、少突胶质细胞前体样、神经前体样、神经发育转录特征（符合浸润区数据集中，肿瘤边缘的神经元状态），无间质细胞
            - 连接细胞主要富集于非神经元细胞状态、星形胶质细胞样（表现出损伤反应转录特征）
        * 间质细胞标记物只分布于连接细胞中，未连接细胞中不含间质细胞，或许它只是伴生、而不是侵袭主力？
        * 未连接细胞 & 瘤周区域的AMPAR基因表达更为丰富（突触后膜特征），可能解释神经元突触输入对TM的动态影响 --- AMPAR抑制性的抗癫痫药物，显著减少了TM长度和分支点
    - 展望：侵袭-定植转换的中介细胞状态、驱动因素，治疗压力（包括放疗和化疗）以及手术切除的影响
    - [（2022）扰乱Ca2+的通讯模式，破坏GBM细胞网络节律](https://zhuanlan.zhihu.com/p/596160993)
        

* [（2022）GBM治疗、复发](https://pmc.ncbi.nlm.nih.gov/articles/PMC10487236/)

* [（2024）GBM微环境、治疗耐药性、复发](https://translational-medicine.biomedcentral.com/articles/10.1186/s12967-024-05301-9)

## Methods

### DSRCT 生信示例

（可以参考本文分析流程，以及可视化展示的方法）

chimeric EWSR1::WT1 protein 是一种异常转录因子(TF)，从 WT1 wild-type 变异而得，可结合GGAA微卫星序列、产生新的增强子、激活邻近基因，是一种罕见的侵袭性肉瘤(STS)亚型 DSRCT 的主要驱动。EWS::FLI1 induces the robust expression of a specific set of **novel spliced and polyadenylated transcripts** within otherwise transcriptionally silent regions of the genome，这些转录本被称为 [neotranscripts](https://www.sciencedirect.com/science/article/pii/S1097276522003823). 


本文（[Single-cell multiomics profiling reveals heterogeneous transcriptional programs and microenvironment in DSRCTs](https://www.sciencedirect.com/science/article/pii/S266637912400274X)）数据
```
scRNA ----- 10*DSRCT  + 1*juxtatumoral_peritoneal（以及对应DSRCT样本的WES）
snMultiome(snRNA/snATAC) ----- 1*DSRCT
bulk RNA ----- 29*DSRCT
```


由于：1. WT1 wild-type 的干扰（3'read 长度不足以覆盖 chimeric 断点）2. 低测序深度转录本的 drop-out，作者设计了针对断点的 PCR primer，**目标性的扩增了 scRNA 的 cDNA 文库中的 EWSR1::WT1 转录本**，称为 targeted scRNA-seq。所得的扩增子中可能还有 WT1 wild-type 污染，因此 targeted scRNA-seq 相关的生物信息分析使用 negative selection method。


* scRNA：聚类后，Harmony 整合不同样本、数据类型；非恶性细胞类型用约定的 canonical markers，DSRCT用其差异高表达的marker。
    - 将 neotranscripts加入参考基因组，随后重新 count 其表达量
    - 对差异 marker 进行GO富集分析
    - [Hotspot](http://www.github.com/yoseflab/Hotspot) 根据基因之间的相关性、寻找 gene modulest
    - 配体-受体（细胞间相互作用）：[CellPhoneDB](https://github.com/Teichlab/cellphonedb)（DSRCT -- microenvironment cell），NicheNet
    - InferCNV
    - 细胞分化状态：CytoTRACE（寻找轨迹分析的起点），StemID（转录组熵反映多能性的水平），CellRank（scVelo）
    - Azimuth: 使用 Cell atlases 进行健康细胞的 label transfer 以及亚群分类
    
* bulk RNA：CIBERSORTx deconvolution，所得的细胞比例与scRNA的不同，可能是由于采样偏差（bulk RNA 样本是冷冻的，而 scRNA 样本处理不同？）
    - Arriba 预测 gene fusions
    - 与其它 STS bulk RNA 数据进行差异基因分析 (DESeq2)
    - 从每个 scRNA 所得的 DSRCT/其它STS亚型 中选取 Top 100 上调基因作为特征，计算这些特征在 bulk RNA 数据中的表达量作为 signatures；ANOVA 检验 signatures 作为特征的显著性
    - survminer 进行生存分析，进一步评估 signatures 的预后价值
 
* scRNA and scATAC: SCENIC+ 预测细胞类型特异的 TFs

* [bulk ATAC-seq Pipeline](https://github.com/nf-core/atacseq)：deepTools 进行免疫沉淀富集，MACS2进行peak calling，HOMER注释gene features；DESeq2寻找差异binding，MEME套件对显著富集的峰进行Motif分析（AME利用JASPAR2020数据库挖掘已知motifs，DREME寻找 de novo motifs）

* [bulk ChIP-seq Pipeline](https://github.com/nf-core/chipseq)：....
    - peak-associated genes 进行 ToppFun GO富集分析
    - ChIP-Enrich 对 ChIP-seq-derived genomic regions 进行 GO富集分析（genomic regions 可以是两个临近基因TSS的midpoint--也是一个gene，富集指标是被peak覆盖的区域比例）
    - DESeq2 寻找 fold enrichment >5 compared to isotype control ChIP 的 peak 作为 signature，并且在 scATAC 中计算这些 signature 的水平
    - MEME套件对显著富集的峰进行Motif分析；同时看看什么k-mer过表达了
    - 与ATAC的peak进行对比，有无重叠

* scRNA and snMultiome: Cell Ranger ARC 进行 ATAC peak calling，随后进行 Seurat + Signac 的标准流程：
    - hg38 EnsDb 进行基因注释
    - 生成 Pseudo-bulk ATAC 数据，Peak Calling (MACS2)，选取其中的高质量Peaks
    - WNN clustering
    - ChromVAR + JASPAR 2020 human transcription factor motifs database 进行 Motif 富集分析
    - 将 scRNA 的标签转移 给 snMultiome 数据（使用 scRNA 的 intronic reads: derive from unprocessed nuclear transcripts）

* visium: anchor 整合 scRNA 数据

* scRNA对应样本的WES数据: CNVkit 对比正常组织与DSRCT样本


### Organoids Screening


微孔板：类器官筛选药物: Promega CellTiter-Glo 3D (ATP发光定量来确定活细胞数量)，[OrBITS(荧光细胞死亡标志物)](https://www.biorxiv.org/content/10.1101/2021.09.09.459656v2.full)，[OrBITS + bulk_RNA 预测药物起效对应的biomarker，scRNA(聚类以选取细分的细胞种类、查看其中marker的表达？) ](https://jeccr.biomedcentral.com/articles/10.1186/s13046-024-03012-z) 



