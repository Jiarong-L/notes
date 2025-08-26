
[HiC-Pro](https://github.com/nservant/HiC-Pro) 可用于生成 Hi-C 交互矩阵

1. ReadQC
2. Mapping，处理嵌合 reads
3. 统计有效 Hi-C 交互数据量
4. 生成不同分辨率的 contact matrix (bin)，进行 ICE Normalization
5. 为方便下游分析，matrix格式可转换为：.hic 格式（Juicebox），.cool（Cooler）




## Install

```bash
git clone https://github.com/nservant/HiC-Pro
conda env create -f HiC-Pro/environment.yml -p hicpro
conda activate /mnt/l/WSL_DIR/WORKDIR/HiC_run/hicpro
```


## Useage


hic_results/data/allValidPair