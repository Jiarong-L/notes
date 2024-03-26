
用于测试流程的数据源

## SRA
下载[sra-tools](https://github.com/ncbi/sra-tools)
```bash
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.6/sratoolkit.3.0.6-ubuntu64.tar.gz
tar -xzf sratoolkit.3.0.6-ubuntu64.tar.gz
export PATH=$PWD/sratoolkit.3.0.6-ubuntu64/bin:$PATH
```


查找文章中SRRxxxxx编号进行下载, 或参考[link](https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/)
```bash
echo -e "SRR22097888\nSRR3156163\nSRR3157034\nSRR3156160\n" > SraAccList.txt
export HOME=$PWD/SRRtmp/

## prefetch SRR22097888  -X 100000000
less SraAccList.txt | while read dd; do prefetch $dd ; done


## fastq-dump --split-3  --gzip SRR22097888.sra -o SRR22097888
## fastq-dump --split-3  --gzip SRR22097888
less SraAccList.txt | while read dd; do fastq-dump --split-3  --gzip $dd ; done

```
参考: https://blog.csdn.net/hgz2020/article/details/128313178  
SRR22097888: The complete chloroplast genome of Triplophysa bombifrons



## 10X Genomics
[https://www.10xgenomics.com/resources/datasets](https://www.10xgenomics.com/resources/datasets) 可以搜索10X Genomics的各种数据：
Spatial Gene Expression， In Situ Gene Expression， Single Cell Gene Expression Flex， Single Cell Immune Profiling

例如：
```bash
wget http://cf.10xgenomics.com/samples/cell-exp/1.1.0/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz
tar -xzf pbmc3k_filtered_gene_bc_matrices.tar.gz
```


## Generate Fake Reads

自己写的假数据生成脚本。暂未完成。

https://github.com/Jiarong-L/GenReads




