
Juicer系列是HiC数据分析的常用工具，包括[Juicer](https://github.com/aidenlab/juicer/wiki), [Juicebox](https://github.com/aidenlab/Juicebox), [Juicertools](https://github.com/aidenlab/juicertools)


最便捷的工具是Juicer系列: [Juicer](https://github.com/aidenlab/juicer) 从raw.fq数据直接生成 Hi-C maps & structural features；[Juicebox](https://github.com/aidenlab/Juicebox) 提供可视化、修改功能；随后再将修改后的map返回 Juicer 完成 scaffolding。  


[Juicertools](https://github.com/aidenlab/juicertools) 可提供额外的下游分析 (TAD/Loops/...)


## Install
```bash
conda activate hic

conda install hcc::juicer    ##  juicer_tools -h 
# conda install conda-forge::gnu-coreutils
conda install bioconda::bwa

git clone https://github.com/theaidenlab/juicer.git     
cd juicer/CPU
wget 
ln -s juicer_tools.1.9.9_jcuda.0.8.jar  juicer_tools.jar
cd ..
ln -s CPU scripts        ## hard code in some steps ...
cd ..

export PATH=$PATH:$PWD/juicer/CPU/     ## juicer.sh   -----  juicer/CPU/juicer.sh
export PATH=$PATH:$PWD/juicer/misc/    ## generate_site_positions.py      -----  juicer/misc/generate_site_positions.py
# ln -s juicer/CPU scripts
```
Juicebox建议安装桌面版，莫折腾WSL了

测试数据：[juicer’s Test data](https://github.com/aidenlab/juicer/wiki/Installation#quick-start)，[ENCODE](https://www.encodeproject.org) 下载 .hic，[WorkShop](https://github.com/hms-dbmi/hic-data-analysis-bootcamp) 的数据

## Juicer

```bash
juicer.sh \
  -z ref/hg38.fa \              # bwa index hg38.fa
  -p ref/hg38.chrom.sizes \     # 染色体 大小    samtools faidx hg38.fa; cut -f 1,2 hg38.fa.fai > hg38.chrom.sizes
  -y ref/hg38_HindIII.txt \     # 酶切位点       generate_site_positions.py HindIII hg38 hg38.fa
  -d fq_folder \                # matching fq_folder/<fastq  and split(Trimmed)>/*_R*.fastq*
  -D $PWD/juicer \              # /path/to/juicer 安装目录
  -t 4                          # 线程数

# juicer.sh  -z ref/hg38.fa  -p ref/hg38.chrom.sizes -y ref/hg38_HindIII.txt -d fq_folder -D $PWD/juicer -t 4  
```

Output: 
```bash
fq_folder/aligned/
├── merged_nodups.txt    # 去重后的交互对 .pairs 格式，可通过 pairtools 处理
├── inter.hic            # 标准化的 Hi-C 矩阵（用于下游分析）
└── inter_30.hic         # 30kb 分辨率矩阵
```


## Juicebox

可视化，见相关视频

Try: ```java -jar Juicebox.jar -m hg38.chrom.sizes -p fq_folder/aligned/inter.hic```

## Juicertools

Find Loops
```bash
juicer_tools hiccups -m 512 -r 5000,10000 -k KR   fq_folder/aligned/inter.hic  loops_output

-m matrixSize   最小交互距离
-k normalization (NONE/VC/VC_SQRT/KR)  归一化方法
-c chromosome(s)
-r resolution(s)   分辨率
-f fdr
-p peak width
-i window
-t thresholds
-d centroid distances
--ignore-sparsity
specified_loop_list
```

Find TADs --- 其实是一些concat domain，更像是sub-TAD?
```bash
juicer_tools arrowhead -m 2000 -r 10000 -k KR   fq_folder/aligned/inter.hic  tads_output


-c chromosome(s)
-m matrix size
-r resolution
-k normalization (NONE/VC/VC_SQRT/KR)
--ignore-sparsity flag
feature_list
control_list
```

