

参考 [GATK](https://gatk.broadinstitute.org/hc/en-us) Best Practices


中文示例
```
HaplotypeCaller流程     https://cloud.tencent.com/developer/article/1445600
HaplotypeCaller流程     https://zhuanlan.zhihu.com/p/69726572
HaplotypeCaller原理     https://zhuanlan.zhihu.com/p/485479829
(g)vcf矫正质量          https://cloud.tencent.com/developer/article/2323192
PathSeq                https://cloud.tencent.com/developer/article/2331060
```


## Install

下载GATK及其[对应的JAVA环境](https://github.com/broadinstitute/gatk?tab=readme-ov-file#requirements)
```bash
sudo apt install openjdk-17-jdk    ##java -version
wget https://github.com/broadinstitute/gatk/releases/download/4.5.0.0/gatk-4.5.0.0.zip
unzip gatk-4.5.0.0.zip
export PATH=$PATH:$PWD/gatk-4.5.0.0/

gatk --list    ##--java-options "-Xmx20G -Djava.io.tmpdir=./" 
```



正常服务器中也可以直接使用 [Docker 版的 GATK](https://gatk.broadinstitute.org/hc/en-us/articles/360035889991--How-to-Run-GATK-in-a-Docker-container)，预先 [Docker Installation](https://docs.docker.com/engine/install/ubuntu/)；注意 [WSL 一般用作 Desktop 版本的后台](https://docs.docker.com/desktop/wsl/#turn-on-docker-desktop-wsl-2)??，[WSL-Ubuntu 启用 systemctl](https://learn.microsoft.com/zh-cn/windows/wsl/systemd) 有许多坑，**以下代码在WSL中没有成功**，[参考](https://blog.csdn.net/shizheng_Li/article/details/124364276)
```bash
sudo apt update
sudo apt install systemd -y
ps -p 1 -o comm=

sudo usermod -aG docker a
sudo gpasswd -a a docker  

sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

sudo service docker start    ## systemctl restart docker  systemctl not avaliable
sudo service docker status   ## shutdown immediately
```


## Variants Calling

从bam文件中提取SNP和INDEL信息

### DATA

以 Whole exome sequencing 项目的数据为示例，此例使用 [SRR7696207](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR7696207&display=metadata) 和 hg38 的一部分（话说其实 Arabidopsis thaliana genome 更小）


```bash
ascp -i /home/a/miniconda3/envs/ascp/etc/asperaweb_id_dsa.openssh -l 100M -QT -P33001 -k1 era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/SRR769/007/SRR7696207/SRR7696207_1.fastq.gz ./
ascp -i /home/a/miniconda3/envs/ascp/etc/asperaweb_id_dsa.openssh -l 100M -QT -P33001 -k1 era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/SRR769/007/SRR7696207/SRR7696207_2.fastq.gz ./
wget https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa
head -54305 GRCh38_full_analysis_set_plus_decoy_hla.fa > ref.fa
```


预处理后mapping，生成bam文件、各种index

```bash
trimmomatic PE -phred33  SRR7696207_1.fastq.gz  SRR7696207_2.fastq.gz  R1.trimmed.fq.gz R1.U.fq.gz  R2.trimmed.fq.gz R2.U.fq.gz SLIDINGWINDOW:4:15 MINLEN:75   -summary summary.txt  -trimlog log.txt  -threads 64  -quiet
## Sequence and quality length don't match, so get only 8956996/4 reads
bwa index ref.fa 
samtools faidx ref.fa 
bwa mem ref.fa R1.trimmed.fq.gz R2.trimmed.fq.gz > aln.sam 
samtools view -b aln.sam > aln.bam
samtools sort aln.bam  > sorted.aln.bam
picard CreateSequenceDictionary R=ref.fa O=ref.dict
```


### bam 预处理

```bash
gatk --java-options "-Xmx20G -Djava.io.tmpdir=./tmp" MarkDuplicates \
    -I sorted.aln.bam -O markdp.bam \
    -M aln.metrics \
    1>MarkDuplicates_log 2>&1

gatk --java-options "-Xmx20G -Djava.io.tmpdir=./tmp" FixMateInformation \
    -I markdp.bam \
    -O markdp.fixmt.bam \
    -SO coordinate \
    1>FixMateInformation_log 2>&1 

# fix the read groups， opt：  # SORT_ORDER=coordinate \
picard AddOrReplaceReadGroups \
I=markdp.fixmt.bam \
O=markdp.fixmt.RG.bam \
RGID=RGID \
RGLB=lib1 \
RGPL=ILLUMINA \
RGPU=unit1 \
RGSM=Sample1 \


samtools sort markdp.fixmt.RG.bam  > final.bam
samtools index final.bam
```

1. 标记 PCR duplicates，之后可以设置 REMOVE_DUPLICATES=true 来丢弃duplicated序列
2. Fix mate information for pair-end data
3. （GATK3-now_Depricated）对INDEL周围进行 realignment: RealignerTargetCreator + IndelRealigner
4. （可选）BaseRecalibrator 根据 **利用已有的snp/indel数据库(known-sites)** 计算校准值  + ApplyBQSR 重新调整原来BAM中碱基质量值
5. **ADD ReadGroups ??** 否则 [Errors-about-read-group](https://gatk.broadinstitute.org/hc/en-us/articles/360035532352-Errors-about-read-group-RG-information)


### Variants Calling

检测 SNP/INDEL，可生成 vcf（突变位点情况） 或 gvcf（所有位点情况）
```bash
gatk --java-options "-Xmx20G -Djava.io.tmpdir=./tmp" HaplotypeCaller \
    -R ref.fa  \
    -I final.bam \
    -O raw.vcf \
    1>HaplotypeCaller_log 2>&1

##  --emit-ref-confidence {NONE, BP_RESOLUTION, GVCF}    and -ERC not working
gatk --java-options "-Xmx20G -Djava.io.tmpdir=./tmp" HaplotypeCaller \
    --emit-ref-confidence GVCF  \
    -R ref.fa  \
    -I final.bam \
    -O raw.gvcf \
    1>HaplotypeCaller_log 2>&1    

## IF many GVCF files？？vcf_merge=MergeVcfs, gvcf_merge=GenotypeGVCFs
gatk --java-options "-Xmx20G -Djava.io.tmpdir=./tmp" GenotypeGVCFs \
    -R ref.fa  \
    -V raw.gvcf -O merge
```


### Variants QC
对于vcf，提取 SNP/INDEL 并质控过滤
```bash
## IF many VCF files？？vcf_merge=MergeVcfs, gvcf_merge=GenotypeGVCFs
gatk SelectVariants -select-type SNP -V raw.vcf -O raw.snp.vcf
gatk SelectVariants -select-type INDEL -V raw.vcf -O raw.INDEL.vcf

gatk VariantFiltration -V raw.snp.vcf --filter-expression "QD < 2.0 || MQ < 40.0 || FS > 60.0 || SOR > 3.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "PASS" -O filtered.snp.vcf
gatk VariantFiltration -V raw.INDEL.vcf --filter-expression "QD < 2.0 || FS > 200.0 || SOR > 10.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "PASS" -O filtered.INDEL.vcf

gatk MergeVcfs -I filtered.snp.vcf -I filtered.INDEL.vcf -O filtered.INDEL_SNP.vcf
```

如果有参考数据库，可以对 gvcf 进行 [VQSR 质控过滤（VariantRecalibrator + ApplyVQSR](https://cloud.tencent.com/developer/article/2323192)

