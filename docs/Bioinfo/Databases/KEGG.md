


关联：NR SWissport GO KEGG 已实现相互注释


### Links

参考[KEGG REST API](https://www.kegg.jp/kegg/rest/keggapi.html)的提示，pathway prefix 主要包括：
```bash
map: default
ko - reference pathway map linked to KO entries (K numbers)
rn - reference pathway map linked to REACTION entries (R numbers)
ec - reference pathway map linked to ENZYME entries (EC numbers)
org (three- or four-letter organism code) - organism-specific pathway map linked to GENES entries (gene IDs)
```

KEGG数据库-人类相关：
```bash
    ftp://ftp.genome.jp/pub/db/
    http://rest.kegg.jp/link/hsa/ko     大K和人hsa的对应关系
    http://rest.kegg.jp/list/hsa
    http://rest.kegg.jp/list/ko           大K的功能描述和酶信息
    http://rest.kegg.jp/list/pathway         map/ko 功能描述
    http://rest.kegg.jp/list/pathway/hsa     hsa-ko功能描述
    http://rest.kegg.jp/link/pathway/ko         大K和ko的对应关系
    http://rest.kegg.jp/link/pathway/compound   化合物C编号和ko的对应关系
    http://rest.kegg.jp/link/ko/module          大K和M的对应关系

    https://www.kegg.jp/brite/br08902       kegg层级文件
    https://www.kegg.jp/kegg-bin/show_brite?br08001.keg   化合物功能分类
```

另外，常用：[ko01200](https://www.kegg.jp/dbget-bin/www_bget?pathway+ko01200)
```
Carbon metabolism - ko01200
Methane metabolism - ko00680
Nitrogen metabolism - ko00910
Sulfur metabolism - ko00920
```


### Setup DB

1. 下载 K(enzyme), ko(pathway/map) 及其对应关系: 双方并非一一对应关系；K可以参与多个ko，ko也可以包含多个K
2. 使用 [Collect_pathway_info.py](./KEGG/Collect_pathway_info.py) 收集 pathway 中的 layer info(CLASS)
3. 制作 K(enzyme), ko(pathway/map) 关系的映射文件，单行对应为一个K/ko对应的所有、以','分割
```bash
## relation
wget -c http://rest.kegg.jp/link/ko/pathway -O ko_Ks

## koxxx pathway
wget -c http://rest.kegg.jp/list/pathway                                  ## 570
grep map ko_Ks |cut -f1 | cut -d ':' -f2 |sort|uniq |wc -l           ## 486

## Kxxx enzyme 
wget -c http://rest.kegg.jp/list/ko               ## 26696
cut -d ':' -f3 ko_Ks |sort|uniq |wc -l       ## 14019


mkdir map_folder
cd map_folder
cut -f1 ../pathway |cut -f2 -d ':'  |while read dd ; do wget -c http://rest.kegg.jp/get/$dd ;sleep 1; done
cd ..

python3 Collect_pathway_info.py  pathway  map_folder  pathway_info.xls


rm ko_allK
less pathway| cut -f1|sort | uniq| while read dd ; do echo -e "$dd\t\c" >> ko_allK; grep $dd ko_Ks  | sed 's/ko://g' |  awk '{printf $2 ","}' >> ko_allK; echo '' >> ko_allK; done


rm K_allko
less ko| cut -f1|sort | uniq| while read dd ; do echo -e "$dd\t\c" >> K_allko; grep $dd ko_Ks| grep 'map' | sed 's/path://g' |  awk '{printf $1 ","}' >> K_allko; echo '' >> K_allko; done


## grep map ko_Ks | sed 's/path://g'  | sed 's/ko://g'  | awk '{print $2,$1}'  | sort |join - ko |head
## less pathway_info.xls |cut -f 1,3,4,5 |less
## awk -F '\t' '{if ($3!="-" && $4!="-") print ($1,$3,$4,$5)}'  pathway_info.xls |  less
## 使用map0000而不是ko0000，只是因为官方提供的是map000
## Layer示例：ko01100无CLASS，ko05416有CLASS
```


## Anno

### kofam_scan
Install: 
```bash
wget -c ftp://ftp.genome.jp/pub/db/kofam/ko_list.gz
wget -c ftp://ftp.genome.jp/pub/db/kofam/profiles.tar.gz
gunzip ko_list.gz
tar -xzf profiles.tar.gz
KO_LIST=$PWD/ko_list
PROFILE_DIR=$PWD/profiles/

conda create -n kofam -c bioconda kofamscan     ##  hmmer parallel ruby
conda activate kofam
```

Use:
```bash
exec_annotation uniqGeneSet.faa -o kegg.txt -p $PROFILE_DIR -k $KO_LIST
```

Output: kegg.txt；多个hits，选E-value最优一个
```bash
# gene name           KO     thrshld  score   E-value KO definition
#-------------------- ------ ------- ------ --------- ---------------------
  GeneA        K00121  619.83  560.5  7.2e-172 S-(hydroxymethyl)glutathione dehydrogenase / alcohol dehydrogenase [EC:1.1.1.284 1.1.1.1]
  GeneA        K00001  345.97  308.1   2.5e-95 alcohol dehydrogenase [EC:1.1.1.1]
  GeneA        K00055  389.00  305.5   8.8e-95 aryl-alcohol dehydrogenase [EC:1.1.1.90]
  GeneA        K00153  383.77  276.3   7.8e-86 S-(hydroxymethyl)mycothiol dehydrogenase [EC:1.1.1.306]
```




## KEGG Graph
对于一些关注基因(e.g.差异表达),[Color tool](https://www.genome.jp/kegg/mapper/color.html)可在线标注颜色，或者[使用url控制颜色](https://www.kegg.jp/kegg/docs/color_url.html)，本地可使用使用[pathview R包](https://zhuanlan.zhihu.com/p/601451821),或者也可[下载KGML](https://www.kegg.jp/kegg/rest/keggapi.html)后用[cytoscape-KEGGscape](https://zhuanlan.zhihu.com/p/371399566)绘制（参考：[KEGGscape/py4cytoscape](https://keggscape.readthedocs.io/en/latest/pythonscripting.html),[Dash Cytoscape](https://dash.plotly.com/cytoscape)）。


### KGML
[理解KGML](https://cloud.tencent.com/developer/article/1626035)，[KGML颜色说明](https://www.kegg.jp/kegg/docs/color_gui.html)  
```
cd /mnt/d/WSL_dir/home/miniconda3/envs/r-base/lib/R/library/pathview/extdata/

for dd in ko00010 ko00600 ko04110; do 
wget https://rest.kegg.jp/get/$dd/kgml -O $dd.kgml;
wget https://rest.kegg.jp/get/$dd/image -O $dd.png;
done
```

其它使用：parser KGML文件，然后用 [graphviz](https://graphviz.readthedocs.io/en/stable/manual.html) 画箭头图，示例：[kegg_graphviz.py](./KEGG/kegg_graphviz.py) --TBA


### pathview
Install:
```R
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("pathview")

browseVignettes("pathview")
```

[Usage](https://www.rdocumentation.org/packages/pathview/versions/1.12.0/topics/pathview): 
```R
library("pathview")

KGML_PATH = "/mnt/d/WSL_dir/workdir/KEGG/tt/ko04110.kgml"
IMG_FOLDER = "."
ko_ID = "ko04110"                ## ko_ID.kgml must in IMG_FOLDER
OUT_SUFFIX = "myRed"

node.data=node.info(KGML_PATH)
plot.data.gene = node.map(mol.data=NULL, node.data, node.types="ortholog")   ## ortholog/gene/...
COLOR_LIST = rep('red',length(plot.data.gene$x))

keggview.native(
     plot.data.gene = plot.data.gene, 
     cols.ts.gene = COLOR_LIST,   ## Color List by the order of plot.data.gene
     node.data, 
     pathway.name = ko_ID,
     out.suffix = OUT_SUFFIX, 
     kegg.dir = IMG_FOLDER)
```


## 参考
KEGG: https://www.kegg.jp/   

(kofam_scan)[https://academic.oup.com/bioinformatics/article/36/7/2251/5631907]: ftp://ftp.genome.jp/pub/tools/kofam_scan/INSTALL   

Downloads: ftp://ftp.genome.jp/pub/  

一文快速读懂 KEGG 数据库与通路图: https://zhuanlan.zhihu.com/p/96008506

KGML: https://www.genome.jp/kegg/xml/docs/

KGML下载: https://www.kegg.jp/kegg/rest/keggapi.html

理解KGML：https://cloud.tencent.com/developer/article/1626035 

https://www.genome.jp/kegg/pathway.html
