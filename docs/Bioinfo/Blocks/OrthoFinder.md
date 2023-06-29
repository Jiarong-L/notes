<style>
img{
    width: 60%;
}
</style>

![1](OrthoFinder/img/1.png)


### Install
conda: 
```
conda create -n orthofinder2 -c bioconda orthofinder -y
conda activate orthofinder
conda deactivate
```

use [releases](https://github.com/davidemms/OrthoFinder/releases) if conda fails
```
wget https://github.com/davidemms/OrthoFinder/releases/download/2.5.5/OrthoFinder.tar.gz
tar xzvf OrthoFinder.tar.gz
export PATH=$PWD/OrthoFinder/:$PATH
```
如果GLIBC版本报错，可于[Tricks](../../../Tricks/Linux)中搜索关键词

### Usage
FAA_folder/中存放proteomes fasta，每个species一个文件; 先用其自带的ExampleData/
```
FAA_folder=OrthoFinder/ExampleData/

orthofinder -f $FAA_folder
```



### Results
output会在FAA_folder/中，比较难过
```
## $FAA_folder/OrthoFinder/Results_*/


Comparative_Genomics_Statistics/
Gene_Duplication_Events/
Gene_Trees/
Orthogroup_Sequences/
Orthogroups/
Orthologues/
Phylogenetic_Hierarchical_Orthogroups/
Phylogenetically_Misplaced_Genes/
Putative_Xenologs/
Resolved_Gene_Trees/
Single_Copy_Orthologue_Sequences/
Species_Tree/
WorkingDirectory/
```
详细解读见[exploring-orthofinders-results](https://davidemms.github.io/orthofinder_tutorials/exploring-orthofinders-results.html), 示例结果文件夹：[Results_Jun30.zip](../OrthoFinder/Results_Jun30.zip)


### 参考
Tutorial:  https://davidemms.github.io/   
友好阐释：https://blog.csdn.net/sinat_41621566/article/details/112320002   




https://www.jianshu.com/p/82d4cf6c3eda
