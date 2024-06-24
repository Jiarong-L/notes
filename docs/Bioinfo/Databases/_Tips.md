---
title: Database Tips
---



* 注释方法一般为比对数据库，或者根据DB生成kmer/hmm；一些工具如kraken也可以定量reads
* 可以自己从各个数据库中合并/筛选项目所需（记得CDHIT去冗余）
* 参考 [ID Mapper](ID_Mapper.md) 将不同数据库的ID对应起来；虽然大部分数据库的最终来源很可能都是NCBI，但由于时间版本不同、序号可能不一致，需要注意
* 如果需要数据来测试工具，参考[此处笔记](SRA.md)
* [ENCODE](https://www.encodeproject.org/) 内含众多Epi相关数据，适用于训练DL模型


| -- | DB数据类型 | 包含物种 | 查询数据 | 查询工具 | 其它说明 |
| -- | -- | -- | -- | -- | -- |
| [Taxonony](Taxonony.md) | 分类学索引表格文本 | All | taxid/Name(可能重复) | -- | e.g.界门纲目科属种的对应关系 |
| PDB | 蛋白+三维结构 | -- | -- | -- | -- |
| [Swiss-Prot](https://www.uniprot.org/help/downloads) | Protein序列，UniParc非冗余蛋白序列-->UniprotKB带注释：其中Swiss-Prot人工注释，TrEMBL计算机注释；UniRef按不同相似度聚类，进一步去冗余，注释优先选取Swiss-Prot  | -- | -- | -- | Gene水平的物种注释 |
| [NT](NT_NR.md) | 非冗余 Gene序列（DNA） | All | CDS 序列 | -- | Gene水平的物种注释 |
| [NR](NT_NR.md) | Protein序列（翻译自NT） | All | Protein 序列 | -- | Gene水平的物种注释 |
| [GTDB](GTDB.md) | -- | -- | MAGs/Cell | GTDBtk | 细胞水平的物种注释 |
| [CAT](https://github.com/dutilh/CAT) | -- | -- | Contig序列 | -- | Contig水平的物种注释 |
| BAT | -- | -- | Cell/MAG | -- | Cell/MAG的物种注释 |
| [SILVA](https://www.arb-silva.de/download/arb-files/) | rRNA | Bacteria, Archaea, Eukarya | 16S/18S/... Amplicon Reads | 建议blast/uclust [Archive-Exports](https://www.arb-silva.de/no_cache/download/archive/release_138/release_138_1/Exports/) 中的fasta文件 | 多用于rRNA Amplicon物种注释（但新版本错误很多），或去除数据中的rRNA序列 |
|  |  |  |  |  |  |
| ISFinder | 可移动元件 | 细菌、古菌 | Contigs 序列 | -- | 可移动元件不全在CDS内部 |
|  |  |  |  |  |  |
| [KEGG](KEGG.md) | -- | -- | CDS 序列 | -- | Gene所属的Pathway注释 |
| [GO](GO.md) | -- | -- | CDS 序列 | -- | Gene的生物功能注释(Gene Ontology) |
| [CARD](ARG.md#card) | -- | -- | CDS 序列 | blast最佳，官方的rgi没有成功 | ARGs基因注释 |
| [SARG](ARG.md#sarg) | -- | -- | Reads | ARGs-OAP | 提供ARGs自定义单位的定量；也可以用于 blast CDS |
| [CAZy](CAZy.md) | 蛋白序列 | Bacteria, Eukaryota, Archaea, Viruses | 蛋白序列 | -- | 将碳水化合物活性酶归入不同蛋白质家族 |
| [PHI-base](PHI.md) | 蛋白序列 | -- | -- | -- | 基因对病原菌致病能力的影响 |
| -- | -- | -- | -- | -- | -- |
|  |  |  |  |  |  |
| [InterPro](Homologous.md) | Gene Family(Pfam) + 结构 + 功能 多个数据库的整合 | -- | 蛋白序列 | InterProScan | 包括了Pfam |
| [EggNOG](Homologous.md) | 不同分类水平的 Orthogonal Group（COG的拓展） | -- | 蛋白序列 | eggNOG-mapper | 更新慢 |
| String | 蛋白质互作关系 | [见??](https://stringdb-downloads.org/download/species.v12.0.txt) | id/蛋白序列 | -- | 提供 ```aa1 aa2 SCORE``` 列表 + 相关aa序列，见 [String](https://cn.string-db.org/) 网站 download 页面说明 |



[VFDB: virulence factors of bacterial pathogens](http://www.mgc.ac.cn/VFs/main.htm)


