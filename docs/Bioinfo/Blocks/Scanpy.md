<style>
img{
    width: 60%;
}
</style>


## Install
```
pip install "scanpy[leiden]"

import scanpy as sc
```

## AnnData
![AnnData](Scanpy/img/AnnData.png)
```
adata.X = pd.read_csv(mtx_annotation)
adata.var['GeneAnno'] =           ## annotation of variables (genes)
adata.obs['CellAnno'] =           ## annotation of observations (cells)
```
本次以[CellRanger](../CellRanger)-filtered_feature_bc_matrix 输出为示例：[download](http://cf.10xgenomics.com/samples/cell-exp/1.1.0/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz)



## Pipeline

* Load AnnData
* QC
    * adata.var_names_make_unique()
    * sc.pp.filter_cells(adata, min_genes=200)
    * sc.pp.filter_genes(adata, min_cells=3)
    * 








## 参考
Scanpy：https://scanpy.readthedocs.io/en/stable/tutorials.html   

!!!    
https://www.jianshu.com/p/e22a947e6c60


https://www.jianshu.com/p/0b2ca0e0b544


