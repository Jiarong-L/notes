<style>
img{
    width: 60%;
}
</style>

官方提供了 [Scanpy tutorials](https://scanpy.readthedocs.io/en/stable/tutorials.html) 以及 [API描述](https://anndata.readthedocs.io/en/latest/api.html)

## Install
```
pip install scanpy
pip install leidenalg

pip install Cython
pip install pyproject
git clone git@github.com:bhargavchippada/forceatlas2.git  ## install fa2
python setup.py install    ## remove 'fa2/fa2util.pxd' from setup.py
```

## AnnData
![AnnData](Scanpy/img/AnnData.png)
```
adata.X = pd.read_csv(mtx_annotation)
adata.var['GeneAnno'] =           ## annotation of variables (genes)
adata.obs['CellAnno'] =           ## annotation of observations (cells)
```

## Tips

| 模块/操作 | 作用 | 说明 |
| -- | -- | -- |
| ```sc.read_10x_mtx``` | 读取[CellRanger](CellRanger.md)结果为AnnData | ```filtered_feature_bc_matrix/``` |
| ```sc.pp.---``` | 处理 | Filter、Normalize、Log、HVGs，直接修改Matrix/结果存入AnnData.var |
| ```sc.tl.---``` | 计算 | Umap等，结果存入AnnData.obs；相当于Seurat的meta.data |
| ```sc.pl.---``` | 作图 | -- |
| ```adata=adata[:,:].copy()``` | 手动Filter | ```adata[adata.obs.?? < ?, adata.var.?? < ?]``` |

* ```adata.raw = adata```把处理前的矩阵留存在'.raw'中，```adata.raw.to_adata()```进行调用
* 需要手动Filter得到HVGs的矩阵，再进行下一步
* Cluster的重命名需要修改pd.category类型:
```py
adata.obs['leiden'] = adata.obs['leiden'].cat.rename_categories({'0':'New0'})
```

## scRNA
示例数据：外周血单核细胞(pbmc)
```bash
wget https://cf.10xgenomics.com/samples/cell/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz
tar -xzf pbmc3k_filtered_gene_bc_matrices.tar.gz
ls filtered_gene_bc_matrices/hg19
### barcodes.tsv  genes.tsv  matrix.mtx
```
示例代码：[tutorial: pbmc3k](https://scanpy-tutorials.readthedocs.io/en/latest/pbmc3k.html)，操作记录：[Scanpy.ipynb](https://github.com/Jiarong-L/notes/tree/main/docs/Bioinfo/Blocks/Scanpy/Scanpy.ipynb)

与 [Seurat](Seurat.md)基本操作类似，得到Cluster与Markers；```sc.tl.paga``` 提供轨迹分析

参考：[PAGA轨迹推断](https://www.jianshu.com/p/0b2ca0e0b544)，[其它人的操作记录](https://www.jianshu.com/p/e22a947e6c60)


## Spatial: Visium 

示例代码：[tutorial: 10xVisium](https://scanpy-tutorials.readthedocs.io/en/latest/spatial/basic-analysis.html)


