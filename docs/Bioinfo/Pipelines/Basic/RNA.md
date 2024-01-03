<style>
img{
    width: 60%;
}
</style>


其它：可变剪接的研究，非编码RNA与靶基因的互作...

## mRNA Pipeline
基因的表达水平

* QC & Trim
* Clean Data
    - Remove host RNA (Human + host) via mapping result
    - Remove rRNA (SILVA,GreenGene,[NCBI rRNA](https://ftp.ncbi.nlm.nih.gov/blast/db/)...) via mapping result
* Assembled Genome
    - Opt1. NCBI Ref / same sample's DNA assembly
    - Opt2. denovo -- 组装完成后可以与Opt1的contigs合并、去重
        * Trinity / rnaSPAdes / IDBA-MT (for Meta)
* Gene Prediction & dereplicate
* Gene expression Counts (RPKM/...)
    - via Mapping: HISAT2+stringTie / SOAPaligner
    - via Kmer: Kallisto/Salmon
* Diff expr
    - DESeq2 / edgeR / limma
* Gene Functions
    - GO / KEGG / String / ...


## Dual RNA-seq Pipeline
针对病原体和宿主之间的互作；无需分离二者、减少数据损失。

![dualRNA](../Pipelines_overview/img/dualRNA.png)
 
* 必须有Host与Patho的参考基因组。若无，Host可找近缘物种提取contigs，而Patho比较容易直接组装
* 互作：共生、寄生、竞争、捕食
* Patho可以是一个物种，也可以是Meta数据
