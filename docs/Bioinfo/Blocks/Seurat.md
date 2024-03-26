<style>
img{
    width: 60%;
}
</style>

事实上[官方 Cheat Sheet](https://satijalab.org/seurat/articles/essential_commands) 已经提供了功能简记

Seurat v5 的尝试记录；简言之就是生成一个SeuratObject，相应处理计算得到的数据都存储于其中，官方同时提供了获取相应结果的方程；其中作图请见 [Seurat 5 官网 Data visualization](https://satijalab.org/seurat/articles/visualization_vignette)

## Install
```
install.packages('Seurat')
```

示例数据：外周血单核细胞(pbmc)
```bash
wget https://cf.10xgenomics.com/samples/cell/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz
tar -xzf pbmc3k_filtered_gene_bc_matrices.tar.gz
ls filtered_gene_bc_matrices/hg19
### barcodes.tsv  genes.tsv  matrix.mtx
```

示例代码：[Seurat 5 官网 pbmc 示例](https://satijalab.org/seurat/articles/pbmc3k_tutorial)

## scRNA

一些常用功能简记: 

### Load / Filtering by meta.data

* features 指基因，variable features 指 HVGs

* subset进行各种filtering操作
    - ```subset=``` 提取Genes（via filtering meta.data -- 各种表达式）
    - ```cells=```提取细胞，```idents=```提取Clusters （via name/list）

```R
library(Seurat)

## 00.Load Data: colname_AAACAT  rowname_Gene 
pbmcRawData <- Read10X(data.dir = "./filtered_gene_bc_matrices/hg19/")

## 00.Init SeuratObject & raw Filtering
pbmc <- CreateSeuratObject(counts = pbmcRawData, 
                          project = "pbmc3k", 
                          min.cells = 3,       ## Filter off Genes: Appear in >3 Cells
                          min.features = 200,  ## Filter off Cells: Appear in >200 Genes
                          meta.data = NULL
                          )


## Sum geneFrature rows with pattern (^MT-) 
## and Assign result to meta.data as 'percent.mt'
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")

## Filtering Cells by meta.data
pbmc <- subset(pbmc, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)


### Plot meta.data
p1 <- VlnPlot(pbmc, features = c("percent.mt"), ncol = 1)
p2 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "percent.mt")
p1 + p2
```


### Normalize/Scale/HVGs
注:  ```SCTransform() = NormalizeData() + FindVariableFeatures() + ScaleData()```
```R
## Normalizing the data 
##   -- equals to:  pbmc[["RNA"]]$data <- NormalizeData(pbmc[["RNA"]]$counts)
pbmc <- NormalizeData(pbmc)

## Find top2000 HVGs: Active assay now have 2000 variable features
pbmc <- FindVariableFeatures(pbmc, selection.method = "vst", nfeatures = 2000)
HVGsNameList <- VariableFeatures(pbmc)

## Scale: remove unwanted sources of variation
##     -- Zero-centered or Mean-subtraction
##     -- Save to:  pbmc[["RNA"]]$scale.data     Layer
pbmc <- ScaleData(pbmc, 
          features = rownames(pbmc),        ##  default only HVGs, here all genes
          vars.to.regress = "percent.mt",   ##  ‘regress out’ heterogeneity associated with mitochondrial contamination
          )

### Plot HVGs
pHVGs <- VariableFeaturePlot(pbmc)
LabelPoints(plot = pHVGs, points = head(HVGsNameList, 10), repel = TRUE)
```




### PCA/Clustering
一般先PCA，然后基于降维结果进行KNN聚类；如果进行UMAP，一般是基于PCA的结果（当然也可以使用原数据）
```R
## result in pbmc[["pca"]] pbmc[["umap"]]
pbmc <- RunPCA(pbmc, features = HVGsNameList)
pbmc <- RunUMAP(pbmc, reduction = "pca", dims = 1:10) ## Using PCA's first 10 dim (otherwise features=xxx to use RNA table), Note：umap has only 2 dim as the result

## plot PC's SD to choose dims of use (not applicable for umap)
ElbowPlot(pbmc, reduction = "pca")

## construct a KNN graph based on the euclidean distance in Embedded space
pbmc <- FindNeighbors(pbmc, reduction = "pca", annoy.metric = "euclidean", dims = 1:10)

## Clustering based on KNN graph
pbmc <- FindClusters(pbmc, resolution = 0.5)

### Plot
DimPlot(pbmc, reduction = "pca")
```


如果需要修改ClusterID：（```Idents(pbmc)``` 获取每个Cell对应的ClusterID）
```R
## Rename clusters (After find markers to get its Cell type Annotation)
pbmc <- RenameIdents(pbmc, '0' = 'A', '2' = 'C')    ## levels(pbmc) to check
```


如果需要提取降维结果 Matrix：
```R
Embeddings(pbmc, reduction = "pca")   ## pbmc[['pca']]@cell.embeddings
Loadings(pbmc, reduction = "pca")     ## pbmc[['pca]]@feature.loadings
```


### Find markers of Clusters

将某个clusterA与另一个/所有cluster进行对比，选取其中差异显著者(p_val_adj & avg_log2FC>0.1 & clusterA中满足最小存在量)为 clusterA的 Marker Genes 

```R
cluster2_vs_All.markers <- FindMarkers(pbmc, ident.1 = 2)
cluster2_vs_5.markers <- FindMarkers(pbmc, ident.1 = 2, ident.1 = c(5))

All.markers <- FindAllMarkers(pbmc, only.pos = TRUE)

### Plot Gene Expression in each clusters  & Coloring the genes in PCA plot
VlnPlot(pbmc, features = rownames(All.markers)[1:2])
FeaturePlot(pbmc, features = rownames(All.markers)[1:2], reduction="pca")
```



## Multimodal

假设**同一细胞**有多种数据类型，它们被存储于同一个 SeuratObject中（2个Assay5），于是可以基于scRNA数据得到 Cluster（Cell Type），然后再基于Cell Type信息分析/展示其他数据。或者，也可以[基于两种模态的加权组合对细胞进行聚类（WNN graph while clustering）](https://satijalab.org/seurat/articles/weighted_nearest_neighbor_analysis): ```FindMultiModalNeighbors()```

已知一些方法可以采集来自**同一细胞**的多组学数据：CITE-seq = RNA + ADT；10x multiome kit = RNA + ATAC

首先，需要将多组学数据集整合到 scRNA ref Dastaset 上


### Integration: +Protein

[在低维空间中寻找 Anchors 以整合两个不同组学数据集](https://satijalab.org/seurat/articles/multimodal_reference_mapping): ```FindTransferAnchors```: 两个数据集的 features(Gene/row) 必须相同，且已经记录了降维操作的结果

```R
## 00. SCTransform() & PCA both SeuratObject
## 01. Find Anchors: SeuratObjects must share the same features(Gene/row)
anchors <- FindTransferAnchors(
  reference = pbmcRef,
  query = pbmc,
  normalization.method = "LogNormalize",   ## Use Layer: data 
  reference.reduction = "pca",             ## Use previously calculated PCA result
  dims = 1:50
)

## 02. Map: transfer cell type labels and Ref data from the reference to the query
pbmcMerged <- MapQuery(
  anchorset = anchors,
  query = pbmc,
  reference = pbmcRef,
  refdata = list(                     ## What to transfer: newAssayinQurey = "Name of the metadata field or assay in ref"
    nCount_RNA_New = "nCount_RNA",    ##                                    or: (??)The reference data itself as either a vector where the names correspond to the reference cells, or a matrix, where the column names correspond to the reference cells.
    MT_New = "percent.mt"
  ),
  reference.reduction = "pca", 
  reduction.model = NULL            ## DimReduc object that contains the umap model, 
                                    ## e.g. reduction.name="wnn.umap" when running RunUMAP (??)
)


    # > pbmcMerged
    # An object of class Seurat
    # 15450 features across 2638 samples within 2 assays
    # Active assay: RNA (13714 features, 2000 variable features)
    #  3 layers present: counts, data, scale.data
    #  2 other assays present: prediction.score.nCount_RNA_New, prediction.score.MT_New
    #  2 dimensional reductions calculated: pca, ref.pca
```


### Integration: +ATAC

[bridge integration](https://satijalab.org/seurat/articles/seurat5_integration_bridge) 整合 ATAC 与 RNA

1. ```PrepareBridgeReference```
2. ```FindBridgeTransferAnchors```
3. ```MapQuery```

或先用 [Signac](./Signac.md) 将Peak matrix 转换为 Activity matrix（假设基因的表达活性可以简单的通过基因上下游2kb范围内覆盖的reads数的加和进行定量，需要先通过GTF/EnsDb得到GRanges注释）；参考[Seurat5 scATAC Integration](https://satijalab.org/seurat/articles/seurat5_atacseq_integration_vignette) 将 scRNA-seq 的 label 转移给 scATAC-seq

1. ```FindTransferAnchors```
2. ```TransferData```


### Use: +Protein

* [scRNA + ADT(antibody-derived tags) Protein](https://satijalab.org/seurat/articles/multimodal_vignette)
    - 可以Plot出 ADT Protein 在scRNA数据的降维空间里的丰度
    - 可以寻找 scRNA Clusters 的 Protein Markers，可能意味着这个Cell Type 的 Cell Surface Protein Markers

注：需要分别对二者Normalize/Scale


## Batch Correction

参考 [Seurat integration_introduction](https://satijalab.org/seurat/articles/integration_introduction)
```R
obj <- IntegrateLayers(
  object = obj, method = CCAIntegration,
  orig.reduction = "pca", new.reduction = "integrated.cca",
  verbose = FALSE
)

obj <- JoinLayers(obj)                 ## collapses the individual datasets together and 
                                       ## recreates the original counts and data layers


## CCAIntegration 适用于不同数据集中细胞类型保守的情况，有可能过度对齐
## RPCAIntegration 适用于不同数据集中细胞类型差别较大的情况
## HarmonyIntegration 
## FastMNNIntegration
## scVIIntegration       ## install.packages("reticulate")  ## also scvi-tools
```

随后 Clustering & **FindConservedMarkers**（或者FindMarkers）
```R
obj <- FindNeighbors(obj, reduction = "integrated.cca", dims = 1:30)
obj <- FindClusters(obj, resolution = 1)
obj <- RunUMAP(obj, dims = 1:30, reduction = "integrated.cca")
cluster2_vs_All.markers <- FindConservedMarkers(obj, ident.1 = 2, grouping.var = "stim", verbose = FALSE)
```


其它信息：
```
MNN/fastMNN：使用PCA降维矩阵/原始表达矩阵计算细胞之间的余弦距离、生成互近邻的集合、寻找MNN pairs、矫正对齐；适用于不同数据集中细胞类型保守的情况
    - 参考 https://cloud.tencent.com/developer/article/1814115
    - Seurat Anchor: CCA+MNN --- FindIntegrationAnchors()+IntegrateData()

LIGER：iNMD分解矩阵，根据此空间内的距离（maximum factor loadings）建立 neighbors graph；适用于不同数据集中细胞类型差别较大的情况
    - 参考 https://cloud.tencent.com/developer/article/1814109

Harmony：在PCA空间进行soft k-means clustering；节约运行时间
    - 参考 https://cloud.tencent.com/developer/article/1814104
```


## SeuratObject

具体可参考 [Seurat v5 and Assay5 introductory vignette](https://satijalab.org/seurat/articles/seurat5_essential_commands)

* SeuratObject 是[一层一层的结构](https://www.jianshu.com/p/0c4bc6a932b2): ```SeuratObject@L1$L2```
* 得到 meta.data: ```colnames(pbmc_small[[]])```
* 得到 Active Assay's layer names: ```Layers(pbmc)```等同于```Layers(pbmc[["RNA"]])```
* 得到 Cell Names: ```colnames(pbmc)```

* 同时从某个layer中提取 assay列 和 meta.data列: 
```R
FetchData(object = pbmc, layer = "counts", vars = c("rna_MS4A1", "PC_1", "nCount_RNA"))
```

* 查看Assay名字：```Assays(pbmc)```
* Active Assay: Multimodal/MultiAssay时需要切换Assay
```R
pbmc@active.assay            ## Current Active Assay：[1] "RNA"
DefaultAssay(pbmc) <- "RNA"  ## set Active Assay as "RNA"
```

* ```pbmc@assays$RNA``` 以下两种方式无差别
```R
class(pbmc@assays$RNA)    ## "Assay5"
class(pbmc[['RNA']])      ## "Assay5"

class(pbmc[["RNA"]]$data)  ## "Matrix"
```


* ```pbmc@meta.data``` 以下三种方式有差别
```R
## colnames(pbmc@meta.data)

head(pbmc@meta.data$nCount_RNA) ## "numeric" list
head(pbmc$nCount_RNA)           ## "numeric" list with names: pbmc$nCount_RNA['TTTCTACTGAGGCA-1']
head(pbmc[['nCount_RNA']])      ## "data.frame" 
```




## Spatial

### Visium

BayesSpace聚类：https://zhuanlan.zhihu.com/p/393981571  
https://www.jianshu.com/p/9206ba12c854

3.2!!! https://www.jianshu.com/p/13d7ea85bd71

https://satijalab.org/seurat/articles/spatial_vignette.html











