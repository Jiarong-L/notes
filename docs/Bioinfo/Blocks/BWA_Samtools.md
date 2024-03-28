
BWA: mapping low-divergent sequences against a large reference genome

ATAC、RNA 的教程常常用 Bowtie2 进行mapping，不过其实 BWA 可以搞定一切；此外极短数据仍可以尝试 Bowtie1

Samtools是一个用来处理sam/bam文件的工具

## Install
Conda：samtools需要强制控制版本(不然也许会是1.9版本);此外，源的设置不对可能会导致lib报错
```bash
conda create --name map
conda activate map

conda install -c bioconda bwa       
conda install -c bioconda samtools=1.18 --force-reinstall
conda install -c bioconda bowtie
conda install -c bioconda bowtie2 

conda install -c bioconda sambamba
```
Ubuntu直接装也行，不过samtools需要手动安装一些依赖：
```
sudo apt install bwa      
sudo apt install samtools  
sudo apt install bowtie
sudo apt install bowtie2
```

## Use
可以在Mapping时设置限制，也可以比对完成后再进行筛选；各软件详细参数请至官方文档查询。    
**reads输入可以是.fq也可以是.fq.gz**
### BWA
一般使用MEM即可；生成sam文件
```bash
bwa index ref.fa  ## 建立索引 ref.fa.amb ann bwt pac sa

bwa mem ref.fa R1.fq R2.fq > aln.sam  ## PE
## bwa mem ref.fa R1.fq > aln.sam     ## SE
```


### Bowtie
bowtie1 擅长短片段的匹配(25-50bp)；Docs见：[What is Bowtie](https://bowtie-bio.sourceforge.net/manual.shtml#what-is-bowtie)
```bash
bowtie-build ref.fa idxPerfix
bowtie -x idxPerfix -1 R1.fq -2 R2.fq -S aln.PE.sam 
```
* -n alignment mode: (default) 限制seed中mismatches
* -v alignment mode: 限制Alignment中mismatches
* 案例 - miRNAseq只需要0错配且最优的比对：```-n 0 -m1 --best --strata```


### Bowtie2
Bowtie2 擅长匹配比 bowtie 稍长些的序列的序列(>50bp)；它与bowtie1完全不同，Docs见：[How is Bowtie 2 different from Bowtie 1?](https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#how-is-bowtie-2-different-from-bowtie-1)
```bash
bowtie2-build ref.fa idxPerfix

bowtie2 -x idxPerfix -1 R1.fq -2 R2.fq -S aln.PE.sam 
bowtie2 -x idxPerfix -U R1.fq          -S aln.SE.sam
```
注：可加 -b aln.PE.bam 但很容易报错



### Samtools


#### SAM/BAM转换   
当输入的SAM的开头有 @SQ lines 时:
```bash
samtools view -b aln.sam > aln.bam
```
否则需要先对 ref.fasta 进行 faidx：
```bash
samtools faidx ref.fa  ## 建立索引 ref.fa.fai
samtools view -b aln.sam > aln.bam
```

view常用： 
```
samtools view -b aln.sam > aln.bam
samtools view    aln.bam > aln.sam
samtools view -c aln.sam | less     ## count of matching records
```



#### 常用功能

```bash
samtools sort aln.bam  > sorted.bam  ## sort by pos
samtools index sorted.bam  ## 生成索引.bai，必须先sort

samtools merge [out.bam][in1.bam][in2.bam][in3.bam] ## merge 3 files

samtools fastq aln.bam > hasmapped.ref.fa
samtools depth sorted.bam > depth.tab.txt
samtools flagstat aln.bam  | less          ## 统计各flag
```


#### Filter Expr
此外，还可以使用[FILTER_EXPRESSIONS](https://www.htslib.org/doc/samtools.html#FILTER_EXPRESSIONS)简单filter；**此功能仅1.12以上版本支持**

```bash
samtools view -e 'mapq >= 30' aln.bam | less

samtools view --input-fmt-option 'filter=(mapq >= 30)' aln.bam | less
```



#### Duplicate Marking
```bash
samtools collate -O aln.bam > collate.bam   ## sort by name
samtools fixmate collate.bam - > fixmate.bam ## repairs PE mate info；需要先collate
samtools sort fixmate.bam > fixmate.sorted.bam
samtools markdup fixmate.sorted.bam - > rmdup.bam
```

写成pipe格式：
```bash
## PE reads
samtools collate -O aln.bam | samtools fixmate - - | samtools sort - | samtools markdup - rmdup.bam

## SE reads
samtools sort aln.bam | samtools markdup - rmdup.bam
```

tips: 此外还有picard MarkDuplicates等；个人PC内存较小，可以使用[sambamba](http://lomereiter.github.io/sambamba/docs/sambamba-markdup.html):
```bash
ulimit -n 8000    ## 限制同一时间最多可开启的文件数
sambamba markdup -r aln.bam rmdup.bam --tmpdir=./ -t 2
```



## 参考
BWA：https://bio-bwa.sourceforge.net/   
BWA使用手册：https://bio-bwa.sourceforge.net/bwa.shtml  
samtools：https://www.htslib.org/doc/samtools.html#flags  
Bowtie：https://bowtie-bio.sourceforge.net/manual.shtml  
Bowtie2：https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml   
