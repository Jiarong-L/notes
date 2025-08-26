

The current version of SPAdes works with **Illumina** or IonTorrent reads and is capable of providing hybrid assemblies using **PacBio**, Oxford Nanopore and Sanger reads. You can also provide additional contigs that will be used as long reads.

## Install
```
wget https://cab.spbu.ru/files/hicSPAdes/hicSPAdes-binner-0.1.tar.gz
tar -xzf hicSPAdes-binner-0.1.tar.gz
cd hicSPAdes-binner-0.1
mkdir build 
cd build 
cmake ../src -Wno-dev
make hicspades-binner

wget https://cab.spbu.ru/files/release3.15.4/SPAdes-3.15.4-Linux.tar.gz
tar -xzf SPAdes-3.15.4-Linux.tar.gz

export PATH=/mnt/d/WSL_dir/workdir/hicSPAdes-binner-0.1/build/bin:/mnt/d/WSL_dir/workdir/hicSPAdes-binner-0.1/build/SPAdes-3.15.4-Linux/bin:$PATH
```


## SPAdes
### Usage
```
spades.py -o out_dir  -1 E.R1.fq.gz  -2 E.R2.fq.gz    
spades.py -o out_dir  -1 E.R1.fq.gz  -2 E.R2.fq.gz   --pacbio   E.pacbio.fq.gz
spades.py -o out_dir  -1 E.R1.fq.gz  -2 E.R2.fq.gz   --nanopore E.nano.fq.gz

# --careful --disable-gzip-output --threads 24 --memory 150(是GB)   
```
得到默认命名的scaffolds.fasta，可以重新命名; 其中输出的Header示例：
```
>NODE_1_length_535588_cov_260.739

## 可以基于此筛选：放弃coverage<30的序列，length<500的序列
```
也可以加入其它软件生成的contigs（作为seed?）：
```
--trusted-contigs      high_quality_ctgs.fa
--untrusted-contigs    low_quality_ctgs.fa
```


### Other Modes
```
  --isolate                   this flag is highly recommended for high-coverage isolate and multi-cell data
  --sc                        this flag is required for MDA (single-cell) data
  --meta                      this flag is required for metagenomic data
  --bio                       this flag is required for biosyntheticSPAdes mode
  --corona                    this flag is required for coronaSPAdes mode
  --rna                       this flag is required for RNA-Seq data
  --plasmid                   runs plasmidSPAdes pipeline for plasmid detection
  --metaviral                 runs metaviralSPAdes pipeline for virus detection
  --metaplasmid               runs metaplasmidSPAdes pipeline for plasmid detection in metagenomic datasets (equivalent for --meta --plasmid)
  --rnaviral                  this flag enables virus assembly module from RNA-Seq data
  --iontorrent                this flag is required for IonTorrent data

coronaspades.py
metaplasmidspades.py
metaspades.py
metaviralspades.py
plasmidspades.py
rnaspades.py
rnaviralspades.py
truspades.py
```
示例：
```
spades.py -o out_dir  -1 E.R1.fq.gz  -2 E.R2.fq.gz  --meta  
## Same As ##
metaspades.py  -o out_dir  -1 E.R1.fq.gz  -2 E.R2.fq.gz
```

## hicSPAdes (Meta)
Hi-C Metagenomics, pre-release.  

### 批量调用
* [Batch.py](./SPAdes/Batch.py)批量生成脚本与yaml
* [Collect.py](./SPAdes/Collect.py)将每个样本的fasta分开至每一个bin  
```
## 需要修改Gen_Scripts开头的PATH！！！

python3 Batch.py clean.fq.lst
```

其中clean.fq.lst示例：
```
Example1    ABSOLUTE_PATH//E1_R1.fq.gz ABSOLUTE_PATH//E1_R1.fq.gz
Example2    ABSOLUTE_PATH//E2_R1.fq.gz ABSOLUTE_PATH//E2_R1.fq.gz
```
```
<output_dir(also as perfix)>   <clean_R1.fq.gz>    <clean_R2.fq.gz>
- tab分隔, 无header
- output_dir末尾不能带'/'等影响linux命名的字符，它可以是相对or绝对路径；建议使用分析名当文件夹
- 生成：output_dir.pipe.sh  output_dir/cleandata.yaml 
```

### 示例bash
Example1.pipe.sh
```
cd Example1
export PATH=/mnt/d/WSL_dir/workdir/hicSPAdes-binner-0.1/build/bin/:$PATH
export PATH=/mnt/d/WSL_dir/workdir/hicSPAdes-binner-0.1/build/SPAdes-3.15.4-Linux/bin/:$PATH
metaspades.py -1 ABSOLUTE_PATH/E1_R1.fq.gz -2 ABSOLUTE_PATH/E1_R1.fq.gz -o .
hicspades-binner assembly_graph_with_scaffolds.gfa cleandata.yaml Bins
cd Bins ; python3 /mnt/d/WSL_dir/workdir/Collect.py; cd ..
```

### 示例yaml
Example1/cleandata.yaml
```
        [
                {
                        orientation: "fr",
                        type: "hic",
                        right reads: ["ABSOLUTE_PATH/E1_R1.fq.gz"],
                        left reads: ["ABSOLUTE_PATH/E1_R1.fq.gz"],
                }
        ]
```
‘hicSPAdes-binner currently supports a **single** Hi-C library described in a YAML file’, 安全起见一个样本一个YAML吧

### Error
```
No input file to read network 
```
- 因为并行运行使用同一个./tmp目录，导致结果相互覆盖 
- 数据不足，没有通过HiC数据连接的contigs   




## 参考
SPAdes: https://github.com/ablab/spades  
hicSPAdes: https://cab.spbu.ru/software/hicspades/  
SPAdes manual: https://cab.spbu.ru/files/release3.13.0/manual.html
SPAdes: https://zhuanlan.zhihu.com/p/77274286