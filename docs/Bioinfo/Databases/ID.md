

将不同数据库的注释结果对应起来


| -- | 常用对应关系 | -- |
| -- | -- | -- |
| [ID Mapping](https://www.uniprot.org/help/id_mapping) | UniProtKB/GI | 在线/命令行/py |
| [accession2taxid](ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/) | Accession/Taxid/GI | .gz |
| [filtered_goa_uniprot_all.gaf.gz](http://release.geneontology.org/) | UniProtKB/GO/GI | latest-->annotations-->.gz |
| [bioDBnet](https://biodbnet-abcc.ncifcrf.gov/db/db2db.php) | GI/KEGG/EC/... | 在线 |
| [g:Profiler](https://biit.cs.ut.ee/gprofiler/convert) | Ensemble | 在线，部分物种 |
| ```org.xx.eg.db + select()``` | ENTREZID/ENSEMBL/SYMBOL | R:AnnotationDbi |
| ```org.xx.eg.db + bitr()``` | ENTREZID/ENSEMBL/SYMBOL | R:clusterProfiler |
| ```getBM()``` | Ensemble:Gene/Transcript | R:biomaRt |





| ID | 说明 | 示例 |
| -- | -- | -- |
| Taxid | NCBI Taxonomy 所用ID | ```1``` root |
| [Ensemble ID](http://asia.ensembl.org/info/genome/stable_ids/prefixes.html) | ```ENS[SPE][X][11 number].[V]``` | ```ENSP00000339754.1``` P=Protein |
| [GI Number](https://www.ncbi.nlm.nih.gov/genbank/sequenceids/) | GeneBank的记录ID，可能Accession的不同版本会有不同GI号 | ```GI: 2462602239``` RNF180 |
| [Accession](https://www.ncbi.nlm.nih.gov/guide/howto/find-func-gene/) | refseq，nt，nr，(非冗余) | ```GenBank: XM_054352456.1``` RNF180 |
| [Entrez ID]() | 也称Gene ID，不同变异/位于不同物种中可能有不同Accession | ```GeneID: 285671``` RNF180 |
| Gene Symbol | 基因通用名称，或在Entrez ID前添加LOC前缀作为Symbol | -- |
| [UniProtKB Accession](https://www.uniprot.org/help/accession_numbers) | 提交记录，一个[Entry](https://www.uniprot.org/help/entry_name)可能对应多个Accession | ```A2BC19，P56559``` |
| [GO terms](https://geneontology.org/docs/GO-term-elements) | -- | ```GO:0005829``` |




其它参考：[将GEO里的探针转换为基因Symbol](https://www.bilibili.com/read/cv14560979/)


