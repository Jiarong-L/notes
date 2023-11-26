

* promoter: 接近TSS区域，包含TF结合位点、募集 RNA polymerase
* 如果TF接触 promoter region 时结合了 enhancer，则基因的表达量升高；如果结合了 silencer，则基因的表达量降低
* enhancer 最远距离 promoter region 上下游1Mb


# ATAC-seq 


* 使用Tn5转酶切割染色质的开放区域、对这些片段进行测序。    
* 优点：只需要少量样本(500~50000 cell)、
* 可结合基因表达数据、挖掘开放区域的潜在转录因子结合区域(TFBS)，得到关键的TF
    - Atlas绘制
    - 潜在的疾病Marker

## Pipeline

* Sequencing QC & Trim
* Mapping
* Pre-analysis
    - Mark PCR Duplicate
    - Filter Insert Size
* Peak Calling
    - QC & replicate reproducibility
    - High Quality Peak Sets
* Analysis
    - Normalization
    - Peak Annotation
    - Motif detection
    - GO, Pathway ...






