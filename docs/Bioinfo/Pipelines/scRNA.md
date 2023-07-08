


## Links
* 示例数据来源：https://www.10xgenomics.com/resources/datasets
* 数据库（TBA）
    * CellMarker：http://biocc.hrbmu.edu.cn/CellMarker/index.jsp
    * PanglaoDB：https://panglaodb.se/index.html
    * SingleR datasets


## Pipeline (mainly Seurat)
* QC
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
* Batch Correction
    * Opt.1: CCA+MNN --- Seurat: FindIntegrationAnchors()+IntegrateData()
    * Opt.2: Harmony
* Normalize & Scale
    * NormalizeData() --- "LogNormalize"
    * FindVariableFeatures() --- HVGs: GeneA_cellA v.s. GeneA_Overall
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
* Clustering
    * PCA
    * UMAP/tSNE (PCA result as input)
    * Clustering (PCA result as input)
    ```
    scRNA <- FindNeighbors(scRNA, dims = pc.num)
    scRNA <- FindClusters(scRNA, resolution = 0.5)
    ```
* Cell-type Annotation
    * Find marker genes --- Diff-expr genes: cluster v.s. clusters
    * Annotate clusters (cell types) based on marker genes
        * SingleR() + HumanPrimaryCellAtlasData(label.main)/CellMarker/PanglaoDB/Papers...
    * Tips：在这个水平上进行一些常规的分析(cluster间的比较)，比方说KEGG、GO富集分析，差异基因表达分析（cell-type间），etc.
* Sub-Clustering
    * Pick a cluster (cell-type), Clustering & Annotate
        * SingleR() + MonacoImmuneData(label.fine) to sub-clusters
    * Tips：假设这些sub-type都来自同一个cell-type，在这个水平上进行一些更加细致的操作，比如：对免疫细胞细致分类，拟时序分析，RNA velocity，etc.
    













## 参考
数据集汇总： https://www.jianshu.com/p/49e5cf91f819  

NBIS: https://www.jianshu.com/p/1e29e3b9a4ab  

Doublet: https://zhuanlan.zhihu.com/p/376439628


HVGs: https://www.jianshu.com/p/3d40c56e5fc8

Cell Circle： https://zhuanlan.zhihu.com/p/82654538   



