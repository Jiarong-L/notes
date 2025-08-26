某些组装软件要求预估基因组大小，此时可以参考相似物种的大小；也可以使用Jellyfish  


## Install
```
sudo apt install jellyfish
```

## Use
### Basic
TBA






### Estimate Genome Size xxx
基因组大小=(Kmer总数)/(主峰深度)

1. PE reads 需要将R2进行进行反向重复后、合并至R2
2. 对合并后的文件error correction (quorum) & 清除 adapter(??)
3. jellyfish count 

https://zhuanlan.zhihu.com/p/506725567  

当基因组杂合非常高或者重复序列比例非常大时，其影响可能导致无法通过K-mer分析正确估计基因组大小

https://www.annasyme.com/docs/jellyfish.html  





masurca中示例：[rename_filter_fastq](./MaSuRCA/rename_filter_fastq)、[rename_filter_fastq.pl下载](./MaSuRCA/rename_filter_fastq.pl)
```bash
./rename_filter_fastq 'pe' <(less 'E_R1.fq.gz' | awk '{if(length($0>250)) print substr($0,1,250); else print $0;}') <(less 'E_R2.fq.gz' | awk '{if(length($0>250)) print substr($0,1,250); else print $0;}' ) > 'renamed.fastq'

MIN_Q_CHAR=`cat renamed.fastq |head -n 50000 | awk 'BEGIN{flag=0}{if($0 ~ /^\+/){flag=1}else if(flag==1){print $0;flag=0}}'  | perl -ne 'BEGIN{$q0_char="@";}{chomp;@f=split "";foreach $v(@f){if(ord($v)<ord($q0_char)){$q0_char=$v;}}}END{$ans=ord($q0_char);if($ans<64){print "33\n"}else{print "64\n"}}'`


./quorum_error_correct_reads  -q $(($MIN_Q_CHAR + 40)) --contaminant=/mnt/d/WSL_dir/workdir/MaSuRCA-4.1.0/bin/../share/adapter.jf -m 1 -s 1 -g 1 -a 3 -t 32 -w 10 -e 3 -M  quorum_mer_db.jf pe.renamed.fastq --no-discard -o pe.cor.tmp --verbose 1>quorum.err 2>&1 && mv pe.cor.tmp.fa pe.cor.fa 

## JF_SIZE can be randomly large; it's size of hash table: should be genome size + extra kmers from seq errors
## However, it does say that hash size will be increased automatically if needed
JF_SIZE=`ls -l renamed.fastq | awk '{n+=$5}END{s=int(n/50); if(s>200000000)printf "%.0f",s;else print "200000000";}'` 
jellyfish count -m 31 -t 32 -C -s $JF_SIZE -o out.txt pe.cor.fa

ESTIMATED_GENOME_SIZE=`jellyfish histo -t 32 -h 1 out.txt | tail -n 1 |awk '{print $2}'`
echo $ESTIMATED_GENOME_SIZE
```



## 参考
Jellyfish: https://github.com/gmarcais/Jellyfish  
Download: http://www.cbcb.umd.edu/software/jellyfish/   
Blog: http://www.chenlianfu.com/?p=806   
