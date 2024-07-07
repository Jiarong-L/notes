
[孟德尔随机化(Mendelian randomization)](https://gwaslab.org/2021/06/24/mr/) 通过 [Instrumental Variables Z 消除 Confounding U 的影响](../Course/Causal_Inference_I.md#l8-do-instrument)，以此探寻因果关系（而不仅仅是相关性）

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



## R

[TwoSampleMR官方示例](https://mrcieu.github.io/TwoSampleMR/articles/perform_mr.html)，[原理+代码示例](https://gwaslab.org/2021/11/14/twosamplemr/)


1. 读取 exposure_data T 的GWAS数据：输入表格中每一行代表一个SNP，必须含!符号的4列:
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

2. LD Clumping 获取互不相关的SNP子集: ```clump_data(exp_dat, clump_r2=0.01, pop = "???")```  需要预先得知相关population中的LD关系

3. 读取 outcome_data Y 的GWAS数据，提取上述SNP子集
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

4. ```res <- mr(dat)``` 获取MR分析结果（不同method计算得到 Y-T 是否有因果关系的pval），作图及异质性分析等详见官方教程，[最常用的两种方法原理](https://cloud.tencent.com/developer/article/2078504)


