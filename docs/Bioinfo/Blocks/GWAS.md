

[GATK](GATK.md)/芯片获取SNP信息后，可以进行全基因组关联分析

推荐 [GWASLab 系列笔记](https://gwaslab.org/2021/03/29/ld-score-regression/)

## 预处理

预处理 + 分析流程

1. 合并数据：snpflip 统一正负链方向，对于芯片数据需要进行 Genotype-Imputation（因为非全测序的数据覆盖区域不一）

2. 去除低质量样本(```--remove xx.txt(FID IID)```)：样本缺失率大于5%的个体(```--mind 0.05```)，杂合个体(```--het```)，性别不一致个体(```--check-sex```)，缺失率大于20%的位点，不符合HW平衡的位点(case/control设计中)

3. 去除低质量SNP: ```plink --bfile xxx --hwe 0.00001 --geno 0.02 --maf 0.01 --make-bed --out yyy```

4. 进行群体分层校正: 按分层切割群体、独立分析，或者将混杂因素（年龄，性别，PCA的若干PCs...）作为协变量添加入模型

5. 分析：关联分析，MR分析，...

6. 解释结果：LocusZoom图可视化显著SNP周围的LD block，...


[参考](https://www.cnblogs.com/chenwenyan/p/11803311.html)


### PLINK:数据处理

提供一些进化意义上的filtering选择和关联分析

```bash
conda create -n test
conda activate test
conda install -c bioconda vcftools -y
conda install -c bioconda bedtools -y
conda install -c bioconda plink -y
```



* 格式转换，[PLINK's INPUT Formats](https://www.cog-genomics.org/plink/1.9/input)，[PLINK File-Format PED](https://easygwas.biochem.mpg.de/faq/view/15/)
```bash
## raw.log  raw.map  raw.nosex  raw.ped
plink --vcf snp.vcf --recode --out raw --const-fid --allow-extra-chr    ## vcftools --vcf snp.vcf --plink --out raw
## raw.bed  raw.bim  raw.fam
plink --file raw --make-bed --out raw    

--vcf    输入vcf          ——file（支持gz）
--bfile  输入bed bim fam  ——perfix
--file   输入map ped      ——perfix
```


* 初步过滤
```bash
## clean.bed  clean.bim  clean.fam  clean.log  clean.nosex
plink --bfile raw --mind 0.1 --maf 0.05 --geno 0.05 --hwe 0.00001 --make-bed --out clean


--mind      max missing call frequencies (filtering samples)
--maf       min allele frequency (filtering SNPs)
--geno      max missing call frequencies (filtering SNPs)    0.05 即要求 call rate > 95%
--hwe       max Hardy-Weinberg equilibrium exact test p-values (filtering SNPs)
```

* LD过滤
```bash
## 得到LD标记：prune.in prune.out； Fail，可能数据太少
plink --bfile clean --indep-pairwise 50 5 0.5 --out LD
## 调取LD位点
plink --bfile clean --extract LD.prune.in --make-bed --out LDin
```

* 统计操作
```bash
## 查看缺失率：{rawmiss.imiss(样本缺失率)  rawmiss.lmiss(SNP位点缺失率)}  rawmiss.log  rawmiss.nosex
plink --file raw --missing --allow-extra-chr --out rawmiss

## 查看MAF频率：{cleanmaf.frq}  cleanmaf.log  cleanmaf.nosex
plink --bfile clean  --freq --allow-extra-chr --out cleanmaf

## 统计样本杂合度：{cleanhet.het}  cleanhet.log  cleanhet.nosex
plink --bfile clean --het --out cleanhet
```

* 提取数据
```bash
## 提取/删除样本  --keep/--remove; 
echo -e "0\tSample1" > samples.txt   ## FamilyID，SampleID，见ped文件
plink --bfile clean --keep samples.txt --make-bed --out keepS \

## 提取/删除SNP  --extract/--exclude
echo -e "12149"> snps.txt
plink --bfile clean --exclude snps.txt --make-bed --out delP
```

* [LD pruning & clumping](https://gwaslab.org/2021/05/18/pruning-and-clumping/): 抽取两两之间不关联的SNP子集
```bash
--indep-pairwise 500 50 0.2                pruning
--clump                                    clumping
```







## 关联分析

假设我们需要计算某SNP是否与某性状存在关联，一般采用线性回归的方式计算p值：
```  
        if斜率 > 0                       if斜率 = 0
   |                                |
 B |               **             B |
 M |        *      *              M |         *
 I | *      **                    I | **     ***    **
   | **                             |
   |____________________            |____________________        
     AA     AT     TT                 AA     AT     TT    

SNP: A/T       p-val=???, effect=斜率   注，GWAS示例一般使用十万多样本
```

通常一次操作多个SNP，需要对p-val进行多重比较的矫正，矫正后会通过曼哈顿图查看SNP的位置。
```
-log10(p-val)
    |                    *
    |      *            
    |        *
    |  *************************
    |_________________________________
           Genome Position
```

与某性状显著关联的SNP不一定位于基因内，它很可能只是与关键基因存在连锁不平衡(LD)。进行GWAS后，可以关注此SNP周边的基因，其中很可能包含真正作用于目标性状的基因。（即：GWAS起到了缩小检验范围的作用）

### PLINK:关联分析

* **关联分析**，可用 ```--assoc```,```–-fisher```,```--model```，也可以通过 ```--condition xxSNP``` 消除来自另一个SNP的影响

* 进行表型/基因型/协变量的**关联分析**（未尝试）
```bash
## --linear/--logistic
plink --bfile clean --linear --pheno pheno.txt --mpheno 1,2,3 --covar covar.txt --covar-number 1,2,3 --out asso_res


pheno.txt: FamilyID，SampleID，PhenotypeA，PhenotypeB，...
covar.txt: FamilyID，SampleID，height，gender，...
mpheno/--covar-number 1,2,3 选择第1、2、3个表型、协变量
如果数值是二分类0/1，使用 --logistic
```

如果 ```--pca``` 显示存在群体分层，直接进行关联分析会造成假阳性，建议将 ```_pca.eigenvec``` 加入 covar.txt 以消除影响


分析完成后，如果p-val分布不符合正态分布（QQ plot），需要考虑是否存在基因多效性（[进行 LD score regression](https://gwaslab.org/2021/03/29/ld-score-regression/)） 或群体分层（[计算基因组膨胀系数](https://gwaslab.org/2021/07/07/genomic-control/)）


除了关注单个SNP，也可以对个体计算其[多基因风险得分(PRS)](https://gwaslab.org/2021/08/04/prs/)，综合评估多个弱SNP对形成某种表型的影响。







## 孟德尔随机化

[孟德尔随机化(Mendelian randomization)](https://gwaslab.org/2021/06/24/mr/) 通过 [Instrumental Variables Z 消除 Confounding U 的影响](../../Course/Causal_Inference_I.md#l8-do-instrument)，以此探寻因果关系（而不仅仅是相关性）

```
          U
        /   \(e)    
Z ---> T ---> Y       （假设）causal equation Y:= dT + eU , 求 d
  (c)    (d)     


1. regress T on Z, 得到 T 中被 Z 解释的部分 T' = .. + c*Z
2. regress Y on T', 得到 Y 中被 T' 解释的部分 Y' = .. + d*T'    其中 d 即为所求


```
Z可以是一个SNP，T是与Z强相关的某个因素（暴露因素），Y是不与Z直接相关的结果（表型性状）

从GWAS结果中选取与T显著相关的Z（pruning/clumping保证SNP之间相互独立），即可开始MR分析。

### R:TwoSampleMR

[TwoSampleMR官方示例](https://mrcieu.github.io/TwoSampleMR/articles/perform_mr.html)，[原理+代码示例](https://gwaslab.org/2021/11/14/twosamplemr/)


* 读取 exposure_data T 的GWAS数据：输入表格中每一行代表一个SNP，必须含!符号的4列:
```R
exp_dat <- read_exposure_data(
    filename = "", sep = "\t",
    snp_col = "",                  #! SNP ID 列（header名）
    beta_col = "",                 #! The effect size，GWAS关联分析得到的斜率
    se_col = "",                   #! The standard error of the effect size
    effect_allele_col = "",        #! The allele of the SNP which has the effect marked in beta  e.g. A
    other_allele_col = "",          # The non-effect allele e.g. T
    eaf_col = "",                   # The effect allele frequency
    pval_col = "",
    ...
)
```

* LD Clumping 获取互不相关的SNP子集: ```clump_data(exp_dat, clump_r2=0.01, pop = "???")```  需要预先得知相关population中的LD关系

* 读取 outcome_data Y 的GWAS数据，提取上述SNP子集
```R
## 若使用 extract_outcome_data(snps = exp_dat$SNP, outcomes = 'GWAS id')    则需要从 https://gwas.mrcieu.ac.uk/ 查询 GWAS id，或者
out_dat <- read_outcome_data(
    filename = "", sep = "\t",
    snps = exp_dat$SNP,
    snp_col = "",  
    ...
)

## The effect of a SNP on an outcome and exposure must be harmonised to be relative to the same allele
dat <- harmonise_data(
    exposure_dat = exp_dat, 
    outcome_dat = out_dat
)
```

*  ```res <- mr(dat)``` 获取MR分析结果（不同method计算得到 Y-T 是否有因果关系的pval），作图及异质性分析等详见官方教程，[最常用的两种方法原理](https://cloud.tencent.com/developer/article/2078504)



## LD

连锁不平衡(Linkage Disequilibrium, LD) 指群体内，不同位点处等位基因间的非随机关联。例如，对于 Aa/Bb 这两个位点，其相应表型的频率可以是：

| 表型 | 完全独立(```r^2 = 0```) | 完全连锁(```r^2 = 1```) |
| -- | -- | -- |
| AB | 0.25 | 0.5 |
| Ab | 0.25 | 0 |
| aB | 0.25 | 0 |
| ab | 0.25 | 0.5 |

度量 LD 的基本指标为 ```D = P(AB) - P(A)P(B) = P(AB)P(ab) - P(aB)P(Ab)```，标准化后得到系数  ```r^2 = D^2 / [P(A)P(B)P(a)P(b)]```。假如 ```r^2 = 1```，即说明基因型(A)与基因型(B)总是同时出现。

一般而言，由于染色体重组等机制，两个位点在基因组上离得越远，相关性越弱(```r^2 < 0.1```即可被认为没有相关性)。


* GWAS研究通常会绘制LD衰减曲线，其x轴为标记的物理距离(kb)，其y轴为物种的LD系数(```r^2```)，取```r^2 = 0.1```时的距离为```LD衰减距离```。GWAS研究的标记间隔不能超过这个距离，因为间隔过大可能会导致遗漏潜在的信号。

* GWAS检验中，某个SNP的效应(effect)通常也会包含与其高度相关的位点的效应（遗传因素），有可能受到分层等因素的干扰（混杂因素），二者都会造成更高的卡方检验量。LD score regression (LDSC) 设定对卡方统计量设定回归公式（遗传+混杂），以定量区分二者的大小 ----- 主要关心SNP的遗传力
  - ```LD score``` 即某SNP与一定范围内其他SNP的```r^2```之和，公式中‘遗传项’的一部分
  - ldsc库可实现，需提供 SWAS statistics + 研究群体的LD参考

* S-LDSC同理，公式中基于注释分层（功能/细胞类型/组织...）
  - gsMap: 空间转录组中，选取了 Marker Gene 后可获得它们对应调控区域内的SNP，S-LDSC 得到对应细胞中这些SNP的遗传力（针对表型的解释中）



## 参考
```
教程汇总     https://zhuanlan.zhihu.com/p/356927396    https://www.cnblogs.com/chenwenyan/p/11803311.html
GWAS介绍     https://www.jianshu.com/p/acdc4a22e30a
GWAS流程     https://zhuanlan.zhihu.com/p/667352071
GWAS示例     https://www.jianshu.com/p/23058873b814
GWAS R       https://www.r-bloggers.com/2017/10/genome-wide-association-studies-in-r/       + association v.s. linkage mapping
PLINK        https://www.jianshu.com/p/2bf82e596e45  
PLINK        https://zhuanlan.zhihu.com/p/157291097  关联分析/...
Meta分析     https://www.sciencedirect.com/science/article/pii/S2772594422001169  
Meta示例     https://blog.csdn.net/m0_37228052/article/details/133026057
gsMap        https://www.bilibili.com/video/BV1aGTtzeENM/
S-LDSC       https://gwaslab.org/2021/03/29/ld-score-regression/
```
