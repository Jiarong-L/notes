
用于测试流程的数据源

## SRA

查找文章中SRRxxxxx编号进行下载, 或参考[link](https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/)
### sra-tools + prefetch

下载[sra-tools](https://github.com/ncbi/sra-tools)
```bash
wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.6/sratoolkit.3.0.6-ubuntu64.tar.gz
tar -xzf sratoolkit.3.0.6-ubuntu64.tar.gz
export PATH=$PWD/sratoolkit.3.0.6-ubuntu64/bin:$PATH
```

下载数据
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

### ascp

从[EBI的数据页面](https://www.ebi.ac.uk/ena/browser/view/SRR5874659)中鼠标指向SRR页面的"ftp"获取其ftp地址，随后可ascp下载（```conda install -c hcc aspera-cli -y```安装ascp，安装目录中有```etc/asperaweb_id_dsa.openssh```）

```bash
## PE pattern 1
echo SRR12362016 | while read i; do
x=$(echo $i | cut -b1-6)
y=`echo ${i: -2}`
echo $id
ascp -QT -l 500m -P33001  -i /home/a/miniconda3/envs/bulkatac/etc/asperaweb_id_dsa.openssh \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/0${y}/${i}/${i}_1.fastq.gz \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/0${y}/${i}/${i}_2.fastq.gz ./
done

## PE pattern 2
echo SRR5874659 | while read i; do
x=$(echo $i | cut -b1-6)
y=`echo ${i: -1}`
echo $id
ascp -QT -l 500m -P33001  -i /home/a/miniconda3/envs/bulkatac/etc/asperaweb_id_dsa.openssh \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/00${y}/${i}/${i}_1.fastq.gz \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/00${y}/${i}/${i}_2.fastq.gz ./
done


## SE pattern
echo SRR14209175 | while read i; do
x=$(echo $i | cut -b1-6)
y=`echo ${i: -2}`
echo $id
ascp -v -QT -l 300m -P33001 -k1 -i /home/a/miniconda3/envs/bulkatac/etc/asperaweb_id_dsa.openssh \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/0${y}/${i}/${i}.fastq.gz ./
done
```


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




