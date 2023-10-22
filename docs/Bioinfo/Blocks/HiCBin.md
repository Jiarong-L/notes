
# [HiCBin](https://github.com/dyxstat/HiCBin)

结合HiC数据与Taxa信息、辅助Binning   

## Install:
**Bug**: 有时候必须在./hicbin.py的安装目录运行```python3 ./hicbin.py```才能成功，直接```hicbin.py```会有路径错误; export path + chmod 777 无用
```bash
git clone https://github.com/dyxstat/HiCBin.git
cd HiCBin
conda env create -f HiCBin_linux_env.yaml 
conda activate HiCBin_env

cp /MY_CONDA/envs/HiCBin_env/lib/libdeflate.so /MY_CONDA/envs/HiCBin_env/lib/libdeflate.so.0
conda install -c conda-forge r-glmmtmb
#conda install -c conda-forge binutils

export PATH="/MY_CONDA/envs/HiCBin_env/bin/:$PATH"
export PATH="/MY_CONDA/envs/HiCBin_env/lib/:$PATH"
export PATH="$PWD:$PATH"
hicbin.py test test/out        ## test hicbin


## for input preparetion:
conda install -c bioconda bwa
conda install -c bioconda bbmap   
conda install -c bioconda metabat2
conda install -c bioconda samtools==1.7
conda deactivate
```

## 准备
* 数据格式参考test/文件夹示例
1. [scaffolds.fasta](./HiCBin/contig_assembly_test.fa) 来自其它软件的组装，需要binning的对象
2. clean.1.fq.gz，clean.2.fq.gz 质控过的HiC数据
3. 生成前置数据:
    * HiC_mapto_Contig.bam: scaffolds.sorted.bam
    * [HiC_mapto_Contig.coverage](./HiCBin/coverage_test.txt)
    * [Contig_Taxa.txt](./HiCBin/contig_tax_test.csv): [TAXAssign](https://github.com/umerijaz/TAXAassign) (需要安装SQL，麻烦)；推荐CAT(Contig Annotation Tool)

```bash
## 1. mapping HiC reads to scaffolds.fasta 
# 为何不用下文bbmap.sam??
bwa index scaffolds.fasta
bwa mem scaffolds.fasta  clean.1.fq.gz  clean.2.fq.gz | samtools view -F 0x904 -bS - | samtools sort -n -@ 20 - > scaffolds.sorted.bam


## 2. bbmap to caculate coverage
bbmap.sh in1=clean.1.fq.gz in2=clean.2.fq.gz ref=scaffolds.fasta  out=bbmap.sam  bamscript=bs.sh
sh bs.sh
jgi_summarize_bam_contig_depths --outputDepth Coverage.txt --pairedContigs pair.txt bbmap_sorted.bam

## 3. Taxonomy Anno for Contigs (NCBI's TAXAssign)
/NCBITools/TAXAassign.sh -c 20 -r 10 -m 98 -q 98 -t 95 -a "60,70,80,95,95,98" -f scaffolds.fasta
```

## 运行

```bash
$DATA_DIR='WHERE_DATA_IS/'
$RES_DIR='WHERE_OUTPUTS_ARE/'


## Binning: $DATA_DIR/BIN
hicbin.py pipeline $DATA_DIR/scaffolds.fasta $DATA_DIR/scaffolds.sorted.bam  $DATA_DIR/Contig_Taxa.txt  $DATA_DIR/Coverage.txt $OUT_DIR
## Checkm
cd $OUT_DIR
checkm lineage_wf -x fa  BIN/  checkm/ -t 16 --pplacer_threads 8 --tab_table -f checm.summary.xls
python3 Contaminated_Bins.py
cd -
## recluster: $DATA_DIR/SUB_BIN
hicbin.py recluster --cover -v $DATA_DIR/scaffolds.fasta $OUT_DIR/Contaminated_BinID.txt $OUT_DIR
## Merge BIN and SUB_BIN: $DATA_DIR/FINAL_BIN
merge_bins.py $OUT_DIR/Contaminated_BinID.txt $OUT_DIR
```
其中 Contaminated_Bins.py 读入'checm.summary.xls'、生成'Contaminated_BinID.txt'：(filter范围自选)
```py
## read in 'checm.summary.xls';Generate 'Contaminated_BinID.txt'
import pandas as pd
df = pd.read_csv('checm.summary.xls',sep='\t')
df = df[df['Completeness']>50]
df = df[df['Contamination']>10]
with open('Contaminated_BinID.txt','w') as f:
    for item in df['Bin Id'].values:
        f.write('{}\n'.format(item))
```
