

[CCF期刊](https://www.ccf.org.cn/Academic_Evaluation/Cross_Compre_Emerging/)泛读记录，[CCF Conference Deadlines](https://ccfddl.cn/)


## [Bioinformatics - Advance articles](https://academic.oup.com/bioinformatics/advance-articles)


### [2025.01](https://academic.oup.com/bioinformatics/issue/41/1)

* SCARAP
    - 推断泛基因组（序列相似的氨基酸序列集）？MAFFT+MMseqs2 进行比对聚类 
        - species-level core genome --> orthogroup fixation frequency ?（Orthogroup正交群 -- 由一个物种的LCA中的单个基因进化而来的一组基因）
    - 如何寻找核心基因集？先从少量数据中获取特征（hints 旧方法：从泛基因组中获取子集 -- 耗时 / 预设一组core基因候选 -- 不全）
        1. 随机选取100个seed genomes、推断它们的pan
        2. 识别core候选集：基因家族，存在于90%以上的seed genomes中
        3. 对选取的每个基因家族获取其 alignment profiles（MAFFT+MMseqs2），再度遍历 seed genomes，根据单个profile 与 core / not core 候选集的比对分数决定cutoff阈值（二者均值），用这个cutoff阈值重新筛查这个profile可比对的基因，若存在于95%以上的seed genomes中，则这个profile对应的基因家族是core
        4. 将 core gene profiles / cutoffs 应用于完整数据集中
    - 预设定一组基因（core/pan），可计算基因组间的相似度（ANI），本文提供了从数据库中获取新（不相似）基因组的工具
    - pan-genome 数据：SimPan模拟 (nucleotide identity 90% 区分属), Tonkin-Hill 数据集 (区分亚种), GTDB (区分属), OrthoBench/paraBench


* CrossIsoFun  亮点在于 isoform-isoform interactions IIIs 的 Encoder，比PPIs分辨率更高？
    - multi-omics
        - PPIs (Interactomics)
        - isoform expression profiles from RNA-seq data (Transcriptomics)
        - sequence features from protein sequences and conserved domains (Proteomics)
    - multi-omics --> GO slim 
        1. AE_CycleGAN(multi-omics) --> IIIs
        2. GCN(expression)  GCN(sequence)  GCN(III)  获取各模态的特征
        3. View Correlation Discovery Network (VCDN) 集成、寻找模态间相关性


* 1D convolutional：单细胞表观 multi-omics 整合
    - 如何生成序列？在基因组上按区域/bin统计某个特征的计数
    - 多组学？全连接层-VAE（联合分布 ---> 分解为条件分布的乘积 ---> 联合分布）忽略了基因组顺序，且独立处理每个模态、丢失跨模态的关键信息。本文建议在有序特征空间上进行卷积（具有多个特征/通道的1D序列），即 ConvNet-VAE （本文设置泊松分布为VAE的条件分布）
    - 一些评估：marginal likelihood p_data (从z中再生成数据的能力/贝叶斯模型的基准测试)，Adjusted Rand Index ARI(获得embedding后的聚类性能评估)


* POASTA 兆级长度的多重序列比对
    - 偏序比对（POA）是一种渐进式多序列比对（逐步添加序列）


* 采样时，一般希望 k-mer 数量尽量少，Bryce Kille 证明了一个近紧下界


* PHIStruct: phage–host interaction
    - 从 phage 数据库中提取 Receptor-binding protein (名称匹配+PhageRBPdetect)，用 SaProt Embed 结构信息，预测 [ESKAPEE host genera](https://www.tsu.tw/edu/10693.html)


* EnrichRBP 平台：RNA-RBP binding site/motif/select/visualize ... 支持DL在内的多种工具


* DDGemb：又一个 PLM+Transformer 预测残基变异对蛋白质热力学稳定性的影响
    - 相关的实验ΔΔG值：ProTherm 数据库，PTmul 数据集


* BetaAlign: NLP 将一组未比对的生物序列映射到 MSA  **???**
    - concat `ATG | ACGG | ACG` --> **Transformer 预训练的** --> crossed `AAA TCC -G- GGG` --> `AT-G ACGG AC-G`
    - 训练：已知 “true” MSA 的模拟数据，cross-entropy loss    
        - 值得思考：进化参数对序列比对推断准确性的影响（indel长度、频率）--- 当前评分方案/惩罚参数是否可靠？
    - 最多 1024 个 token，超出只能分段 MSA
    - 对k条序列生成`k!`种MSA，选取最佳


* TPepPro：局部序列特征(TextCNN) + 局部-稍远处结构特征(TAGCN) --> 有/无 PepPI
    - 肽-蛋白质相互作用（PepPIs）的难点在于其瞬时性质、以及肽的高柔性；传统的分子动力学模拟方法需要大量的计算资源
    - 可解释性：Attention，卷积核 activation maps

* CParty算法，已被纳入2D预测工具 HotKnots 2.0（旧版支持 HFold 算法，也可包含假结，但模糊）
    - pseudoknots(hairpin_loop与RNA链的某部分再度稳定缠绕) 是 RNA 2D 结构预测的难点（NP难）
    - density-2 指在序列的任何一点，最多重叠两层碱基对的弧线（Figure 1）
    - RNA 结构的自由能：所有环的能量之和
    








