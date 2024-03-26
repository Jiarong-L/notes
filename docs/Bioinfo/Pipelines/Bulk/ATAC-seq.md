

使用Tn5转酶切割染色质的**开放区域**、对这些片段进行**测序**；只需要少量样本(500~50000 cell)；可结合基因表达数据、挖掘开放区域的潜在转录因子结合区域(TFBS)，得到关键的TF作为潜在的疾病的Marker或进行Atlas绘制


* promoter: 接近TSS区域，包含TF结合位点、募集 RNA polymerase
* 如果TF接触 promoter region 时结合了 enhancer，则基因的表达量升高；如果结合了 silencer，则基因的表达量降低
* enhancer 最远距离 promoter region 上下游1Mb


## Pipeline

与 [ChipSeq 流程](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3431496/)有许多重合

| 依次进行 | Tools | 说明 |
| -- | -- | -- |
| Reads QC + Trim | FastQC + Trimmomatic | -- |
| Mapping to Ref | Bowtie2 | 得到 BAM file |
| Pre-analysis | Samtools | - Mark PCR Duplicate<br>- Filter Insert Size<br>- Filter off mitochondria reads |
| Peak Calling + Refining | MACS2 ```--shift -100``` | - QC & replicate reproducibility<br>- High Quality Peak Sets |
| Peak QC | samtools + ChIPQC + phantompeakqualtools | InsertSize, FRiP, ... |
| (Combine Replication) | IDR | 得到重复样本间一致性的peaks (理论上重复样本的peaks应该高度一致，但...) |
| ------- | Normalization + Analysis | ------- |
| Diff Peak | DiffBind | 鉴定两个样本间差异结合位点，输入BED file |
| Peak Annotation | ChIPseeker | 如果Bioconductor没有合适的TxDb，则需要使用GenomicFeatures包```makeTxDbFromUCSC/ makeTxDbFromBiomart```制作 |
| Motif detection | MEME / [chromvar](https://github.com/GreenleafLab/chromVAR) + ggmotif_plot  | 获取Motif基序 |
|  | TFBSTools | 随后可以根据Motif寻找潜在TFBS（或使用JASPAR数据库） |
| Footprinting | HINT-ATAC | 验证潜在TFBS：如果某一开放区域已经结合TF，则此区域不会被测得，表现为peak中间有凹陷 |
| GO, Pathway ... | -- | -- |



## 参考


https://www.plob.org/article/24683.html

https://zhuanlan.zhihu.com/p/590862767

https://zhuanlan.zhihu.com/p/471350610

https://www.jianshu.com/p/6aba8f1dea56

https://cloud.tencent.com/developer/article/1624517

https://cloud.tencent.com/developer/article/1360799

https://zhuanlan.zhihu.com/p/57516178

https://www.jianshu.com/p/6aba8f1dea56  
