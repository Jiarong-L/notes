<style>
img{
    width: 60%;
}
</style>




## [Current progress and open challenges for applying deep learning across the biosciences (2022)](https://www.nature.com/articles/s41467-022-29268-7)


### 获取DNA/RNA/AA序列的表示

* LSTM/Transformer（序列、Epi、结构） + Knowledge（GCN:PPI/BlastHits、...）随后可用CNN整合
* 在缺失标签的情况下，可用AE/DAE获得表示
* [ESM](https://blog.csdn.net/qq_52038588/article/details/134074662) 是facebook预训练的蛋白质表示网络



### 解释模型(XAI)

1. 输入中的那一部分比较重要？e.g. GNNExplainer 识别重要子图结构，LIME，[SHAP](https://shap.readthedocs.io/en/latest/example_notebooks/genomic_examples/DeepExplainer%20Genomics%20Example.html)
    - 控制输入数据中的某一特征，评估该特征对于prediction loss 的影响
    - 对输入数据中的某一特征添加扰动 delta_x，评估其对于输出扰动 delta_y 的影响: delta_y/delta_x


2. 对于某一类输出，输入应该是什么样子？
    - 训练Generator对该类别的低维特征输出进行解码？

3. 模型中？
    - 根据反向传播网络中所有神经元对输入的每个特征的贡献，分解神经网络对特定输入的输出预测（DeepLIFT）


### 应用

| OK Tasks | 数据 | 评估 | 示例 |
| -- | -- | -- | -- |
| 蛋白质**结构预测** | PDB | CASP 竞赛 | AlphaFold2 |
| 蛋白质GO**功能预测** | UniportKB/GO/... | CAFA 竞赛 | [DeepGO-SE](https://zhuanlan.zhihu.com/p/662030558), DeepEC  |
| **相互作用预测**：辅助CRISPR系统设计 | inDelphi/[CRISPRon](https://db.cngb.org/search/project/CNP0001031/)  | 高通量芯片合成及文库筛选 | [DeepCas9](https://zhuanlan.zhihu.com/p/524591517) |
| **Data integration** | -- | -- | 尤其在单细胞工具中：批次矫正、多组学Anchor |

* CRISPR
```
 gRNA-Cas9      XXXXX——————————MMM
target DNA 5'———XXXXX——————————PAM——3'

CRISPR靶向特异性：
    1. pairing between gRNA and target DNA
    2. binding between Cas9 and short motif PAM
```

* 系统发育树（效果不好）
    - Hyperbolic space 更适合 hierarchical latent structure (Tree Embedding)
    - [旅行商问题思路](https://www.sciencedirect.com/science/article/pii/S2589004220308476)解决 min state flip，以推断 perfect phylogeny
    - DEPP用于扩充单基因树


## [Machine Learning and Deep Learning in Synthetic Biology: Key Architectures, Applications, and Challenges (2024)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10918679/)


* [细胞工程](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10918679/bin/ao3c05913_0003.jpg) 
    - 预测启动子/RBS强度
    - 预测目标基因表达强度
    - sgRNA on/off-target binding

* [代谢工程](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10918679/bin/ao3c05913_0005.jpg)：代谢通路设计/优化/量产
    - [ART](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7519645/) 为希望达成的 response（化合物产量） 提供推荐 input（omics）：由于化合物可能来自多条代谢通路，需要在**不影响整体细胞状况**的情况下最大化其产量
    - [Optimus 5-Prime](https://zhuanlan.zhihu.com/p/685900922): 5′UTR序列(长度/SNV/..)与翻译调控(ribosome footprints 密度)之间的关系


* 训练数据获取
    - 长度有限的序列（5′UTR/promoter）可通过生成随机/半随机 Libraries，进行  massively parallelized assays 



## 单细胞中应用


* [SAUCIE (2019)](https://www.nature.com/articles/s41592-019-0576-7): 可以用AE中间层的输出进行批次矫正、聚类、细胞类型注释等，以应对稀疏、噪音等问题，[说明](https://cloud.tencent.com/developer/article/1781390)。


* [DISC (2020)](https://cloud.tencent.com/developer/article/1785312): 半监督学习插补缺失值；将AE重构表达谱循环输入AE，最后取所有表达谱的加权平均值作为插补结果。




## 其它话题

* [LOGO (2022)](https://cloud.tencent.com/developer/article/2202917): 语言模型，可被迁移用于序列标记任务（启动子识别、增强子-启动子相互作用预测、染色质状态预测）和非编码变异优先排序任务

* [AE对MS蛋白质组数据进行插补](https://www.nature.com/articles/s41467-024-48711-5): ???


### WES for CNV detection

* [DECoNT (2022)](https://genome.cshlp.org/content/32/6/1170.long)
* [ECOLE (2024)](https://www.nature.com/articles/s41467-023-44116-y)

WES 使用 targeting probes，因此其数据中存在 length/GC/reference biases，故而使用此类数据进行的 CNV 检测精度不佳。但是它便宜。


DECoNT 基于 matched WES and WGS data (1000 Genomes Project) 进行训练，纠正 WES-based germline CNV callers 的结果。

1. CNVnator Call CNV，[单个样本的CNV统计结果按照位置区间排列](https://blog.csdn.net/yangl7/article/details/114656482)
2. BiLSTM读取、生成各个位置区间的CNV信息（WES），输出尽可能接近WGS数据结果


ECOLE 主要改用 Transformer 架构优化了一下、加入了人类专家标记数据，可以达到 68.7% precision and 49.6% recall，并可推广至其他测序平台数据


### TFBS prediction

* [DeepSEA (2015)](https://www.nature.com/articles/nmeth.3547) 根据 non-coding region 中的突变信息预测 TF binding、DNaseI sensitivities、histone marks
* [TFcoop (2019) 非DL](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6359851/) 是 logistic model (LASSO)；利用序列 + cooperating TFs' binding affinity 推断TFBS

注：训练集的TFBS信息从Chip-seq 数据获得，可从 [ENCODE](https://www.encodeproject.org/)下载

传统生信项目一般使用[PWM矩阵（motif.jaspar文件）](https://www.jianshu.com/p/b1abf71c78cf)在基因组中扫描潜在TFBS





