<style>
img{
    width: 60%;
}
</style>


## Links
* 示例数据来源：https://www.10xgenomics.com/resources/datasets
* 数据库（TBA）
    * CellMarker：http://biocc.hrbmu.edu.cn/CellMarker/index.jsp
    * PanglaoDB：https://panglaodb.se/index.html
    * SingleR datasets


## Basic Pipeline (mainly Seurat)
* CellRanger ...
* Data QC
    * Filter off Genes
        * Appear in >3 Cells
    * Filter off Cells
        * Doublet Detection: Scrublet, DoubletFinder, DoubletDecon
        * Mitochondrial Genes 
        ```
        (pattern = "^MT-")     ## <15% OK, later: ScaleData(pbmc, vars.to.regress = "percent.mt")
        ```
        * Ribosomal Genes 
        ```
        (pattern = "^RP[SL]")  ## <5% OK
        ```
        * Hemoglobin Genes 
        ```
        (pattern = "^HB[^(P)]")
       ## "HBA1","HBA2","HBB","HBD","HBE1","HBG1","HBG2","HBM","HBQ1","HBZ"
       ```
        * minGeneNum > 200-500 
        * maxGeneNum < X, X decided via 'VlnPlot()'; Droplets may contain more genes
* Normalize & Scale & HVGs
    * NormalizeData() --- "LogNormalize"
    * FindVariableFeatures() --- **HVGs:** GeneA_cellA v.s. GeneA_Overall
        * Opt. If dataset is large, use HVGs for afterward analysis
    * ScaleData() --- Zero-centered or Mean-subtraction
    * SCTransform() = NormalizeData() + FindVariableFeatures() + ScaleData()
* Cell-Cycle Scoring and Regression (Opt.)
    * Pick HVGs
    * Load Cell Circle Genes --- Seurat: cc.genes
    * CellCycleScoring()
    * ScaleData()
        * Opt.1: vars.to.regress = c("S.Score", "G2M.Score")
        * Opt.2: vars.to.regress = c("CC.Difference")；CC.Difference = S.Score - G2M.Score
        * 注意，Opt.1不适合关注细胞分化的实验，因为会完全消除非周期细胞和周期细胞之间的区别；Opt.2 将保持二者间细胞周期差异，仅消除二者内部细胞周期差异
        * Tips：可以通过查看对PC贡献最多的基因是否是细胞周期相关基因来判断影响
* Batch Correction
    * Opt.1: CCA+MNN --- Seurat: FindIntegrationAnchors()+IntegrateData()
    * Opt.2: Harmony
* Clustering
    * PCA
    * UMAP/tSNE (PCA result as input)
    * Clustering (PCA result as input)
    ```
    scRNA <- FindNeighbors(scRNA, dims = pc.num)
    scRNA <- FindClusters(scRNA, resolution = 0.5)
    ```
* Cell-type Annotation
    * Find marker genes --- **Diff-expr genes:** cluster v.s. clusters
    * Annotate clusters (cell types) based on marker genes
        * SingleR() + HumanPrimaryCellAtlasData(label.main)/CellMarker/PanglaoDB/Papers...
    * Tips：在这个水平上进行一些常规的分析(cluster间的比较)，比方说KEGG、GO富集分析，差异基因表达分析（cell-type间），etc.
* Sub-Clustering
    * Pick a cluster (cell-type), Clustering & Annotate
        * SingleR() + MonacoImmuneData(label.fine) to sub-clusters
    * Tips：假设这些sub-type都来自同一个cell-type，在这个水平上进行一些更加细致的操作，比如：对免疫细胞细致分类，拟时序分析，RNA velocity，etc.
    

## Meta scRNA (Testing)
对宏基因组使用scRNA与Basic Pipeline不同；Basic Pipeline中已知样本来自某一生物，所以可以很简单的使用参考基因组进行每个细胞内、每个基因的定量；而宏基因组的潜在参考基因集过于庞大，耗费过量资源；且宏基因组使用scRNA技术的目的之一是希望得到更准确的细胞组成信息（现有Binning有时准确度堪忧），需求是对每一个cell进行准确的物种注释。

为了尽量缩小潜在参考基因集范围，可以参考相似研究的Meta Bulk注释提到的基因组；Tips: GTDB使用ANI进行分类，可以使用本地储存的文件，不用去NCBI再下载

其单细胞QC步骤一如前文所述。有两种或许可行的注释、定量方法： 
    * Anno via FastANI：当需要注释的细胞数量较少时，可以将其比对参考DB，根据ANI确定可能Taxa范围
    * Anno via Mapping：通过cdhit等对参考基因集进行去重，然后将scRNA数据map上去，根据细胞的mapping信息决定其物种注释(也许可以使用cellranger)

Tips：有时如果物种注释结果不理想，我们也可以进行单细胞水平的功能注释(GO,ARG,pathway...)

## 其它

* scATAC: 基于scRNA得到某种亚细胞的转录谱，或已知reference情况下；可以分析10x平台产生的单细胞水平ATAC数据
* Bulk mRNA 数据可以帮助验证scRNA数据的完整性；如果还有其它bulk多组学数据，可以尝试算一下相关性







## 参考
数据集汇总： https://www.jianshu.com/p/49e5cf91f819  

NBIS: https://www.jianshu.com/p/1e29e3b9a4ab  

Doublet: https://zhuanlan.zhihu.com/p/376439628

HVGs: https://www.jianshu.com/p/3d40c56e5fc8

Cell Circle： https://zhuanlan.zhihu.com/p/82654538   

Batch: https://www.jianshu.com/p/ebc328f9fb73   

