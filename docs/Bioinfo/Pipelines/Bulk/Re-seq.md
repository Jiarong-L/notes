
将测序结果比对至已知reference，可探测个体的突变信息


## Pipeline

对每个样本：Mapping 后 drop PCR duplicates + 低质量的Mapping (MAPQ<10)，call variants：

| Variants | Detection | Annotation |
| -- | -- | -- |
| SNP/INDEL | GATK | ANNOVAR: UTR/exon/upstream/splicing/... + CDS: synonymous/frameshift/stopgain/... |
| SV | BreakDancer | dbVar |
| CNV | CNVnator | -- |

此外还有常用突变频率数据库（G1000/ExAC/ESP6500/dbSNP），功能预测数据库（dbNSPF），突变治病信息与表型数据库（HGMD/dbGap/ClinVar）


随后，针对不同的实验设计，可进行群体分析/GWAS/Binmap/QTL/...  TBA



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

