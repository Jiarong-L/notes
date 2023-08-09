


ko - reference pathway map linked to KO entries (K numbers)
rn - reference pathway map linked to REACTION entries (R numbers)
ec - reference pathway map linked to ENZYME entries (EC numbers)
org (three- or four-letter organism code) - organism-specific pathway map linked to GENES entries (gene IDs)


## Download & Install
### links
KEGG数据库-人类 
```
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


### kofam_scan
```
wget -c ftp://ftp.genome.jp/pub/db/kofam/ko_list.gz
wget -c ftp://ftp.genome.jp/pub/db/kofam/profiles.tar.gz
gunzip ko_list.gz
tar -xzf profiles.tar.gz
KO_LIST=$PWD/ko_list
PROFILE_DIR=$PWD/profiles/

conda create -n kofam -c bioconda kofamscan     ##  hmmer parallel ruby
conda activate kofam
```
### K, ko, layers
```
wget -c http://rest.kegg.jp/list/ko
wget -c http://rest.kegg.jp/list/pathway

wget -c http://rest.kegg.jp/link/ko/pathway -O pathway_KO.mapped
wget -c http://rest.kegg.jp/link/pathway/ko -O KO_pathway.mapped


mkdir map_folder
cd map_folder
cut -f1 ../pathway |cut -f2 -d ':'  |while read dd ; do wget -c http://rest.kegg.jp/get/$dd ;sleep 1; done
cd ..

python3 Collect_pathway_info.py  pathway  map_folder  pathway_info.xls
```

check results:
```
less pathway_info.xls |cut -f 1,3,4,5 |less
awk -F '\t' '{if ($3!="-" && $4!="-") print ($1,$3,$4,$5)}'  pathway_info.xls |  less


mkdir ko_folder; cd ko_folder
cut -f1 ../pathway |cut -f2 -d ':'  | sed -e 's/map/ko/g'|while read dd ; do wget -c http://rest.kegg.jp/get/$dd ;sleep 1; done
cd ..

mkdir check_ko
ls ko_folder | while read dd ; do ln -s ko_folder/$dd check_ko/$dd ; done
awk -F '\t' '{if ($3!="-" && $4!="-") print ($1)}'  pathway_info.xls |  sed -e 's/map/ko/g' |while read dd ; do rm check_ko/$dd ; done

ls check_ko
ko01100  ko01110  ko01120  ko01200  ko01210  ko01212  ko01220  ko01230  ko01232  ko01240  ko01250
```
示例: [ko01100](https://www.kegg.jp/dbget-bin/www_bget?pathway+ko01110)无pathway_info(layer info)，[ko05416](https://www.genome.jp/dbget-bin/www_bget?ko05416)有pathway_info(Class: Human Diseases,Cardiovascular disease)


## Anno
### kofam_scan: K
```
exec_annotation uniqGeneSet.faa -o kegg.txt -p $PROFILE_DIR -k $KO_LIST
```
kegg.txt: 多个hits，选E-value最优一个
```
# gene name           KO     thrshld  score   E-value KO definition
#-------------------- ------ ------- ------ --------- ---------------------
  GeneA        K00121  619.83  560.5  7.2e-172 S-(hydroxymethyl)glutathione dehydrogenase / alcohol dehydrogenase [EC:1.1.1.284 1.1.1.1]
  GeneA        K00001  345.97  308.1   2.5e-95 alcohol dehydrogenase [EC:1.1.1.1]
  GeneA        K00055  389.00  305.5   8.8e-95 aryl-alcohol dehydrogenase [EC:1.1.1.90]
  GeneA        K00153  383.77  276.3   7.8e-86 S-(hydroxymethyl)mycothiol dehydrogenase [EC:1.1.1.306]
```


### K to ko,layers
双方并非一一对应关系；K可以参与多个ko，ko也可以包含多个K。上述下载文件[pathway_KO.mapped](http://rest.kegg.jp/link/ko/pathway),[KO_pathway.mapped](http://rest.kegg.jp/link/pathway/ko)，以及归纳的pathway_info.xls描述了三者的对应关系。
```
TBA
```


## KEGG Graph
对于一些关注基因(e.g.差异表达),[Color tool](https://www.genome.jp/kegg/mapper/color.html)可在线标注颜色，或者[使用url控制颜色](https://www.kegg.jp/kegg/docs/color_url.html)，本地可使用使用[pathview R包](https://zhuanlan.zhihu.com/p/601451821),或者也可[下载KGML](https://www.kegg.jp/kegg/rest/keggapi.html)后用[cytoscape-KEGGscape](https://zhuanlan.zhihu.com/p/371399566)绘制。

### KGML
[理解KGML](https://cloud.tencent.com/developer/article/1626035),下载示例
```
mkdir KGML;cd KGML;
for dd in hsa00600; do 
wget https://rest.kegg.jp/get/$dd/kgml -O $dd.kgml;
wget https://rest.kegg.jp/get/$dd/image -O $dd.png;
done
```
[KGML颜色说明](https://www.kegg.jp/kegg/docs/color_gui.html)  

### pathview
Install:
```
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("pathview")

browseVignettes("pathview")
```

Usage:
```
library("pathview")

```

### keggtools

```
pip install keggtools
pip install graphviz
```

```
import keggtools

```






## Info
```
Carbon metabolism - ko01200
Methane metabolism - ko00680
Nitrogen metabolism - ko00910
Sulfur metabolism - ko00920
```


## 参考
KEGG: https://www.kegg.jp/   

(kofam_scan)[https://academic.oup.com/bioinformatics/article/36/7/2251/5631907]: ftp://ftp.genome.jp/pub/tools/kofam_scan/INSTALL   

Downloads: ftp://ftp.genome.jp/pub/  

一文快速读懂 KEGG 数据库与通路图: https://zhuanlan.zhihu.com/p/96008506

KGML: https://www.genome.jp/kegg/xml/docs/

KGML下载: https://www.kegg.jp/kegg/rest/keggapi.html

理解KGML：https://cloud.tencent.com/developer/article/1626035 


