

绘制基因结构和变异位置示意图，参考: [trackViewer](https://mp.weixin.qq.com/s/bcUphx5t01zk1oSpQWNK4A), [IRanges](https://www.jianshu.com/p/ba831e9cefb8)


```R
## BiocManager::install("trackViewer")
library(trackViewer)


SNP_pos <- c(100,101,102,222,355)
SNP <- IRanges(start=SNP_pos, width=1, names=paste0("snp", SNP_pos) )
SNP.gr <- GRanges("ExampleChr", SNP)
SNP.gr$color <- c("#FF8833","#FF8833","#FF8833","white","#51C6E6")


Gene <- IRanges(start=c(10,300), end=c(200,500), names=c("Gene1","Gene2") )
Gene.gr <- GRanges("ExampleChr", Gene)
Gene.gr$height <- c(0.02, 0.01)
Gene.gr$fill <- c("#FF8833", "#51C6E6")

lolliplot(SNP.gr, Gene.gr, ranges = GRanges("ExampleChr", IRanges(1, 800)),ylab = FALSE)


### Multi layer
Gene_multi.gr <- rep(Gene.gr, 3)
Gene_multi.gr$featureLayerID <- paste("TX", rep(1:3, each=length(Gene.gr)), sep="_")
lolliplot(SNP.gr, Gene_multi.gr, ranges = GRanges("ExampleChr", IRanges(1, 800)),ylab = "TX", label_on_feature = FALSE )

```
![](trackViewer/1.png)





