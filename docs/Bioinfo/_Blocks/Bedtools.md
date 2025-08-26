
[Bedtools](https://bedtools.readthedocs.io/en/latest/index.html)支持处理BAM, BED, GFF/GTF, VCF；[简书Bedtools笔记](https://www.jianshu.com/p/f8bbd51b5199)也很有帮助


## Install
```
conda install -c bioconda bedtools
```

## I/O

Input支持 ```-i <FILENAME>``` 或者 ```-i stdin``` 或者 ```-i -``` 
```bash
bedtools bamtobed -i A.bam > A.bed
cat A.bam | bedtools bamtobed -i stdin > A.bed
cat A.bam | bedtools bamtobed > A.bed           ## 只有一个输入文件时候可以忽略 -i 参数 
```
Output一般为标准输出，用```>```保存至文件

注意，输入中要求的 ```-g GENOME``` 格式包含contig Name & Len：
```
samtools faidx A.fa
cut -f1,2 A.fa.fai >A.GENOME
```

## Format conversion

可以提取mapped region， mapped fq，
```bash
bedtools bamtobed -i A.bam > A.bed
bedtools bamtofastq -i A.bam  -fq R1.fq.gz -fq2 R2.fq.gz   ### if R1 in bam but R2 not, Skipping & raise warning
```

可以将BED12格式转换成最常见的BED6格式：```bedtools bed12tobed6 -i A.bed12 > A.bed6```  

此外 ```bedtools bedtobam -i A.bed -g A.GENOME > A.bam.re``` 帮助压缩储存大型注释文件；```bedtools bedpetobam```同理，不过输入是 BEDPE 

## Fasta manipulation


[getfasta](https://bedtools.readthedocs.io/en/latest/content/tools/getfasta.html) 获取BED对应区域的FASTA序列，[maskfasta](https://bedtools.readthedocs.io/en/latest/content/tools/maskfasta.html)BED对应区域的FASTA序列mask为NNNNN，nuc计算FASTA文件对应区域的核酸含量

```bash
bedtools getfasta -fi A.fa -bed A.bed   >  A.get.fa
bedtools maskfasta -fi A.fa -bed A.bed -fo A.mask.fa
bedtools nuc -fi A.fa -bed A.bed | less    ## %AT %GC A/T/C/G/others_observed
```


## BED manipulation

从[bedtools-suite](https://bedtools.readthedocs.io/en/latest/content/bedtools-suite.html)的图示中查看其用法，指南：（此处feature指一段区域，即BED中一行）

| option | 场景 |
| -- | -- |
| complement | 获取genome中没有被A覆盖的区域 |
| intersect | 获取A/B的交集，可设定 ```-wa -v -wao```等多种模式 |
| window | 获取与A及A上下游```-l -r```bp有交集的B |
| closest | 获取与A距离最近的B |
| subtract | 获取A中不与B重叠的部分 |
| merge | 将A中有重叠/距离近的features合并为一个feature |
| cluster | 按距离将A中features分组（但不merge） |
|  |  |
| groupby | groupby ```-g col1,2,3``` 然后```-o <opreation>```计算统计量 |
| map | 将一些内置函数```-o <opreation:mean,collapse,..>```应用于BED或BEDPE文件 |
|  |  |
| slop | 提取A及A上下游```-l -r```bp区域 |
| flank | 提取 A上下游```-l -r```bp(不包括A)区域 |
| overlap | 计算A/B间overlap | IN:BEDPE<br>OUT:BEDPE+overlapbp+... |
| coverage | 计算A被B覆盖区域的大小与比例 |
| annotate | 计算A被B/C/D/..覆盖区域的比例 |
| genomecov | 计算genome被A覆盖区域的大小与比例 |
| summary | 对genome的各种统计 |
|  |  |
| shift | 坐标修正 |
| sort | BED排序 |
| spacing | 输入Sorted BED，计算feature与上一个feature之间的GAP(bp) |
|  |  |
| shuffle | 随机更改feature位置 |
| random | 对genome生成随机feature |
|  |  |
| expand | 将一些形如```v1,v2,v3```的行拆分成多行，每个值一行 |
| makewindows | 将features切割成窗口大小 |


此外，```igv```可用于创建igv内运行脚本，links可用于创建对应feature的UCSC注释信息（HTML格式，指向 UCSC Genome Browser）


## Example

示例一：[提取promoter序列](https://www.biostars.org/p/17162/)

```bash
## ref.GENOME includes:  chrNAME chrLEN
bedtools flank -i genes.bed -g ref.GENOME -l 2000 -r 0 -s > genes.2kb.promoters.bed
bedtools getfasta -fi ref.fa -bed genes.2kb.promoters.bed -fo genes.2kb.promoters.bed.fa
```
