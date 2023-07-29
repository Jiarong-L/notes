
快速进行序列去重/序列相似性聚类，原理：

1. words：若需要xx%相似度，则至少有yy个长度为zz的相同word
2. index table for words

关联：UCLUST 

## Install 
conda按照，或Clone，或于此处下载：https://github.com/weizhongli/cdhit/releases
```
conda install -c bioconda cd-hit

############################## OR #####################(4.8.1)###
sudo apt install zlib1g-dev -y
git clone https://github.com/weizhongli/cdhit.git
cd cdhit
make openmp=no
cd cd-hit-auxtools
make
export PATH=$PATH:/mnt/d/WSL_dir/workdir/cdhit/:/mnt/d/WSL_dir/workdir/cdhit/cd-hit-auxtools/:/mnt/d/WSL_dir/workdir/cdhit/psi-cd-hit/
```
注意，Conda安装仅支持cd-hit、cd-hit-2d、cd-hit-est、cd-hit-est-2d、cd-hit-454、cd-hit-div；其它命令须Git Clone + MAKE 安装才支持


## Commands

* 后缀  
```
.faa = FASTA Amino Acid file  
.ffn = FASTA nucleotide coding regions file  
.fna = FASTA Nucleic Acid file  
```
* word_length & thresholds
```
####### protein
-n   word_length
            5 for thresholds 0.7 ~ 1.0 (default)
            4 for thresholds 0.6 ~ 0.7
            3 for thresholds 0.5 ~ 0.6
            2 for thresholds 0.4 ~ 0.5
####### nucleotide 
-n   word_length
            10-11  for thresholds 0.95 ~ 1.0
            8-9    for thresholds 0.90 ~ 0.95
            7      for thresholds 0.88 ~ 0.9
            6      for thresholds 0.85 ~ 0.88
            5      for thresholds 0.80 ~ 0.85
            4      for thresholds 0.75 ~ 0.8 
```

* local/global sequence identity
```
-G   If 1 (default)："global sequence identity" = 
            total length of all co-linear and non-overlapping HSPs 
            divided by length of the shorter sequence;
     If 0: "local sequence identity" = 
            identity of the top high score HSP; 
        Only use -G 0 when using alignment coverage controls -aL, -AL, -aS, -AS
```



### cd-hit
Clusters a **protein** dataset，每个cluster会有一个代表序列
```
cd-hit -i input.faa -o cdhit.faa -c 0.9 -G 1 -n 5 -M 16000 -T 8 -bak 1

-i   input.fa(.gz)*
-o   output.fa*
-c   sequence identity threshold, default 0.9
-G   sequence identity；1:global (default), 0:local
-n   word_length (default 5), selection method see above
-M   memory limit (in MB)
-T   number of threads
-bak write backup cluster file (1 or 0-default)
```

### cd-hit-2d
Compares **protein** dataset B to A
```
cd-hit-2d -i inputA.faa -i2 inputB.faa -o BmapA.faa -c 0.9 -n 5 -M 16000 -T 8 -bak 1
```

### cd-hit-est
Clusters a **nucleotide** dataset (non-intron containing); -j -op for paired end (PE) files
```
cd-hit-est -i input.ffn -o cdhitest.ffn -c 0.95 -G 1 -n 10 -M 16000 -T 8 -bak 1

cd-hit-est -i input_F.ffn -j input_R.ffn -o cdhitest_F.ffn -op cdhitest_R.ffn -c 0.95 -G 1 -n 10 -M 16000 -T 8 -bak 1
```

### cd-hit-est-2d

Compares **nucleotide** dataset B to A (both non-intron containing);   

* -j/-op for paired end (PE) files
* 1/2 for A/B datasets
```
cd-hit-2d -i inputA.ffn -i2 inputB.ffn -o BmapA.ffn -c 0.9 -n 5 -M 16000 -T 8 -bak 1

cd-hit-2d -i inputA_F.ffn -j inputA_R.ffn -i2 inputB_F.ffn -j2 inputB_R.ffn -o BmapA_F.ffn -o BmapA_R.ffn -c 0.9 -n 5 -M 16000 -T 8 -bak 1

## -mask NX: mask out both 'N' and 'X'
```


### psi-cd-hit.pl  
PSI-CD-HIT clusters **proteins at very low threshold** (cd-hit support threshold >40%), it also cluster **long DNA sequences** (cd-hit-est can not handle that)

1. Sort seq by decreasing length
2. 1st-seq as the first representative
3. Blast 1st-seq aganist all remaining sequences, pick up seqs that fits clustering threshold
4. Repeat until done
```
psi-cd-hit.pl -i input.faa -o psicdhit.faa -c 0.3 -prog blastp
psi-cd-hit.pl -i Long_contigs.fa -o Long_contigs_dRep.fa -c 0.9 -prog blastn


-prog    blastp(default), blastn, megablast, psiblast
-circle  treat sequences as circular sequence (0:no-default, 1:yes)
-g       a seq clustered to the first fitted cluster (1:fast-default) or the most similar cluster (0:slow)
-exec    qsub, local
-s       blast para, "-seg yes -evalue 0.000001 -max_target_seqs 100000" (default)
```
(need BLAST) & apply it via Hierarchical clustering!!


### Sequencing reads
* cd-hit-454：Identify duplicated 454 reads
* cd-hit-dup：Removing duplicates from sequencing reads (single/paired-end), remove chimeric reads (opt.)
* cd-hit-lap：Extracting pairs of overlapping reads (with perfect matching, tail-head overlaps)
* read-linker：Concatenate pair-end reads into single ones
```
TBA
```


### Tools
* cd-hit-div: Sort & Divide a FASTA file into pieces
* plot_len.pl: Print out distributions of clusters & sequences
* clstr_sort_by.pl: Sort clusters in .clstr file
* clstr_sort_prot_by.pl: Sort sequences within clusters in .clstr file
* clstr_merge_noorder.pl: Merges two or more .clstr files
* clstr_ renumber.pl: Renumbers clusters and sequences within clusters in .clstr file
* clstr_rev.pl: Combines a .clstr file with its parent .clstr file
* make_multi_seq.pl: Reads in .clstr file and generates a separate fasta file for each oversized clusters
* clstr2xml.pl: Convert .clstr file to xml format
```
cd-hit-div -i input.faa -o div_out.faa -div 3   ## Output: div_out.faa-0  div_out.faa-1  div_out.faa-2

TBA
```


## Output Files

* Clustering's
```
cd-hit/cd-hit-est -o out_F.fa -op out_R.fa ...

    out_*.fa: rep seq of each clusters
    out_*.fa.clstr: list of clusters (by Cluster)
    out_*.fa.bak.clstr: list of clusters (by Seq)
```
* Comparing's
```
cd-hit-2d/cd-hit-est-2d -o out_F.fa -op out_R.fa ...

    out_*.fa: seq in B that connot maps to A
    out_*.fa.clstr: list of similar sequences between A,B (by Cluster)
    out_*.fa.bak.clstr: list of similar sequences between A,B (by Seq)
```
* Clustering's: psicdhit
```
psicdhit -o psi_out.fa ...

    psi_out.fa
    psi_out.fa.clstr
    psi_out.fa.log
    psi_out.fa.out
    psi_out.fa.restart
```

### .clstr
```
>Cluster 0
0       1806nt, >X15065.1... at +/98.50%
1       80423nt, >L07835.1... *
>Cluster 1
0       54962nt, >L10351.1... *
>Cluster 2
0       784nt, >V00880.1... at +/100.00%
1       521nt, >V00881.1... at +/99.81%
2       893nt, >X02215.1... at +/96.86%
3       44594nt, >M18818.1... *
4       1604nt, >J00661.1... at +/100.00%
5       2638nt, >J00664.1... at +/99.73%
6       1827nt, >J00659.1... at +/99.45%
.....

idx    Seq_len,>Seq_ID... at <+-Strand>/Seq_identity
有*者为代表序列
单位可为aa/nt
```

### .bak.clstr
```
13604   556nt, >X17276.1... *
14615   437nt, >X51700.1... at +/100.00%
7026    1512nt, >X68321.1... *
3759    2367nt, >X55027.1... *
2311    540nt, >Z12029.1... at +/98.33%
5859    1759nt, >X52700.1... *
5859    1758nt, >X52701.1... at +/95.56%
5859    1758nt, >X52702.1... at +/95.28%
15101   422nt, >X52706.1... *
15101   410nt, >X52703.1... at +/95.12%
15101   422nt, >X52704.1... at +/97.87%
.....

Cluster_ID   Seq_len,>Seq_ID... at <+-Strand>/Seq_identity
有*者为代表序列
单位可为aa/nt
```

### .restart
if program crash, stoped, termitated, you can restart with .restart file
```
1259    0       *       1
1510    0       0.0/6344:660aa/96.87%   1
1521    0       0.0/4860:1387:656aa/95.13%      1
5465    0       0.0/6344:660aa/97.75%   1
5514    0       0.0/6344:660aa/97.6%    1
1349    0       0.0/6343:660aa/96.61%   1
2668    0       0.0/6343:660aa/96.96%   1
401     0       0.0/6344:660aa/97.7%    1
2723    0       0.0/6344:660aa/97.57%   1
3707    0       0.0/6344:660aa/97.53%   1
2395    0       0.0/4059:2190:660aa/96.2%       1
2628    0       0.0/6344:660aa/97.63%   1
3225    0       0.0/6344:660aa/97.48%   1
2762    0       0.0/2942:1967:1246:660aa/93.98% 1
3534    0       0.0/6227:660aa/97.49%   1
1859    0       0.0/6039:426:39aa/95.25%        1
418     1       *       1
5154    2       *       1
3624    3       *       1
4086    4       *       1
```


### Seq files
header是原文件中header
```
>KJX92028.1 hypothetical protein TI39_contig5958g00003 [Zymoseptoria brevis]
......
```


## Tricks
### Incremental clustering
* 往大文件里加新序列
    1. Find new seqs in Additional.fa (cd-hit/-est-2d)
    2. Dereplicat new seqs (cd-hit/-est)
    3. Add dereplicated seqs to all.fa
```
  cd-hit-est-2d -i all.fa -i2 add.fa -o new.fa -c 0.95 -n 10 -M 16000 -T 16
  cd-hit-est -i new.fa -o new_drep.fa -c 0.95 -n 10 -M 16000 -T 16
  cat new_drep.fa >> all.fa
```
### Hierarchical clustering
* 多步迭代运行, clustering via neighbor-joining method, 从而生成层次结构
* 比一步聚类更快、更准确, 可以避免两个非常相似的序列A和B被归于不同的聚类中
```
cd-hit -i nr -o nr80 -c 0.8 -n 5       ## 0.8
cd-hit -i nr80 -o nr60 -c 0.6 -n 4     ## 0.6  
psi-cd-hit.pl -i nr60 -o nr30 -c 0.3   ## 0.3  
clstr_rev.pl nr80.clstr nr60.clstr > nr80-60.clstr 
clstr_rev.pl nr80-60.clstr nr30.clstr > nr80-60-30.clstr
```
可以0.9-0.6-0.3，总之不要一下子降很快

## 参考
https://github.com/weizhongli/cdhit/wiki/3.-User's-Guide  




