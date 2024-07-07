

[GATK](GATK.md)/芯片获取SNP信息后，可以进行全基因组关联分析


## PLINK

提供一些进化意义上的filtering选择和关联分析

```bash
conda create -n test
conda activate test
conda install -c bioconda vcftools -y
conda install -c bioconda bedtools -y
conda install -c bioconda plink -y
```



1. 格式转换，[PLINK's INPUT Formats](https://www.cog-genomics.org/plink/1.9/input)，[PLINK File-Format PED](https://easygwas.biochem.mpg.de/faq/view/15/)
```bash
## raw.log  raw.map  raw.nosex  raw.ped
plink --vcf snp.vcf --recode --out raw --const-fid --allow-extra-chr    ## vcftools --vcf snp.vcf --plink --out raw
## raw.bed  raw.bim  raw.fam
plink --file raw --make-bed --out raw    

--vcf    输入vcf          ——file（支持gz）
--bfile  输入bed bim fam  ——perfix
--file   输入map ped      ——perfix
```


2. 初步过滤
```bash
## clean.bed  clean.bim  clean.fam  clean.log  clean.nosex
plink --bfile raw --mind 0.1 --maf 0.05 --geno 0.05 --hwe 0.00001 --make-bed --out clean


--mind      max missing call frequencies (filtering samples)
--maf       min allele frequency (filtering SNPs)
--geno      max missing call frequencies (filtering SNPs)    0.05 即要求 call rate > 95%
--hwe       max Hardy-Weinberg equilibrium exact test p-values (filtering SNPs)
```

3. LD过滤
```bash
## 得到LD标记：prune.in prune.out； Fail，可能数据太少
plink --bfile clean --indep-pairwise 50 5 0.5 --out LD
## 调取LD位点
plink --bfile clean --extract LD.prune.in --make-bed --out LDin
```

4. 统计操作
```bash
## 查看缺失率：{rawmiss.imiss(样本缺失率)  rawmiss.lmiss(SNP位点缺失率)}  rawmiss.log  rawmiss.nosex
plink --file raw --missing --allow-extra-chr --out rawmiss

## 查看MAF频率：{cleanmaf.frq}  cleanmaf.log  cleanmaf.nosex
plink --bfile clean  --freq --allow-extra-chr --out cleanmaf

## 统计样本杂合度：{cleanhet.het}  cleanhet.log  cleanhet.nosex
plink --bfile clean --het --out cleanhet
```

5. 提取数据
```bash
## 提取/删除样本  --keep/--remove; 
echo -e "0\tSample1" > samples.txt   ## FamilyID，SampleID，见ped文件
plink --bfile clean --keep samples.txt --make-bed --out keepS \

## 提取/删除SNP  --extract/--exclude
echo -e "12149"> snps.txt
plink --bfile clean --exclude snps.txt --make-bed --out delP
```

6. **关联分析**，可用 ```--assoc```,```–-fisher```,```--model```

7. 进行表型/基因型/协变量的**关联分析**（未尝试）
```bash
## --linear/--logistic
plink --bfile clean --linear --pheno pheno.txt --mpheno 1,2,3 --covar covar.txt --covar-number 1,2,3 --out asso_res


pheno.txt: FamilyID，SampleID，PhenotypeA，PhenotypeB，...
covar.txt: FamilyID，SampleID，height，gender，...
mpheno/--covar-number 1,2,3 选择第1、2、3个表型、协变量
如果数值是二分类0/1，使用 --logistic
```

8. [LD pruning & clumping](https://gwaslab.org/2021/05/18/pruning-and-clumping/): 抽取两两之间不关联的SNP子集
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

通常一次操作多个SNP，需要对p-val进行多重比较的矫正。矫正后会通过点图查看SNP的位置
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


PLINK提供关联分析（6、7）


## 参考
```
教程汇总     https://zhuanlan.zhihu.com/p/356927396    https://www.cnblogs.com/chenwenyan/p/11803311.html
GWAS介绍     https://www.jianshu.com/p/acdc4a22e30a
GWAS流程     https://zhuanlan.zhihu.com/p/667352071
GWAS示例     https://www.jianshu.com/p/23058873b814
GWAS R       https://www.r-bloggers.com/2017/10/genome-wide-association-studies-in-r/       + association v.s. linkage mapping
PLINK        https://www.jianshu.com/p/2bf82e596e45  
PLINK        https://zhuanlan.zhihu.com/p/157291097  关联分析/...
```
