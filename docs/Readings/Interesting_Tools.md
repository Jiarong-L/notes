
一些新发表的工具，待尝试


## CancerProteome
* CancerProteome: a resource to functionally decipher the proteome landscape in cancer
* http://bio-bigdata.hrbmu.edu.cn/CancerProteome/
* https://doi.org/10.1093/nar/gkad824
* MicroProteins：https://zhuanlan.zhihu.com/p/266633416

在线查询不同癌症类型的蛋白质/微蛋白


## Phables
* Phables: from fragmented assemblies to high-quality bacteriophage genomes
* https://doi.org/10.1093/bioinformatics/btad586
* https://www.x-mol.com/paper/1705618912748261376/t


从碎片化的病毒宏基因组组装中分离噬菌体基因组

## MedMNIST
* https://www.nature.com/articles/s41597-022-01721-8

似乎是一个比较全面的2D/3D医学图像数据库



## 拟时序多种算法
* Computational methods for trajectory inference from single-cell transcriptomics
* A comparison of single-cell trajectory inference methods
* https://mp.weixin.qq.com/s/j4zezzyiNRhZGKisUWPQ7w


## geNomad
* [Identification of mobile genetic elements with geNomad. Nat Biotechnol](https://doi.org/10.1038/s41587-023-01953-y)
* https://mp.weixin.qq.com/s/v4r008US-73OxqL-EGRAWg

鉴定可移动遗传元件的模型

## BASEHIT
* https://mp.weixin.qq.com/s/yW2DTmT_IPJjB83e_4vOSg

wet：与“人类外蛋白的酵母文库”结合的生物素化的菌株 （BASEHIT可以准确地识别细菌与人类外源蛋白之间的大部分直接相互作用）

“宿主和微生物之间的直接联系”


## 定量的ARG-MGE分布数据库
* https://mp.weixin.qq.com/s/BVvF6f-Bzwfs0Np3Xqrfbg



## GRN
* 现有的诱导分化方案下，未成熟的细胞可以表现适当的细胞类型特异性标记，但不能完全执行其专门的生理功能: [SinCMat](https://www.cell.com/stem-cell-reports/fulltext/S2213-6711(23)00499-X) 根据训练集得到(成熟时)每种细胞特有的TF，随后模型可用于提示query单细胞的功能基因推断其缺乏什么TF才能达成成熟?
    - ITF即身份标志，STF结合ITF微调表达
    - 将细胞类型特异性功能基因集定义为每种细胞类型中表达最高的前10%的基因
    - ITF-STF 对应的 候选功能基因：Jaccard相似性/Pearson相关
    - SinCMatDB, a manually curated database with experimentally validated cell maturation cues from literature


## 引物探针

[引物探针的设计流程](http://www.cebsit.cas.cn/ggpt/ggjsfwzx/zyjspt/fzxbjspt/yqlb_154652/201906/W020190620571716878509.pdf)

```
• 引物尽可能地接近探针，但是不可与探针重叠 
• 引物长度9-40bp，最优20bp，GC含量保持在30-80%之间 
• 避免同一碱基重复过多，特别是连续4个或更多的G 
• 引物Tm值在58-60C之间，上下游引物Tm不要超过2C 
• 引物3’端的5个碱基中，G和C加起来不要超过2个 
• 引物3’端不要是碱基A，避免出现3个以上相同碱基 
• 避免引物自身或与引物之间形成4个或4个以上连续配对 
• 避免引物自身形成环状发卡结构 
• 扩增片段的长度在50-150bp之间
```

我记得NCBI还是哪里可以计算序列的退火温度？？或者有个公式？？


## 单细胞组成差异分析

TODO: 确认一下统计方法

* [scCODA](https://lishensuo.github.io/posts/bioinfo/038%E5%8D%95%E7%BB%86%E8%83%9E%E5%88%86%E6%9E%90%E5%B7%A5%E5%85%B7--sccoda%E7%BB%86%E8%83%9E%E7%BB%84%E6%88%90%E6%AF%94%E8%BE%83/) -- 不同分组样本的细胞组成的差异


## LLM 测试工具

[Agentboard](https://engineering.westlake.edu.cn/NewsEvents/LatestNews/202410/t20241017_43042.shtml) 




