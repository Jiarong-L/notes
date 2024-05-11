

[Homologous Genes](https://link.springer.com/referenceworkentry/10.1007/978-3-642-27833-4_1724-3) 指来源于共同祖先的相似序列，包括 [orthologs](https://link.springer.com/referenceworkentry/10.1007/978-3-642-27833-4_1731-3), [paralogs](https://link.springer.com/referenceworkentry/10.1007/978-3-642-27833-4_1732-3), Xenologs。

```
           Ancester
            /    \     (Gene Duplication)
           A1    A2                                Paralogs: SpeX(A1--A2)
(HGT)      /      \    (Speciation)               Orthologs: (SpeX--SpeY)A1
A1,A2   A1,A2   A1,A2                              Xenologs: (SpeX--SpeZ)A1   跨度巨大的物种间水平基因转移 (e.g. 病毒侵染)
SpeZ    SpeX    SpeY
```


[Protein Family](https://www.ebi.ac.uk/training/online/courses/protein-classification-intro-ebi-resources/protein-classification/what-are-protein-families/) is a group of proteins that share a common evolutionary origin.


**获取基因家族的方式**有2种：(预测CDS后，or工具内置Prodigal)

1. [OrthoFinder](../Blocks/OrthoFinder.md)/OrthoMCL 建 Species Tree & Gene Tree
2. 比对数据库，最基础：
    - [Pfam](http://pfam.xfam.org/): A large collection of protein families & ID-mapping to PDB.
    - [COG/KOG](https://ftp.ncbi.nih.gov/pub/COG/): Cluster of Orthologous Groups of proteins (**prokaryotic**-COG/**eukaryotic complete genomes**-KOG)


**注释基因家族的的用途**：

1. 对未知序列进行功能注释（因此数据库一般也提供 ID-mapping to GO）
2. 对家族内基因进行MSA，确定保守位点
3. 基因家族的扩张和收缩，分析进化压力



## InterPro/Pfam

目前 Pfam 在 InterPro 处更新，[InterProScan](https://www.ebi.ac.uk/interpro/download/InterProScan/) 可实现蛋白家族、结构、功能等多个数据库的注释。[使用手册](https://interproscan-docs.readthedocs.io/en/latest/HowToRun.html)

```bash
wget http://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.67-99.0/interproscan-5.67-99.0-64-bit.tar.gz
tar -pxvzf interproscan-5.67-99.0-*-bit.tar.gz

./interproscan.sh -appl SFLD,Pfam -i input_protein.faa -f tsv -dp
```


也可以：下载 Pfam-A.hmm 后自行注释
```bash
## https://www.ebi.ac.uk/interpro/download/Pfam/
hmmpress Pfam-A.hmm     ## Index DB
hmmscan -o out.txt --tblout out.tbl --noali -E 1e-5 Pfam-A.hmm input_protein.faa
```



## EggNOG

EggNOG 对NCBI的COG数据库进行拓展，并且提供了不同分类水平的 Orthogonal Group；且可以区分 paralogs 与 orthologs（？？）；不过**更新较慢**


使用 [eggNOG-mapper](https://github.com/eggnogdb/eggnog-mapper) 下载目标taxa的各种DB（```-P -M -H``` 对应 Pfam MMseqs2 HMMER）、进行注释；输入类型可选 ```--itype {CDS,proteins,genome,metagenome}```

```
git clone https://github.com/eggnogdb/eggnog-mapper
cd eggnog-mapper

mkdir -p eggnogDB
python download_eggnog_data.py -H -d 2 --dbname 'Bac' --data_dir eggnogDB      ## -d taxid   (then select y or n) 


python emapper.py -m hmmer -i input_protein.faa --itype proteins   -o outperfix   -d Bac    ## To be Check!!!
```

注：下载步骤中的 main annotation DB (eggnog.db.gz)、taxa DB (eggnog.taxa.tar.gz) 亦可从 [emapperdb FTP](http://eggnog6.embl.de/download/emapperdb-5.0.2/) 自行获取、解压、放入 ```eggnogDB/```；相关 taxid 的 ```<taxid>_hmms.tar.gz``` 文件也可以从 [eggNOG FTP - per_tax_level](http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/)获取、放入 ```eggnogDB/hmmer/Bac```；但是，需要注意相应版本


