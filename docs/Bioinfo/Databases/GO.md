

[Gene Ontology](https://geneontology.org/docs/ontology-documentation/) 不提供FASTA序列，故而网上的教程一般推荐EggNOG（太老）和 InterProScan，不过也可以将其它数据库的注释转换为GO ID：

1. 进入[latest-->annotations](http://release.geneontology.org/)下载 ```filtered_goa_uniprot_all.gaf.gz```: [GAF格式](http://geneontology.org/docs/go-annotation-file-gaf-format-2.2/)来源包括 ```UniProtKB  RNAcentral  ComplexPortal```，或许可支持从UniProtKB注释转换
2. [GO Cross-references](https://geneontology.org/docs/download-mappings/)提供EC Number 等的转换
3. 参考[ID Mappers](./ID.md)：可以从nr注释里转换



## Setup

建议将AA序列比对到UniProtKB（或提取3个数据库中对应条目构建数据库）后转为 GO ID

```bash
wget -c http://release.geneontology.org/2024-01-17/annotations/filtered_goa_uniprot_all.gaf.gz
wget -c https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
wget -c https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz
cat uniprot_sprot.fasta.gz  uniprot_trembl.fasta.gz > uniprot.fasta.gz

diamond makedb --in uniprot.fasta.gz -d uniprot
diamond blastp --db uniprot -q input.fasta -o output.tsv --max-target-seqs 1 --evalue 1e-5 --min-score 60 --block-size 40.0 --index-chunks 1
```

## obo

下载[.obo格式](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html)的Ontology文件，用 goatools 解析：一般使用 level2 和 namespace 的信息，于是提示每个条目的 level2 先祖（可能多个，也可能无）
```py
## wget -c https://purl.obolibrary.org/obo/go/go-basic.obo
## pip install goatools
import pandas as pd
from goatools.obo_parser import GODag
obodag = GODag("go-basic.obo")   ## obodag[id].level  :  0-12

L2 = set([id for id in obodag if obodag[id].level == 2])
goDict = {}
for id in obodag:
    goDict[id] = {
        'name':obodag[id].name,
        'namespace':obodag[id].namespace,
        'L2GO': ';'.join(list(set(obodag[id].get_all_parents()) & L2))
    }

godf = pd.DataFrame(goDict).T.reset_index(inplace=False)
```

## Enrichment

如果可以转换为 EntrezID，则可以使用 [R_enrichGO](https://www.rdocumentation.org/packages/clusterProfiler/versions/3.0.4/topics/enrichGO): 只需输入基因集、背景基因集（物种全部基因）

也可以自行计算横坐标:  KEGG同理
```
InputGene: 一般是差异分析得到的差异基因集 & 有GO注释                       KEGG/GO Term
BackgroundG：物种/meta全部的基因 & 有GO注释                                 a |            *
                                                                          b | *
                                                                         cc1|      *
GeneRatio = 富集到这个GO条目上的InputGene / 所有InputGene                  mf1|   *
BgRatio = 富集到这个GO条目上的BackgroundG / 所有BackgroundG                 . |
                                                                          . |
Enrichment Factor = GeneRatio/BgRatio                                     . |___________________
也称 Fold enrichment                                                          Enrichment Factor
```

