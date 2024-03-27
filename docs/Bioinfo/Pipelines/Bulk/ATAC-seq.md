

使用Tn5转酶切割染色质的**开放区域**、对这些片段进行**测序**；只需要少量样本(500~50000 cell)；可结合基因表达数据、挖掘开放区域的潜在转录因子结合区域(TFBS)，得到关键的TF作为潜在的疾病的Marker或进行Atlas绘制


* promoter: 接近TSS区域，包含TF结合位点、募集 RNA polymerase
* 如果TF接触 promoter region 时结合了 enhancer，则基因的表达量升高；如果结合了 silencer，则基因的表达量降低
* enhancer 最远距离 promoter region 上下游1Mb


## Pipeline

与 [ChipSeq 流程](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3431496/)有许多重合：mapping后callPeaks，然后idr合并重复样本重合的peaks作为这个样本最终的peaks。Peaks实际上是chr上的一段区间，可以提取这个区间的序列进行motif富集/denovo预测，然后选取motif基序扫描基因组得到潜在的TFBS，Footprinting验证其是否已经结合TF。同时也可注释Peak所在区域，提取Promoter对应的基因进行GO/KEGG等分析。也可查看不同样本间结合位点的差异性（DiffBind）



| Task | Tools | 说明 |
| -- | -- | -- |
| Reads QC + Trim | FastQC + Trimmomatic | -- |
| Mapping to Ref | BWA/Bowtie2 | 得到 BAM file |
| Pre-analysis | Samtools | - Mark PCR Duplicate<br>- Filter Insert Size<br>- Filter off mitochondria reads |
| Peak Calling | MACS2 ```--shift -75(ReadsLen)``` (断点才是Peak中心) | 已经初步过滤  |
| View Peak | IGV | 提供bam和gff，对照Peak Calling结果查看peak是否合理 |
| Peak QC | samtools + ChIPQC + phantompeakqualtools + Greenscreen | 查看PeakCalling的大致的情况，确定数据是否合理<br> - InsertSize, FRiP, ...<br> - [ENCODE Blacklist](https://www.encodeproject.org/search/?searchTerm=exclusion+list): 去除因富含GC/重复片段而总是高信号的区域，有可能过度严格<br> - Greenscreen 去除假阳性Peaks  |
| Merge Replicates | IDR | 寻找、合并重复样本间一致性的peaks |
| ------- | Normalization + Analysis | ------- |
| Diff Peak | DiffBind | 鉴定两个样本间差异结合位点，输入BED file |
| Peak Annotation | ChIPseeker | Peak位于promoter/gene/..处；如果Bioconductor没有合适的TxDb，则需要使用GenomicFeatures包```makeTxDbFromxxx```制作 |
| Motif | MEME（All） <br> homer（denovo） <br> [chromvar](https://github.com/GreenleafLab/chromVAR)（Enrich） <br> TFBSTools（Scan） <br> ggmotif_plot（画图）  | - deNovo: 根据Peak序列从头预测Motif基序 <br>- Enrichment: 扫描Motif库（例如JASPAR数据库），获取本样品中富含的Motif基序 <br>-Scan: 已知晓Motif，扫描基因组寻找潜在TFBS |
| Footprinting | HINT-ATAC | 验证潜在TFBS（寻找已结合TF的TFBS）：如果某一开放区域已经结合TF，则此区域不会被测得，表现为peak中间有凹陷 |
| GO, Pathway ... | -- | -- |


注：可视化推荐用IGV。[deepTools - bamCoverage](https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html)可以将bam转换为BigWig.bw文件，作为IGV或UCSC的输入；deepTools本身也可以画展示TSS附近的coverage的图（UCSC下载refTSS），例如[plotProfile](https://deeptools.readthedocs.io/en/develop/content/tools/plotProfile.html)、plotHeatmap

```bash
## pip install deeptools
## 支持--blackListFileName
## 参考 https://cloud.tencent.com/developer/article/1842761
samtools index reads.bam
bamCoverage --normalizineUsing -b reads.bam -o coverage.bw


## UCSC 下载 ref.TSS.bed
## 参考 https://www.jianshu.com/p/d6cb795af22a
## 参考 https://y-bai.github.io/posts/omics-find-tss-for-genes/
## 然后 computeMatrix reference-point --referencePoint TSS -R refTSS.bed -S my.bw   ...
```


## Run


### SetupDir
```bash
mkdir ref
mkdir raw
mkdir trimmed
mkdir mapped
mkdir peak   # *__peaks.narrowPeak
```

### Prepare Data
```bash
cd ref
wget http://ftp.ebi.ac.uk/ensemblgenomes/pub/release-51/plants/fasta/arabidopsis_thaliana/dna/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz
wget http://ftp.ebi.ac.uk/ensemblgenomes/pub/release-51/plants/gff3/arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.51.gff3.gz
gunzip *.gz
# sed -i 's/>/>chr/g' Arabidopsis_thaliana.TAIR10.dna.toplevel.fa
mv Arabidopsis_thaliana.TAIR10.dna.toplevel.fa Arabidopsis_thaliana.fa
mv Arabidopsis_thaliana.TAIR10.51.gff3  Arabidopsis_thaliana.gff3
bwa index Arabidopsis_thaliana.fa
cd ..

cd raw
echo "SRR5874658\nSRR5874659\n" > SraAccList.txt
cat SraAccList.txt | while read i; do
x=$(echo $i | cut -b1-6)
y=`echo ${i: -1}`
echo $id
ascp -QT -l 500m -P33001  -i /home/a/miniconda3/envs/bulkatac/etc/asperaweb_id_dsa.openssh \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/00${y}/${i}/${i}_1.fastq.gz \
era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${x}/00${y}/${i}/${i}_2.fastq.gz ./
done
cd ..

cd raw     ## extract a small portion of it
cat SraAccList.txt | while read i; do
less  ${i}_1.fastq.gz|head -500000 >  t${i}_1.fastq
less  ${i}_2.fastq.gz|head -500000 >  t${i}_2.fastq
less  ${i}_1.fastq.gz|head -50000 >  c${i}_1.fastq
less  ${i}_2.fastq.gz|head -50000 >  c${i}_2.fastq
done
gzip *.fastq
```

### Call Peak
暂且不用对照组
```bash
echo -e "SampleID\tTissue\tFactor\tCondition\tReplicate\tbamReads\tControlID\tbamControl\tPeaks\tPeakCaller" > peak/Sheet.csv

for dd in SRR5874658 SRR5874659 ; do
SID=t${dd}
# CID=c${dd}
# echo -e "${SID}\tNA\tNA\tNA\t1\t../mapped/${SID}.rmdup.sorted.bam\tControlID\t../mapped/${CID}.rmdup.sorted.bam\t${SID}_out/${SID}_peaks.narrowPeak\tnarrow" >> peak/Sheet.csv
echo -e "${SID}\tNA\tNA\tNA\t1\t../mapped/${SID}.rmdup.sorted.bam\tControlID\tNA\t${SID}_out/${SID}_peaks.narrowPeak\tnarrow" >> peak/Sheet.csv
sh mapping.sh ${SID} Arabidopsis_thaliana.fa 
# sh mapping.sh ${CID} Arabidopsis_thaliana.fa 
# sh callpeakC.sh  ${SID}  ${CID}  135000000
sh callpeak.sh  ${SID}  135000000
done
cd peak
```

然后导入IGV视情况、或根据 */*_peaks.xls 里的 -log10(pvalue) 等消除不合格的peaks（直接从MACS结果的.narrowPeak/.bed文件中提取感兴趣的peaks？？）




### Peak QC

QC只是展示了PeakCalling的大致的情况（类似FastQC），并没有提示某个peak


一些快速QC小技巧
```bash
## insertsize List
samtools view ../mapped/tSRR5874658.rmdup.sorted.bam | cut -f 9 | less

## RIP%/FRiP = reads_in_peak/all_reads
bedtools intersect -a ../mapped/tSRR5874658.bed  -b tSRR5874658_out/tSRR5874658_peaks.narrowPeak | wc -l
wc -l ../mapped/tSRR5874658.bed
```


ChIPQC：似乎已经包含了DiffBind
```R
library(ChIPQC)
## browseVignettes("ChIPQC")
samples <- read.csv('Sheet.csv',sep='\t')
chipObj <- ChIPQC(samples, annotation = NULL) 
ChIPQCreport(chipObj, reportName="ChIP QC report", reportFolder="ChIPQCreport")

# 如果使用SampleList（它也支持单个），则至少有2个sample。否则报错（另外留下的peak太少有可能报错？）   
# 内置的annotation支持blacklist，不过暂时没有找到自定义anno的方法。。
```

### Merge Replicates

找到重复实验的重合peaks，合并它们。

粗暴Merge:
```bash
bedtools intersect -a tSRR5874658_out/tSRR5874658_peaks.narrowPeak -b tSRR5874659_out/tSRR5874659_peaks.narrowPeak -wo > overlaps.bed
## if A B overlaps, return -wo
## : Write the original A and B entries plus the number of base pairs of overlap between the two features
```


IDR:  标准流程
```bash
## 需要先排序
sort -k8,8nr tSRR5874658_out/tSRR5874658_peaks.narrowPeak > s.tSRR5874658_peaks.narrowPeak
sort -k8,8nr tSRR5874659_out/tSRR5874659_peaks.narrowPeak > s.tSRR5874659_peaks.narrowPeak

## 
## WITHOUT --peak-list 
## 如果 SampleA_peak1 与 SampleB_peak9 有overlap，则把它们merge在一起；--use-nonoverlapping-peaks 才能显示无overlap的peaks
idr --samples  s.tSRR5874658_peaks.narrowPeak  s.tSRR5874659_peaks.narrowPeak  --plot


## WITH --peak-list  一组自定义的peak范围
## 从各样本中选取与peaklist中OraclPeak重合者，如果多个样本Peak同时match一个OraclePeak，则依次选择：
## 1. 与summit最近  2. largest overlap 3. highest score
idr --samples  s.tSRR5874658_peaks.narrowPeak  s.tSRR5874659_peaks.narrowPeak  --peak-list  xxx???


## idrValues.txt format
## https://github.com/nboley/idr/blob/master/README.md
```




### Peak Annotation

ChIPseeker covplot 也可以作图
```R
library("ChIPseeker")  
library("GenomicFeatures")

ara_TxDb <- makeTxDbFromGFF("../ref/Arabidopsis_thaliana.gff3")
peaks <-readPeakFile("tSRR5874658_out/tSRR5874658_peaks.narrowPeak")
seqlevels(peaks)  ## chr名称应该与gff中一致！

## Anno
peaksAnno <- annotatePeak(peaks, tssRegion=c(-3000,3000),TxDb=ara_TxDb)
peaksAnno_df  <- as.data.frame(peaksAnno)


## Plot1
covplot(peaks,weightCol=5)
## Plot2:  peakHeatmap(peaks, TxDb=ara_TxDb, upstream=1500, downstream=1500, color="blue")
promoter <- getPromoters(TxDb=ara_TxDb, upstream=1500, downstream=1500)
tagMatrix <- getTagMatrix(peaks, windows=promoter)
tagHeatmap(tagMatrix, xlim=c(-1500, 1500), color="green")
## Plot3
# files <- c("tSRR5874658_out/tSRR5874658_peaks.narrowPeak","tSRR5874659_out/tSRR5874659_peaks.narrowPeak")
# names(files_list) <- c("tSRR5874658","tSRR5874659")
# tagMatrixList <- lapply(files_list, getTagMatrix, windows=promoter)
# plotAvgProf(tagMatrixList, xlim=c(-1000, 1000), conf=0.95,resample=500, facet="row")
```

### Motif （TBA）

homer：由于测试数据太少，没有结果
```bash
awk '{print $4"\t"$1"\t"$2"\t"$3"\t+"}' tSRR5874658_out/tSRR5874658_peaks.narrowPeak > testhomer.bed
findMotifsGenome.pl testhomer.bed ../ref/Arabidopsis_thaliana.fa homer_out
```

chromVAR：peaks此处使用单个试验的，其实也可以是merged（自行从idrValues.txt里提取？？）
```R
library(chromVAR)
library(TFBSTools)
library(ggmotif)   ## https://github.com/AliciaSchep/ggmotif


peaks <- readNarrowpeaks("tSRR5874658_out/tSRR5874658_peaks.narrowPeak")  
bamfiles <- c("../mapped/tSRR5874658.rmdup.sorted.bam","../mapped/tSRR5874659.rmdup.sorted.bam")

fragment_counts <- getCounts(bamfiles, peaks, 
                              paired =  TRUE, 
                              by_rg = TRUE, 
                              format = "bam")

motifs <- getJasparMotifs()

## FAIL TBA
```
























## Bash Files
### mapping.sh
```bash
SID=$1
REF=$2
echo "Processing ${SID}   $REF  $GSIZE at $PWD"

cd trimmed
trimmomatic PE -phred33  ../raw/${SID}_1.fastq.gz ../raw/${SID}_2.fastq.gz  ${SID}_R1.trimmed.fq.gz ${SID}_R1.U.fq.gz  ${SID}_R2.trimmed.fq.gz ${SID}_R2.U.fq.gz SLIDINGWINDOW:4:15 MINLEN:75   -summary ${SID}.summary.txt  -trimlog ${SID}.log.txt  -threads 64  -quiet
fastqc ${SID}_R1.trimmed.fq.gz -o ./
fastqc ${SID}_R2.trimmed.fq.gz -o ./
cd ..


cd mapped
bwa mem ../ref/$REF ../trimmed/${SID}_R1.trimmed.fq.gz ../trimmed/${SID}_R2.trimmed.fq.gz | grep -v Mt | samtools view -b - | samtools sort -  > ${SID}.sorted.bam
ulimit -n 8000 
sambamba markdup -r ${SID}.sorted.bam ${SID}.rmdup.bam --tmpdir=./ -t 2
bedtools bamtobed -i ${SID}.rmdup.bam  > ${SID}.bed 
samtools sort ${SID}.rmdup.bam  > ${SID}.rmdup.sorted.bam
samtools index ${SID}.rmdup.sorted.bam
cd ..

## sh mapping.sh ct Arabidopsis_thaliana.TAIR10.dna.toplevel.fa 
```

### callpeak

callpeak.sh (no control)
```bash
SID=$1
GSIZE=$2
echo "Processing ${SID}    $GSIZE at $PWD"

cd peak
macs2 callpeak -t ../mapped/${SID}.rmdup.sorted.bam -n ${SID} --shift -100 --extsize 200 --nomodel -B --SPMR -g $GSIZE --outdir ${SID}_out 2> ${SID}.macs2.log
cd ..

## sh callpeak.sh SID GSIZE
```


callpeakC.sh (with control)
```bash
SID=$1
CID=$2
GSIZE=$3
echo "Processing ${SID} ${CID} $GSIZE  at $PWD"

cd peak
macs2 callpeak -c ../mapped/${CID}.rmdup.sorted.bam -t ../mapped/${SID}.rmdup.sorted.bam -n ${SID} --shift -100 --extsize 200 --nomodel -B --SPMR -g $GSIZE --outdir ${SID}_out 2> ${SID}.macs2.log
cd ..

## sh callpeakC.sh SID CID  GSIZE
```

## Install Env
```bash
conda create --name idr  ## py11
conda activate idr
conda install python=3.6 -y
conda install -c bioconda idr -y
conda deactivate

conda create --name bulkatac
conda activate bulkatac
conda install -c hcc aspera-cli -y
conda install -c bioconda trimmomatic -y
conda install -c bioconda fastqc -y 
conda install conda-forge::libgcc-ng -y
conda install -c conda-forge ncurses -y
conda install -c bioconda samtools=1.18 --force-reinstall -y
conda install -c bioconda bwa -y
conda install -c bioconda sambamba -y
conda install -c bioconda bedtools
conda install -c bioconda homer -y

sudo apt install macs

wget https://github.com/kundajelab/idr/archive/2.0.4.zip
unzip 2.0.4.zip
cd idr-2.0.4
conda install anaconda::numpy -y 
conda install conda-forge::setuptools -y
pip install  matplotlib  dev
python3 setup.py install




if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("ChIPQC")
devtools::install_github("YuLab-SMU/ggtree")
BiocManager::install("ChIPseeker")
BiocManager::install("chromVAR")  ## sudo apt install libgsl-dev 
BiocManager::install("TFBSTools")
devtools::install_github("AliciaSchep/ggmotif")
```


## 参考

https://zhuanlan.zhihu.com/p/415718382（拟南芥）  

https://www.plob.org/article/24683.html（人 系列教程）

https://cloud.tencent.com/developer/article/1360799（人）

https://hbctraining.github.io/Intro-to-ChIPseq/lessons/05_peak_calling_macs.html（人）

https://zhuanlan.zhihu.com/p/590862767（概念）

https://zhuanlan.zhihu.com/p/471350610（motif-在线集合）

https://www.jianshu.com/p/6aba8f1dea56（footprinting）

https://cloud.tencent.com/developer/article/1624517（esATAC pipeline）

https://zhuanlan.zhihu.com/p/57516178（chromVAR---参考数据库或denovo，找到富含的Motif）

https://www.jianshu.com/p/c65a1cb35d50（TFBSTools---已知Motif扫描，基因组）

https://meme-suite.org/meme/（MEME---denovo/enrichment/scanGenome）

https://zhuanlan.zhihu.com/p/602992278（Greenscreen）


