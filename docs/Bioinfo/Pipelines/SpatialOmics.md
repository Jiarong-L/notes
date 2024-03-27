

原理参考 [10x Genomics Support](https://www.10xgenomics.com/support)

Spatial Omics 可以提供基因表达的空间定位，

## Spatial Omics

Spatial Transcriptomics 常见方法可分为以下3类：

* 原位杂交 FISH：为n种目标RNA设计n种荧光探针以进行原位杂交，根据荧光信号达成高度精确定位
    - 亚细胞水平的分辨率
    - MERFISH（**MERSCOPE**平台）使用多轮杂交的信号组合（一组二进制vector）为身份标识，最多可以同时支持155个基因的探测
    - **CosMx**成像系统原理为FISH，得到3D空间的表达（3cm*3cm*3cm）

* 原位测序（ISS）：信号放大版的FISH
    - 亚细胞水平的分辨率
    - **10x Xenium**：对n种目标RNA设计n种padlock（padlock首尾与RNA互补，中间有ID barcode），将padlock与目标RNA进行杂交，随后通过滚换复制得到几百倍的padlock序列；随后，对padlock进行多轮荧光探针的原位杂交进行定位
        - n种padlock的集合称为paddle 
        - Xenium 的荧光探针是特定序列的寡核苷酸（针对poadlock ID），但染料只有4种颜色，故需分多轮进行杂交定位：清洗后再放入下一轮针对不同ID的荧光探针

* Spot-based（ST）原位捕获：将样本平铺在一片Spot上，裂解细胞后遗传物质落入相应的 Spot 中获得空间标签，随后进行NGS测序
    - Spot的大小为其分辨率，可以是多细胞水平（**10x Visum**），也可以是亚细胞水平（**BGI Stereo-seq**）


## 一些技术问题

* 对于FISH/ISS等亚细胞水平分辨率的方法，得到序列后需要考虑如何将reads分配给细胞
    - assign给最近的细胞核
    - 可以根据 k-hoop neighbor embedding 信息进行 binning
    - 直接从染色图像中识别细胞边界（STCellbin for Stereo-seq）

* 对于 10x Visum，每个Spot可能跨越几个细胞，也可能切割一些细胞，故而如何将spots中reads分配给单个细胞也是一种挑战
    - 常见将单细胞数据作为reference，预测每个spot中的细胞组成（deconvolution）

* 如何将空间坐标（Spatial landmark）与组织照片对齐
    - [Image registration DL model](https://www.nature.com/articles/s41592-024-02199-5)


## BGI Stereo-seq

BGI已为其开发了 [SAW workflow](https://www.stomics.tech/col447/list) 以得到表达矩阵，其中的预处理方法：

* STCellbin 从ssDNA染色图像中识别细胞边界，直接将reads分配给细胞，得到 Cell bin 矩阵；无图像则只能用 Square bin 矩阵（e.g. bin50=50*50 spots）

* Spot-based 方法有极高可能发生如下问题：（[EAGS对Stereo-seq数据进行平滑处理](https://zhuanlan.zhihu.com/p/683428338)）
    - Dropout：某些基因仅在一部分细胞中高度表达，而在其余细胞中为0
    - Spot Swapping：mRNA在解离过程中向附近spot点渗出，表现为RNA被其他组织区域的探针捕获或出现在不该出现的背景区域








## 10x Visum


[Space Ranger](https://www.10xgenomics.com/support/software/space-ranger/latest)(10x Visium; each spot contains several cells) + Seurat.   


Seurat provides methods for clustering, gene expr viewing, marker detection and ‘anchor’ between scRNA datasets (e.g., scRNA data & deconvoluted Visium data).







分析工具

Giotto：https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02286-2









