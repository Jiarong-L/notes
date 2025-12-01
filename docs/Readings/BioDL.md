<style>
img{
    width: 60%;
}
</style>


关于DL的基础，可以参考 [CS231n 课程笔记](https://cs231n.github.io/) ，[深度学习（花书 Ian Goodfellow）](https://github.com/exacity/deeplearningbook-chinese)，[Easy-RL](https://datawhalechina.github.io/easy-rl/)

也推荐查看偏ML基本概念的教材：西瓜书，统计学习方法（李航），[ESL](https://esl.hohoweiya.xyz/index.html)，[MLAPP/PML](https://github.com/probml/pml-book)，PRML


## 基本操作

1. 序列：获取DNA/RNA/AA序列的表示
    - LSTM/Transformer（序列、Epi、结构） + Knowledge（GCN:PPI/BlastHits、...）随后可用CNN整合
    - 在缺失标签的情况下，可用 self/semi-supervised (AE/DAE/GAN) 获得表示
    - 从预训练的PLM中获取蛋白质序列的表示
        - [ESM-facebook](https://blog.csdn.net/qq_52038588/article/details/134074662)
        - [SaProt-westlake](https://github.com/westlake-repl/SaProt) 需要输入Foldseek的 structure-aware sequence，可以搜索Foldseek的在线数据库，也可以从[ColabFold](https://docs.hpc.sjtu.edu.cn/app/bioinformatics/colabfold.html)预测结构、然后[convert](https://github.com/westlake-repl/SaProt?tab=readme-ov-file#convert-protein-structure-into-structure-aware-sequence) 

| 以蛋白质为例 | 数据 | 评估 | 示例 |
| -- | -- | -- | -- |
| **结构预测** | PDB | CASP 竞赛 | AlphaFold2 |
| GO**功能预测** | UniportKB/GO/... | CAFA 竞赛 | [DeepGO-SE](https://zhuanlan.zhihu.com/p/662030558), DeepEC  |
| **相互作用预测**：预测binding，辅助CRISPR系统设计 | inDelphi/[CRISPRon](https://db.cngb.org/search/project/CNP0001031/)  | 高通量芯片合成及文库筛选 | [DeepCas9](https://zhuanlan.zhihu.com/p/524591517) |



2. Matrix：插补，增强，批次矫正，多组学Anchor：单细胞/转录组/蛋白组
    - [AE对MS蛋白质组数据进行插补](https://www.nature.com/articles/s41467-024-48711-5)
    - [DISC (2020)](https://cloud.tencent.com/developer/article/1785312): 应用于单细胞数据，半监督学习插补缺失值；将AE重构表达谱循环输入AE，最后取所有表达谱的加权平均值作为插补结果
    - [SAUCIE (2019)](https://www.nature.com/articles/s41592-019-0576-7): 应用于单细胞数据，可以用AE中间层的输出进行批次矫正、聚类、细胞类型注释等，以应对稀疏、噪音等问题，[说明](https://cloud.tencent.com/developer/article/1781390)


3. 系统发育树：GNN/Topology：Hyperbolic space 更适合 hierarchical latent structure (Tree Embedding) 所以效果不好（？）
    - [旅行商问题思路](https://www.sciencedirect.com/science/article/pii/S2589004220308476)解决 min state flip，以推断 perfect phylogeny
    - DEPP用于扩充单基因树（？）
    - [PhyloGen](https://engineering.westlake.edu.cn/NewsEvents/LatestNews/202410/t20241017_43042.shtml)：不在拘泥于序列对齐，而是基于序列模型提取的特征。此方法获得的距离score避免传统方法中，序列长度、SV、...带来的额外惩罚




4. 解释模型(XAI) --- 常用工具集 [SHAP](https://shap.readthedocs.io/en/latest/example_notebooks/genomic_examples/DeepExplainer%20Genomics%20Example.html)
    - **输入中的那一部分比较重要？**（GNNExplainer）--- 对输入数据中的某一特征添加扰动 delta_x，评估其对于输出(或者loss)的扰动 delta_y : delta_y/delta_x
    - **对于某一类输出，输入应该是什么样子？**--- 训练Generator对该类别的低维特征输出进行解码（？）
    - **模型参数激活值的变化**（DeepLIFT） --- 根据每一层神经元的“改变”来计算每个输入特征的具体贡献


其它：Multi-Head 是一种常见的模式

## 应用内容

参考：[应用综述 (2022)](https://www.nature.com/articles/s41467-022-29268-7)


### [Synthetic Biology (2024)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10918679/)

* [细胞工程](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10918679/bin/ao3c05913_0003.jpg) 
    - 预测启动子/RBS强度
    - 预测目标基因表达强度
    - sgRNA on/off-target binding --- 相互作用预测

```
 gRNA-Cas9      XXXXX——————————MMM
target DNA 5'———XXXXX——————————PAM——3'

CRISPR靶向特异性：
    1. pairing between gRNA and target DNA
    2. binding between Cas9 and short motif PAM
```


* [代谢工程](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10918679/bin/ao3c05913_0005.jpg)：代谢通路设计/优化/量产
    - [ART](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7519645/) 为希望达成的 response（化合物产量） 提供推荐 input（omics）：由于化合物可能来自多条代谢通路，需要在**不影响整体细胞状况**的情况下最大化其产量
    - [Optimus 5-Prime](https://zhuanlan.zhihu.com/p/685900922): 5′UTR序列(长度/SNV/..)与翻译调控(ribosome footprints 密度)之间的关系


* 训练数据获取
    - 长度有限的序列（5′UTR/promoter）可通过生成随机/半随机 Libraries，进行  massively parallelized assays 


### 表观：TFBS prediction

* [DeepSEA (2015)](https://www.nature.com/articles/nmeth.3547) 根据 non-coding region 中的突变信息预测 TF binding、DNaseI sensitivities、histone marks
* [TFcoop (2019) 非DL](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6359851/) 是 logistic model (LASSO)；利用序列 + cooperating TFs' binding affinity 推断TFBS

注：训练集的TFBS信息从Chip-seq 数据获得，可从 [ENCODE](https://www.encodeproject.org/)下载

传统生信项目一般使用[PWM矩阵（motif.jaspar文件）](https://www.jianshu.com/p/b1abf71c78cf)在基因组中扫描潜在TFBS



### 外显子测序数据的 bias Correct

WES 使用 targeting probes，因此其数据中存在 length/GC/reference biases，故而使用此类数据进行的 CNV 检测精度不佳。但是它便宜。

[DECoNT (2022)](https://genome.cshlp.org/content/32/6/1170.long) 基于 matched WES and WGS data (1000 Genomes Project) 进行训练，纠正 WES-based germline CNV callers 的结果。

1. CNVnator Call CNV，[单个样本的CNV统计结果按照位置区间排列](https://blog.csdn.net/yangl7/article/details/114656482)
2. BiLSTM读取、生成各个位置区间的CNV信息（WES），输出尽可能接近WGS数据结果

[ECOLE (2024)](https://www.nature.com/articles/s41467-023-44116-y) 主要改用 Transformer 架构优化了一下、加入了人类专家标记数据，可以达到 68.7% precision and 49.6% recall，并可推广至其他测序平台数据

## 其它话题

* [LOGO (2022)](https://cloud.tencent.com/developer/article/2202917): 语言模型，可被迁移用于序列标记任务（启动子识别、增强子-启动子相互作用预测、染色质状态预测）和非编码变异优先排序任务




## 进一步优化

参考：[西湖大学 NeurIPS (2024) 发布](https://engineering.westlake.edu.cn/NewsEvents/LatestNews/202410/t20241017_43042.shtml)


* 对LCMS的注释受限于数据集设定，但 De Novo Peptide Sequencing 接通过质谱标注来重建肽序列
    - NovoBench 提供各种 De Novo 方法的基准测试：DeepNovo（提取特征后LSTM生成序列），PointNovo（生成小分子）, Casanovo（Transformer）, InstaNovo（Transformer+扩散式迭代优化）, AdaNovo, [π-HelixNovo](https://git.openi.org.cn/OpenI/pi-HelixNovo-NPU)
    - AdaNovo：自适应生成模型，根据反馈调整分子结构：匹配程度，即质谱与氨基酸或肽之间的条件互信息（CMI）


* FlexMol 药物发现工具集：药物/蛋白结构/蛋白序列的Encoder，相互作用层。可用于快速搭建模型架构
    - 药物-靶标相互作用（DTIs）：新药开发和副作用预测
    - 蛋白质-蛋白质相互作用（PPIs）：发现潜在的治疗靶点
    - 药物-药物相互作用（DDIs）：分析多种药物同时使用时的影响

* UniIF 分子序列设计工具集：分子逆折叠模型（结构->序列）
    - 蛋白质设计、RNA设计、小分子材料设计

* 如何更好的将（序列、结构、功能）信息集成在单个蛋白质表示中？
    - ProtGO：使用集成的教师网络（序列、结构、功能）训练学生网络
    - CoupleNet：基于（残差理化性质-node、结构距离-edge）构建动态图，卷积生成蛋白质表达



