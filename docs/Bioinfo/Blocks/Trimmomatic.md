

## Install
```
conda install -c bioconda trimmomatic -y
```

## Usage
PE
```
trimmomatic PE -phred33  E_R1.raw.fq.gz  E_R2.raw.fq.gz  E_R1.trimmed.fq.gz E_R1.U.fq.gz  E_R2.trimmed.fq.gz E_R2.U.fq.gz SLIDINGWINDOW:4:15 MINLEN:75   -summary summary.txt  -trimlog log.txt  -threads 64  -quiet
```  
SE
```
trimmomatic SE -phred33 raw.fq.gz trimmed.fq.gz SLIDINGWINDOW:4:15 MINLEN:75   -summary summary.txt  -trimlog log.txt  -threads 64  -quiet
```

常用参数设置
```
# Trimmomatic内置了常规接头文件，illumina系的常规测序仪下机数据不用输入此参数
# :<待剪切的adapter序列>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>
ILLUMINACLIP:adapter.fa:2:30:10     

# :<windowSize>:<requiredQuality>
SLIDINGWINDOW:4:15

# :<length>
MINLEN:75
```
详细参数描述请见: [TrimmomaticManual](./Trimmomatic/TrimmomaticManual_V0.32.pdf)

## Result
outputFiles(PE): paired(trimmed) unpaired(U)
```
E_R1.trimmed.fq.gz       *
E_R1.U.fq.gz
E_R2.trimmed.fq.gz       *
E_R2.U.fq.gz
```

outputFiles(SE): 
```
trimmed.fq.gz            *
```

summary
```
Input Read Pairs: 500
Both Surviving Reads: 494
Both Surviving Read Percent: 98.80
Forward Only Surviving Reads: 3
Forward Only Surviving Read Percent: 0.60
Reverse Only Surviving Reads: 3
Reverse Only Surviving Read Percent: 0.60
Dropped Reads: 0
Dropped Read Percent: 0.00
```

trimlog:  
```
SRR22097888.1 E100030723L1C001R00100000167 length=150 150 0 150 0
SRR22097888.1 E100030723L1C001R00100000167 length=150 150 0 150 0
SRR22097888.2 E100030723L1C001R00100000669 length=150 149 0 149 1
SRR22097888.2 E100030723L1C001R00100000669 length=150 150 0 150 0
SRR22097888.3 E100030723L1C001R00100000975 length=150 150 0 150 0
SRR22097888.3 E100030723L1C001R00100000975 length=150 150 0 150 0
SRR22097888.4 E100030723L1C001R00100020241 length=150 150 0 150 0
SRR22097888.4 E100030723L1C001R00100020241 length=150 135 0 135 15
SRR22097888.5 E100030723L1C001R00100026545 length=150 150 0 150 0
SRR22097888.5 E100030723L1C001R00100026545 length=150 149 0 149 1
......
```



## 参考
[Manual](http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf) 

[Fastq](https://www.jianshu.com/p/b37b9fdb7e61)  

[Phred(illumina1.8+后回归33)](https://zhuanlan.zhihu.com/p/504905826)