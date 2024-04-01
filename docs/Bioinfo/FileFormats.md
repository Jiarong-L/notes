
生物信息常见文件格式


## BAM/[SAM](https://samtools.github.io/hts-specs/SAMv1.pdf)

是常见的比对结果文件；BAM是SAM的二进制格式（且丢失开头的@SQ lines），可以使用 ```samtools view``` 相互转换它们；

| SAM header | 空格或tab分隔 | -- |
| -- | -- | -- |
| @HD | ```VN:version```<br>```SO:unknown/unsorted/queryname/coordinate``` | samtools排序后不能自动更新SO值，picard可以? |
| @SQ | ```SN:contigName```<br>```LN:contigLen``` | reference 的 contigs，should be in karyotypic order |
| @RG | ```ID:SampleID```<br>```SM:SampleName```<br>```LB:Library```测序仪<br>```PU:Illumina PL:Miseq```平台 | ```bwa mem -R```加上Read Group信息（1个样本的多个library整合为一个RG？） |
| @PG | ```ID:bwa  PN:bwa  VN:0.7.17-r1188 CL:bwa mem ref.fa R1.fq R2.fq``` | mapping软件信息 |


mandatory fields 每一列依次为：
```
1   QNAME      query read name
2   FLAG       数值表示比对类型，例如 1=PAIRED
3   RNAME      ref contig name；'*' 表示没有map上
4   POS        Alignment的起始位置，0表示没有map上
5   MAPQ       Mapping Quality
6   CIGAR      比对结果信息
7   RNEXT      (PE 测序专属) query R2 比对上的 ref片段；'='表示map到同一片段 ，'*' 表示没有map上
8   PNEXT      (PE 测序专属)query R2 Alignment的起始位置，0表示没有map上
9   TLEN       (PE 测序专属)插入序列长度；+/-表示R1R2的顺序
10  SEQ        序列，若比对在-链则显示反向互补序列
11  QUAL       fastq quality
    ...        Optional fields，/tab分隔
```

[FLAG](https://broadinstitute.github.io/picard/explain-flags.html): Reads info
```
    read paired (1)
    read mapped in proper pair (2)
    read unmapped (4)
    mate unmapped (8)
    read reverse strand (10)
    mate reverse strand (20)
    first in pair (40)
    second in pair (80)
    not primary alignment (100)
    read fails platform/vendor quality checks (200)
    read is PCR or optical duplicate (400)
    supplementary alignment (800)

如果全部符合，则加上对应的分值(1)+(2)+(4)+...+(800)=4095
```

CIGAR: Mapping status
```
M/I/D = match_mismatch/insertion/deletion
S     = spliced
P     = 缺口
I     = 插入
....

3S6M1P1I4M 依次为：3bp被剪去，6bp match，1bp缺口，1bp插入，4bp match
```


SAM示例：
```
@SQ     SN:X17276.1     LN:556
@SQ     SN:X51700.1     LN:437
@SQ     SN:X68321.1     LN:1512
@SQ     SN:X55027.1     LN:2367
@SQ     SN:Z12029.1     LN:540
@SQ     SN:X52700.1     LN:1759
@SQ     SN:X52701.1     LN:1758
......
@PG     ID:bwa  PN:bwa  VN:0.7.17-r1188 CL:bwa mem ref.fa R1.fq R2.fq
SRR22097888.1   77      *       0       0       *       *       0       0       CCAACATTCAATTTTGAAACATTAGTTAATCAATCATATCCTCTGGCATTAGAAATAATATTCTATATTGGATTTTTTATTGCTTTTGCTGTCAAATTACCGATTATTCCTTTACATACATGGTTACCGGATACCCATGGAGAAGCACAT  FFFGGGGFGGGFGGGFDFFFGDGCFGGGFEGEFDGGFFGGGGFGFGFGFGGFGGFFGGDGGG=GGEGFGEFDFGGGGGDEGFEGGFGGFGGFFFGFGFFGGGFFGGFGFGGGGFGGDGGEFGGFGEGGGFGGGGGGGAGGGGFFGGGGG;  AS:i:0  XS:i:0
...
SRR22097888.4   97      X66414.1        5       60      118S32M =       130     212     AGAATTTGAATTGATGTCTTTTCATTGTTTTACTTCCTCCTAAATTGTATTTATTGATTTATCCTAAAGATTTCATTTCAATAGGAATTTGGTTATTCACCATGCACGAGGATCCCCGCTAAGCATCCATGGCTGAATGGTTAAAGCGCC       FFEFGFFECGFFDDF:FFGFFFD<EGFEFEG3FFFFFFEGF6FFCFBDGFEF>FFFEFFG>E<EGE:F-CFFFGGFFGFEFEFAFEDEFFFAAF+FGFCGGF<GFFFF0F<CFEFFG7GBB=FFF?BGF/B5DFF/BF<F8E-FE6F+AF       NM:i:0  MD:Z:32 MC:Z:6M3D78M66S AS:i:32 XS:i:0
SRR22097888.4   145     X66414.1        130     54      6M3D78M66S      =       5       -212    ATGGAATCTCATCATCAATACCAAAGGAATTGATGTGGTATATTCATATCATAACATATTAACAGTAAGAACTAGCATTCTTATCATAATCATATCTCATATCATATAATTCATAATCGTATCTCATATCATAGAATTCATAATCGTATC       +E/A)3;-C99C86)7(=-2C;9E5A7+>F@8@6D>FEF?E;9EEA?2BE85DEE8E8@FB=EEDEDFFBDEDF?<;;DDEAEE?CFCF@BFEEBAAF9FF>FF>EF==FDFFFDF=;EE9<D?EFCEDDAFF-EDCEFEFF6F?@F;?F       NM:i:9  MD:Z:6^TCT10T4A0T2C6G26G24      MC:Z:118S32M    AS:i:48 XS:i:0
```



## GTF/GFF3

常见的基因组注释文件，一般以```#注释行```开头；GTF/GFF3可以用Cufflinks ```gffread``` 或 [AGAT](https://agat.readthedocs.io/en/latest/gff_to_gtf.html)相互转换


| -- | col | -- | GTF | GFF3 |
| -- | -- | -- | ---- | -- |
| 1 | seqid        | ContigID 必须与FASTA/ASN.1中的一致 | -- | -- |    
| 2 | source       | 注释来源 ```./DB/software``` | -- | -- |   
| 3 | Feature type | [Sequence Ontology](http://www.sequenceontology.org/): term/SO_Accession 可通过[MISO Sequence Ontology Browser](http://sequenceontology.org/browser/obob.cgi)查询 | term | term/SO_Accession_Number | 
| 4/5 | start/end  | Position on Contig, starts at 1；start<=end | -- | circularGenome中end在前，则令```end=end+ContigLen``` | 
| 6 | score        | ```./e-value/p-value```: degree of confidence | -- | -- |   
| 7 | strand       | ```+/-/./?``` for 5'->3'/3'->5'/undetermined/unknown strand | -- | -- |  
| 8 | frame  | ```0/1/2```: coden starts from CDS 5' 1st/2nd/3st nt；若不是CDS则```.``` | -- | -- |  
| 9 | attributes   | -- | -- | -- |      


[**GTF Feature types**](https://agat.readthedocs.io/en/latest/gff_to_gtf.html#feature-types-in-gtf-versions)主要包括: ```gene, transcript, exon, CDS, Selenocysteine, start_codon, stop_codon, three_prime_utr, five_prime_utr```

**GFF3 Feature types** 常见：```gene, mRNA, rRNA, tRNA, ncRNA, tmRNA, mobile_genetic_element, origin_of_replication, promoter, repeat_region, cDNA, polyA_sequence, polyA_site```

[NCBI对GFF/GTF Feature types 有一些特别规定](https://www.ncbi.nlm.nih.gov/genbank/genomes_gff/), e.g. 一些细致SO会被归纳为gene，misc_RNA会被归纳为transcript，intron/protein会被ignore，id的命名，...




**attributes格式**
```
GTF2.2: attr_name “attr_value”;     必须带gene_id transcript_id，value可以是""
        gene_id "xxx"; transcript_id "xxx.1"; transcript_name "GENE_202";

GFF3:   attr_name=v1,v2,...; 
        ID=cds001;Parent=mRNAa,mRNAb;
```


<details>
<summary> Gene/mRNA/CDS/UTR对应关系 </summary>

```
                 gene1  5'PPPPPT=======================================3'     ID=gene1  (DNA)         T=TSS, P=promoter regions
(Transcription)  hnRNA          EEEEEEEEEEEEEEEEEEEIIIIIIIIEEEEEEEEExxx                               E=Exon I=Intron
(Alternative     mRNA1          ===================........=========          ID=mRNA1;Parent=gene1
 splicing)       mRNA2          ===================                           ID=mRNA2;Parent=gene1
                 exon1          ===================                           Parent=mRNA1            ??why not gene1
                 5UTR1          ===................                           Parent=mRNA1 
                 3UTR1          ................===                           Parent=mRNA1
                 CDS1              =============                              Parent=mRNA1


mRNA = exon + exon + exon..
UTR: non-coding part in mRNA
CDS: Protein-coding part in mRNA
```
https://zhuanlan.zhihu.com/p/557609219
</details>



<details>
<summary> 更多GTF attributes </summary>

```
transcript示例：   gene_id "xxx"; transcript_id "xxx.1"; transcript_name "GENE_202"; 

#########ENSG00000186092.6################## gene Attr
gene_id "ENSG00000186092"; 
gene_version "6"; 
gene_name "OR4F5"; 
gene_source "ensembl_havana"; 
gene_biotype "protein_coding";
##########ENST00000641515.2################# mRNA/transcript Attr = gene Attr + 
transcript_id "ENST00000641515"; 
transcript_version "2"; 
transcript_name "OR4F5-202"; 
transcript_source "havana"; 
transcript_biotype "protein_coding"; 
tag "basic";
##########ENSE00003812156.1################# exon Attr = transcript Attr + 
exon_number "1"; 
exon_id "ENSE00003812156"; 
exon_version "1"; 
############################################ CDS Attr = transcript Attr + 
protein_id
############## five_prime_utr/three_prime_utr/start_codon Attr = transcript Attr
```
</details>



## BED

格式说明参考 [ensembl](https://grch37.ensembl.org/info/website/upload/bed.html) 或者 [nyu](https://learn.gencore.bio.nyu.edu/ngs-file-formats/bed-format/)













## VCF

记录SNP/INDEL/SV 等变异信息

| -- | BODY | -- | -- |
| -- | -- | -- | -- |
| 1 | CHROM | contig/chr编号 | -- |
| 2 | POS   | REF上变异发生的位点 | 即下文REF第一个碱基在contig上的位置 |     
| 3 | ID      | Variance 在各DB中的ID | 无则```.``` |      
| 4 | REF     | REF序列 | 空则```.``` |      
| 5 | ALT     | ALT序列 | 空则```.``` |      
| 6 | QUAL    | Phred-scaled: ```-10 * log(1-p)``` | p=是变异的概率 |    
| 7 | FILTER  | 是否通过过滤，通过意味着是变异 | ```filterName```(Failed to pass)/```PASS```/```.```(no filer) |      
| 8 | INFO    | site-level annotations: ```key=value;``` | 示例 ```AC=4973;VT=INDEL``` |    
| 9 | FORMAT  | 定义[SAMPLEs]中的变异位点格式: ```K1:K2:K3:K4``` | -- |      
|10 | SAMPLEs | 来自SAM文件```@RG```行```SM:SampleName```，一个样本对应一列，格式由FORMAT定义 | ```V1:V2:V3:V4a,V4b``` |     

INFO 常见：
```
AA=A              Ancestral Allele Sequence i.e. REF
AC=4973           ALT Allele Count in this sample set；即出现的次数
AF=0.99           ALT Allele Frequency in this sample set  
AN=5008           ALT Allele Number；对于二倍体，杂合子0/1 则 AN+=1，纯合子1/1 则 AN+=2
DP=2365           Read Depth 测序深度
MQ=100            Mapping Quality  比对质量
QD=0.12           Quality by Depth = QUAL/DP
VT=INDEL          Variant Type:   SNP  MNP  INDEL  SV
```

FORMAT for SAMPLEs 常见：
```
                                                         格式说明                                   示例
GT	Genotype	                                   ?/? 未相位化  ?|? 相位化                          0/1
AD	Allele Depth	                               REF,ALT                                        1000,1100
DP	Read Depth                                     REF,ALT                                        1000,1100
GQ	Phred Genotype Quality	                       Phred = -10 * log(1-p)；p是变异的概率              100
PL  Phred Likelihoods of 0/0,0/1,1/1               Phred = -10 * log(1-p)；p是GT存在的概率          0,0,0
PGT	Phased Genotype                                ?|? 相位化                                        0|1

* 相位化指知晓Allele来源亲本（父/母）
* Genotype中，0:REF  1:ALT   2:second ALT
* 0/0，0/1，1/1 Likelihoods总和为1
```
```#HeaderLines```中一般会描述INFO/FORMAT中的列，参考[GATK](https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format)；其它：[1000 Genomes](https://www.internationalgenome.org/) 提供不同地区的人类变异数据。




