

处理scATAC数据，与Seurat格式通用
 

## Install
```R
BiocManager::install("Rsamtools")
install.packages("Signac")
BiocManager::install("GenomicRanges")
BiocManager::install("EnsDb.Hsapiens.v75")
BiocManager::install("biovizBase")
BiocManager::install("genomation") ##
```


## With Seurat

[Signac + Seurat](https://stuartlab.org/signac/articles/pbmc_vignette) 处理PBMC scRNA+scATAC 数据

```R
library(Seurat)
library(Signac)


peaksMTX <- Read10X_h5("atac_v1_pbmc_10k_filtered_peak_bc_matrix.h5")
meta <- read.table("atac_v1_pbmc_10k_singlecell.csv", sep = ",", header = TRUE, row.names = 1, stringsAsFactors = FALSE)


chrom_assay <- CreateChromatinAssay(
  counts = peaksMTX,
  sep = c(":", "-"),
  min.cells = 10,
  min.features = 200
)

pbmc <- CreateSeuratObject(
  counts = chrom_assay,
  assay = "peaks",
  meta.data = meta
)


### --- load GRanges as annotations ---  ### 

Annotation(pbmc) <- annotations


### --- QC & Filtering ---  ### 


pbmc <- RunTFIDF(pbmc)                             ## ---- Normalize & scale via Lsi
pbmc <- FindTopFeatures(pbmc, min.cutoff = 'q0')   ## exclude dim1 since it correlats with sequencing depth
pbmc <- RunSVD(pbmc)


pbmc <- RunUMAP(object = pbmc, reduction = 'lsi', dims = 2:30)      ## ---- Dim reduction & clustering
pbmc <- FindNeighbors(object = pbmc, reduction = 'lsi', dims = 2:30)
pbmc <- FindClusters(object = pbmc, verbose = FALSE, algorithm = 3)



gene.activities <- GeneActivity(pbmc)      ## ---- Switch to GeneActivity Mtx
pbmc[['ACTIVITY']] <- CreateAssayObject(counts = gene.activities)

### Normalize & scale ACTIVITY ---  ### 
### Get scRNA's metaData/GetAssayData(): FindTransferAnchors + TransferData ---  ### 
```



## GRanges Object

上文```Annotation(pbmc) <- annotations```中，annotations是GRanges Object，示例：
```R
BiocManager::install("EnsDb.Hsapiens.v75")
library(EnsDb.Hsapiens.v75)
library(Signac)
annotations <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v75)
seqlevels(annotations) <- paste0('chr', seqlevels(annotations))
genome(annotations) <- "hg19"
Annotation(pbmc) <- annotations

# > annotations[1]
# GRanges object with 1 range and 5 metadata columns:
#                   seqnames        ranges strand |           tx_id   gene_name
#                      <Rle>     <IRanges>  <Rle> |     <character> <character>
#   ENSE00001489430     chrX 192989-193061      + | ENST00000399012      PLCXD1
#                           gene_id   gene_biotype     type
#                       <character>    <character> <factor>
#   ENSE00001489430 ENSG00000182378 protein_coding     exon
```

如果自己提供注释文件，可以使用 [genomation](https://rdrr.io/bioc/genomation/f/vignettes/GenomationManual.Rmd) 将其 load 为 GRanges object

```
library(genomation)
gff = gffToGRanges("Homo_sapiens.GRCh37.82.gtf")
seqlevels(gff) = paste0("chr",seqlevels(gff))     ## 1 ==> chr1
genome(gff) <- "GRCh37"
```

实在不行的话也可以试试其它包的 ```ensDbFromGtf(gtf, outfile, path, organism, genomeVersion, version)``` 或者 ```makeGRangesFromGTF```


## Fragment file

如果要计算 QC Metrics，则需要输入[BED-like Fragment file](https://support.10xgenomics.com/single-cell-atac/software/pipelines/latest/output/fragments)；它是```cellranger-atac count```的输出（```outs/```），也可以用[sinto](https://timoast.github.io/sinto/basic_usage.html#create-scatac-seq-fragments-file)处理bam文件得到
```
chr1    10066   10279   TTAGCTTAGGAGAACA-1      2
chr1    10072   10279   TTAGCTTAGGAGAACA-1      2
chr1    10079   10316   ATATTCCTCTTGTACT-1      2
chr1    10084   10340   CGTACAAGTTACCCAA-1      1
chr1    10085   10271   TGTGACAGTACAACGG-1      1
chrom  chrStart chrEnd    CellBarcode        readSupport
```

## 一些参考
```bash
## peaksMTX
wget http://cf.10xgenomics.com/samples/cell-atac/1.0.1/atac_v1_pbmc_10k/atac_v1_pbmc_10k_filtered_peak_bc_matrix.h5
## metadata
wget http://cf.10xgenomics.com/samples/cell-atac/1.0.1/atac_v1_pbmc_10k/atac_v1_pbmc_10k_singlecell.csv
## fragments file
wget https://cf.10xgenomics.com/samples/cell-atac/1.0.1/atac_v1_pbmc_10k/atac_v1_pbmc_10k_fragments.tsv.gz
## GRCh37 genes
wget ftp://ftp.ensembl.org/pub/grch37/release-84/gtf/homo_sapiens/Homo_sapiens.GRCh37.82.gtf.gz
gunzip Homo_sapiens.GRCh37.82.gtf.gz
## scRNA MTX with celltype Anno
wget http://cf.10xgenomics.com/samples/cell-exp/3.0.0/pbmc_10k_v3/pbmc_10k_v3_filtered_feature_bc_matrix.h5
```
