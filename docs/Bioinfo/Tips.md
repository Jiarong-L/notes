


## About Blocks
一些工具的使用笔记，待整理

## About Databases

当然，也可以自己从各个数据库中合并/筛选项目所需；虽然大部分数据库的最终来源很可能都是NCBI，但由于时间版本不同、序号可能不一致，需要注意

此外，可以用 [ID Mapper](./Databases/ID.md) 将不同数据库的ID对应起来。



| -- | DB数据类型 | 包含物种 | 查询数据 | 自有查询工具 | 其它说明 |
| -- | -- | -- | -- | -- | -- |
| [Taxonony](./Databases/Taxonony.md) | 分类学索引表格文本 | All | taxid/Name(可能重复) | -- | e.g.界门纲目科属种的对应关系 |
| [NT](./Databases/NT_NR.md) | 非冗余 Gene序列（DNA） | All | CDS 序列 | -- | Gene水平的物种注释 |
| [NR](./Databases/NT_NR.md) | Protein序列（翻译自NT） | All | Protein 序列 | -- | Gene水平的物种注释 |
| [GTDB](./Databases/GTDB.md) | -- | -- | MAGs/Cell | GTDBtk | 细胞水平的物种注释 |
| CAT_BAT | -- | -- | Contig序列 | -- | Contig水平的物种注释 |
| -- | -- | -- | -- | -- | -- |
| SILVA | rRNA | Bacteria, Archaea, Eukarya | 16S/18S/... Amplicon | -- | 多用于rRNA Amplicon物种注释（但新版本错误很多），或去除数据中的rRNA序列 |
| -- | -- | -- | -- | -- | -- |
| [KEGG](./Databases/KEGG.md) | -- | -- | CDS 序列 | -- | Gene所属的Pathway注释 |
| GO | -- | -- | CDS 序列 | -- | Gene的生物功能注释(Gene Ontology) |



如果需要测试工具，可以从[SRA](./Databases/SRA.md)获得数据



## About Gallary
一般使用ggplot就足够了，部分示例见 [Gallary_overview](./Gallary/Gallary_overview.md)

## About Pipelines
一些常见流程

