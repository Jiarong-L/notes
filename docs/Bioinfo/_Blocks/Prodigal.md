

* 预测细菌和古生菌的基因序列，以备后续功能注释。       
* 关联： prokka, DRAM, checkv, BUSCO      
* 可以将多种预测方式的结果汇总后去重，然后再进行功能注释   
* 真核生物的预测更加复杂，可用：augustus，snap，GlimmerHMM，GENSCAN，genemarks    

### Install
```
conda create -n prodigal -c bioconda prodigal -y
conda activate prodigal
```

### Usage
* -p 有 single or meta 两种选项，当输入的Assembly是单个菌的时候选single，而输入的Assembly是宏基因组样本的时候选meta。
* -g 根据目标范围选择编码，查询: [The Genetic Codes](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi)
* 输出：output.faa，output.fnn，out.gff，pseudo.stat
```
prodigal -a <output.faa> -d <output.fnn> -f gff -o <out.gff> -g 11 -p single -s <pseudo.stat> -i <input_assembly.fa>


## -a <output.faa>        protein translations
## -d <output.faa>        nucleotide seq
## -f gff                 -o 's format
## -o <out.gff>           gff
## -g 11                  translation table (default 11)
## -p single              Select procedure (single or meta).  Default is single.
## -s <pseudo.stat>       All potential genes (with scores)
## -i <input_assembly.fa>    Input genome to be predicted

## -c:  Closed ends.  Do not allow genes to run off edges.
## -m:  Treat runs of N as masked sequence; don't build genes across them.
## -n:  Bypass Shine-Dalgarno trainer and force a full motif scan.
## -q:  Run quietly (suppress normal stderr output).
## -t:  Write a training file (if none exists); otherwise, read and use the specified training file.
```


### 参考
MetaProdigal: https://pubmed.ncbi.nlm.nih.gov/22796954/  
中文示例: https://zhuanlan.zhihu.com/p/76573262







