
耐药基因(ARGs)数据库：[背景参考](https://zhuanlan.zhihu.com/p/608186172)，

其它：[resfinder](https://pubmed.ncbi.nlm.nih.gov/32780112/)似乎也常见，它支持识别点突变
   

## CARD

[CARD](https://card.mcmaster.ca/browse)包括已知耐药基因及相关药物，同时提供基于NCBI中413种病原体及其变体计算的[患病率（Prevalence）和预测的抗性组（Resistomes）](https://card.mcmaster.ca/resistomes)；于此处下载[DOWNLOAD](https://card.mcmaster.ca/download/)：

```bash
wget -c https://card.mcmaster.ca/download/5/ontology-v3.2.9.tar.bz2           ## Ontology文件：aro.obo
wget -c https://card.mcmaster.ca/download/0/broadstreet-v3.2.9.tar.bz2        ## CARD数据库：card.json
wget -c https://card.mcmaster.ca/download/6/prevalence-v4.0.2.tar.bz2         ## Resistomes：教程中称为wildcard/DB.gz
tar jxvf ontology-v3.2.9.tar.bz2
tar jxvf broadstreet-v3.2.9.tar.bz2
tar jxvf prevalence-v4.0.2.tar.bz2
mkdir wildcard
mv *.gz wildcard
gunzip wildcard/*.gz


## 众多FASTA文件中，'homolog model' 包含耐药基因，但不包括因突变/过表达/缺失而耐药的基因（储存于'variant/overexpression/knockout'中）
## 'rRNA'只有核酸，没有protein
```

推荐blast/blastp ```CARD/*homolog_model.fasta``` 获取 ARO（也许可以忽略prevalence），对照 ```aro.obo / aro_index.tsv``` 获取注释内容；

也可以使用官方推荐的 [rgi](https://github.com/arpcard/rgi/blob/master/docs/rgi_load.rst)：但我用Conda安装 Version 3.2.1 似乎不支持如下 options

| rgi options | 说明 | ```-t INTYPE``` |
| -- | -- | -- |
| [load](https://github.com/arpcard/rgi/blob/master/docs/rgi_load.rst) | 加载数据库 | -- |
| [main](https://github.com/arpcard/rgi/blob/master/docs/rgi_main.rst) | DIAMOND/BLAST对输入序列进行注释 | ```contig(default)/protein``` |
| [bwt](https://github.com/arpcard/rgi/blob/master/docs/rgi_bwt.rst) | bwa/bowtie2/kma对宏基因组reads进行注释 | ```read``` |
| [kmer_build / kmer_query](https://github.com/arpcard/rgi/blob/master/docs/rgi_kmer.rst) | -- | -- |
| -- | 可以cat所有nt.fasta成为教程中的all.fasta | 若是```contig```则会先通过prodigal预测CDS |


## SARG

作者推荐使用基于SARG构建的[ARGs-OAP](https://github.com/xinehc/ARGs_OAP)进行宏基因组注释: **输入为PE reads**
```bash
                                                           ## PE reads 放置于input/
args_oap stage_one -i input/ -o output/ -f fq -t 8         ## output/metadata.txt 展示各样本中 nRead/n16S/nCell
args_oap stage_two -i output/ -t 8                         ## 3种丰度定量单位的结果，每一列为一个样本


ARGs-OAP提供自定义的丰度定量单位：                            ## https://zhuanlan.zhihu.com/p/651920861    https://doi.org/10.1093/bioinformatics/bty053
- ppm = ARG_reads * 1e6 / All_reads   
- copies of ARG per copy of 16S rRNA     (一般一个单拷贝细胞有一个16S rRNA copy??)
- copies of ARG per prokaryote’s cell
```


SARG整合了ARDB和CARD，它的3级 ```type/subtype/gene``` 可以对应ARO（见SARG.2.2.fasta header），不过如果需要从CARD转向SARG注释，需要先人工整理对照关系。


也可以单独使用DB对CDS进行注释，但目前只有[SARG-S可自行下载](https://smile.hku.hk/ARGs/Indexing/download)，SARG-E/L/H只能联系作者索取；只能使用 ARGs-OAP Ublastx_stageone 自带的DB：

```bash
## https://github.com/biofuture/Ublastx_stageone
wget https://smile.hku.hk/SARGs/static/images/Ublastx_stageone2.3.tar.gz
tar -xzf Ublastx_stageone2.3.tar.gz

blastp -db Ublastx_stageone2.3/DB/SARG.2.2.fasta -query test.faa -out sarg.m8 -max_target_seqs 5 -evalue 1e-5 -outfmt 6 -num_threads 8 -task blastp-fast
```








