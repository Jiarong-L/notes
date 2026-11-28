<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache:   'global'   // 'local',or 'global' or 'none'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>
<script type="text/javascript" id="MathJax-script" async
  src="http://127.0.0.1:8000/Statistics/Basis/tex-svg.js">
</script>



将测序结果比对至已知reference，可探测个体的突变信息


## Pipeline

对每个样本：Mapping 后 drop PCR duplicates + 低质量的Mapping (MAPQ<10)，call variants：

| Variants | Detection | Annotation |
| -- | -- | -- |
| SNP/INDEL | GATK | ANNOVAR: UTR/exon/upstream/splicing/... + CDS: synonymous/frameshift/stopgain/... |
| SV | BreakDancer | dbVar |
| CNV | CNVnator | -- |


随后，针对不同的实验设计，可进行群体分析/GWAS/[Binmap](https://www.limfx.pro/readarticle/1255/binmap)/QTL/... ** TBA**

注意各种应对 linkage disequilibrium 的方式 (LD修剪, Fine‑mapping, ...)


## Annotation

我们可能会关心 Variants 位于哪里，从生物意义上推导可能的后果

在使用 [ensembl VEP](https://www.ensembl.org/Tools/VEP) 注释 VCF 时，工具会寻找与位点重叠的 （基因、转录本、调控区域、motif）并且返回相应的 [Sequence Ontology 术语](https://www.sequenceontology.org/browser/current_release/term/SO:0002220/)，并且可以叠加外部注释：


- 突变频率：这个变异在人群里有多常见，**GnomAD**(基于 GRCh38) 
- 功能预测：这个变异会不会破坏功能（保守性），**dbNSFP**
- 临床信息与表型：这个变异和疾病什么关系，ClinVar (公开、胚系为主) / COSMIC (体细胞、癌症驱动) / HGMD (ClinVar)

另外，还可以关注 dbGap (原始研究归档：也可以从中找出一些疾病关联)，以及 dbSNP (分发**rsID**，可能提供一些频率信息)

## 群体分析

群体遗传分析：研究群体中基因型频率的分布及其变化规律，揭示自然选择、突变、迁移、遗传漂变等进化动力对群体结构的影响。其最终目标是阐明生物进化机制，并为育种与疾病研究提供理论基础。e.g. 培育短尾羊


拿到数据后，对单倍型特征（e.g.SNP profile）进行PCA降维、或者基于遗传距离进行PCoA降维，可以粗略判断是否存在明显的**群体分层**


### 进化树

基于遗传距离(Neighbor-Joining)/单倍型特征构建**系统发育树**，推断群体或个体间的进化关系/亲缘关系远近





















### 选择信号

进化动力对群体结构的影响，即：自然/人工的选择对哪些遗传位点的影响比较大？


* 群体间等位基因频率的差异（**Fst**:衡量种群分化程度，0=随机交配/1=完全隔离）可以用于寻找在特定群体中受强烈选择的基因组区域，e.g.对比野生群体与家畜，可以知道人工选育（正选择）的影响


* 群体内的遗传多样性，也可以提示进化事件（作为Fst结果的补充，毕竟差异可能不仅仅来自人工选育）
    - Tajima’s D: ```D = 0``` 中性进化，```D < 0``` **稀有突变过多**，```D > 0``` 中等频率突变过多
    - 核苷酸多样性 π: 随机抽取两条序列，它们平均在多少位点上存在差异。选择压力可能导致这个基因组区域中**多样性降低**（π < 0.005 / 物种经验值 / 全基因组平均水平）
    - iHS: 由于重组会不断打断单倍型，中性进化SNP周围片段的相似程度会随着距离衰减，但正选择会保留SNP周围片段、保留较长的单倍型。 ```iHS > 0``` 即 ```Derived > Ancestral``` 衍生等位基因的单倍型更长，提示正选择发生的位置。



| π | Tajima‘s D | iHS  | 事件 |
| -- | -- | -- | -- |
| 背景水平 | `0` | `0` | 中性进化（中性突变 + 遗传漂变） |
| 低 | `-` | `-` | hard sweep（新突变受到选择压力 -> 固定；新突变意味着只在一条染色体上，所以突变周围的序列一致） |
| 低 | `-` | `+` | soft sweep（旧突变受到选择压力 -> 固定；旧突变意味着它的拷贝可能分布在不同染色体上，即突变周围会有不同的序列） |
| 高 | `+` |  | 平衡选择（维持多样性） |
| 低（全基因组水平） | `+` |  | 近期群体瓶颈 |
| 背景水平/高 | `-` |  | 近期群体扩张 |
| 低 | `-` |  | 背景选择（有害突变被清除时，顺带清除了旁边的中性突变） |
| 背景水平/高 | `?` |  | 基因渗入 |



### 祖源

**祖先成分/群体混合历史**的推断一般使用 Admixture Model：将个体的基因组看作是来自K个潜在祖先群体的混合

假设大小为 N 的群体中，每个个体的 M 个SNP位点上的基因型来自 K 个祖先

$$Q_{N,K}
\left[
\begin{array}{c|ccc}
 & \mathrm{祖先1} & \mathrm{祖先2} & \mathrm{祖先3}\\\\
\hline
\mathrm{个体1} & 0.6 & 0.3 & 0.1\\\\
\mathrm{个体2} & 0.1 & 0.7 & 0.2
\end{array}
\right]P_{K,M}
\left[
\begin{array}{c|ccc}
 & \mathrm{Site1} & \mathrm{Site2} & \mathrm{Site3}\\\\
\hline
\mathrm{祖先1} & 0.9 & 0.2 & 0.5\\\\
\mathrm{祖先2} & 0.3 & 0.8 & 0.1\\\\
\mathrm{祖先3} & 0.1 & 0.1 & 0.7
\end{array}
\right] = Observe \left[
\begin{array}{c|ccc}
 & \mathrm{Site1} & \mathrm{Site2} & \mathrm{Site3}\\\\
\hline
\mathrm{个体1} & 0.64 & 0.37 & 0.40\\\\
\mathrm{个体3} & 0.32 & 0.60 & 0.26
\end{array}
\right]
$$


* 常用工具
    - STRUCTURE: Dirichlet分布作为贝叶斯推断的先验 + MCMC采样
    - ADMIXTURE: 寻找使观测值出现概率最大的Q和P (最大似然估计)



## Notations

* [HGVS命名规范](https://www.hgvs.org/mutnomen/recs-DNA.html) & [坐标转换](https://mutalyzer.nl/)
```
NM_000500 .7 (CYP21A2): c. 293-13 C>G

NM_000500 .7  转录本/染色体名称+版本号
CYP21A2       基因名称
c./n./g.      coding/non-coding/genome
C>G           mutation
```


* 纯合突变hom/杂合突变het
```
hom  所有等位基因都发生突变，对于二倍体：    aa->AA
het    等位基因之一发生突变，对于二倍体：    aa->Aa
```


* [RIL群体](https://zhuanlan.zhihu.com/p/374834118)：F2开始连续自交或同胞交配直至趋于纯合，过程中经历多次减数分裂，重组程度高于F2，比F2更能解析F1代配子的分离。


* SNP
```
Ref     TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT

Reads                   TTTTTTTTTTTCTTTTTTTT    SNP: T>C
                      TTTTTTTTTTTTTCTTTTTT  
                  TTTTTTTTTTTTTTTTTGTT          Sequencing Error
                          TTTTTTTTTCTTTTTTTTTT

考虑到+/-链的问题：正链(T>C)==负链(A>G)，故统称 T:A>C:G
情形共有： C:G>A:T  |  C:G>G:C  |  C:G>T:A  |  T:A>A:T  |  T:A>C:G  |  T:A>G:C 
```

* INDEL
```
Reads              TTTTTTTTTTT                Deletion: GGG deleted in query seq
                       / \
Ref     TTTTTTTTTTTTTTTGGGTTTTTTTTTTTTTTTTTTTTTTTTTTTT
                                / \
Reads                   TTTTTTTTAAATTTTT      Insertion: AAA inserted to query seq
```


* SV (Structural variation)，下文 CNV 是特殊的 SV
```
RefRegion1     TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
RefRegion2     GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG

Reads              TTTTTTTTGGGGGG           SV: >1kb region, can be cross-chromosomal
```

* CNV (Copy Number Variation)检测方法：根据深度/断裂点/突变基因型
```
对于二倍体：

Ref          ===========GeneA==========
缺失         ==========================
重复         ===========GeneAGeneA======

或发生在两条姐妹染色单体之间：
             -----------GeneAGeneA------
             ---------------------------
```


* 哈迪–温伯格平衡：在“种群足够大、随机交配、无突变、无选择、无迁移、无遗传漂变”时，等位基因频率 p、q 及基因型频率 p²、2pq、q² 在世代间保持稳定不变
    - 设 `p=P(A), q=P(a)`，
    - 等位基因频率：`p + q = 1`
    - 基因型频率：`p² + 2pq + q² = 1`


* 如果两个个体在某loci上的等位基因相同，可能 IBS (碰巧一致、无亲缘) / IBD (来源于同一祖先)。我们只能观测到 IBS，然后用它推断 IBD 的值；由于真正的 IBD 会形成较长的连续共享片段（正选择事件），所以推断选取IBD片段时需要考虑连续多个位点的 IBS 模式，通常使用HMM进行模拟、选取总概率`P(IBS:1→2→1→.., IBD:0→1→1→..)`最大的那条状态跳转路径
    - 转移概率 `P(状态_{t}|状态_{t-1})`：基于两个SNP位点之间的遗传距离（或物理距离）
    - 发射概率 `P(观测|状态)`：基于等位基因的频率，计算当前点位因为随机概率形成当前IBS状态的可能性 `P( IBS=i ∣ IBD=z)`

| 个体 | 个体 | IBS | `P( IBS=i ∣ IBD=0)` --- IBD=1/2也可计算 |
| -- | -- | -- | -- |
| AA | AA | 2 | `P(AA,AA)+P(aa,aa) = (pp)(pp) + (qq)(qq)` = $$p^4 + q^4$$ |
| ... |
| Aa | Aa | 2 | `P(Aa,Aa) = (2pq)(2pq)` = $$4p^2q^2$$ |
| AA | Aa | 1 | `P(AA,Aa)+P(Aa,AA)+P(Aa,aa)+P(aa,Aa)= (pp)(2pq) + ..` = $$4p^3q+4pq^3$$ |
| ... |
| AA | aa | 0 | `P(AA,aa)+P(aa,AA)` =$$2p^2q^2$$ |
| ... |


* 全局IBD状态可用于推断亲缘关系，例如 PLINK 使用的 `PI_HAT = Z2 + 0.5×Z1` 依次对应 `0(无亲缘)`-`0.25(表兄弟姐妹)`-`0.5(亲子/兄弟姐妹)`-`1(本人/同卵双胞胎)`
    - 统计全基因组范围内所有点位的随机概率的均值 `P_( IBS=i ∣ IBD=z)`
    - 统计全基因组范围的 `P_(IBS=i)`
    - 对 `z=0/1/2  i=0/1/2`，我们可以从方程 `P_(IBS=i) = ∑P_(IBS=i∣IBD=z)P_(IBD=z)` 中求解全基因组范围内的 ` P_(IBD=z)`（简写为`Z0/Z1/Z2`）


