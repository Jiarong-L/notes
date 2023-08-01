---
title: NCBI Taxonony
date: 2022-01-01 19:32:55
tags:
---

# NCBI Taxonony 

1. 下载 [taxdump.tar.gz](ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz) 
2. 简化一下将要使用的文件。提取names中储存学名的行，nodes的taxid、parent_id、tax_level列
```
grep 'scientific name'  names.dmp > names.dmp.scientific
cut -f 1,3,5 nodes.dmp > nodes.dmp_simplified
```
3. 用法
    * 从names.dmp中找到目标物种的taxid
    * 从nodes.dmp中回溯其parent id直至顶端
    * 利用names.dmp将parent id翻译为物种名
    * 注意，ncbi中可能会有taxa名称相同、但taxid不同的情况，他们就是不同的taxa。
    * 另，使用前，也可以删除一些无意义的字符，比如 ' " [] () 

## 示例
本示例中，由于只关注界门纲目科属种(NCBI中的Domain其实是superkingdom)，因此使用dict形式来返回结果，方便提取。若要完全NCBI的taxonomy，改用list或者string就好。  

另：uniqName_id_dict_eachlevel存储每个目标level中没有重复的taxa name，若名字重复，只能从names_df里找了，会慢一点。  

```
import pandas as pd
import numpy as np

names_dir = 'taxdump/names.dmp.scientific'
nodes_dir = 'taxdump/nodes.dmp_simplified'
target_level = ['superkingdom','phylum','class','order','family','genus','species']
target_level_abbrev = ['d','p','c','o','f','g','s']
abbrev_dict = dict(zip(target_level,target_level_abbrev)) 


names_df = pd.read_csv(names_dir,sep = '\t',header = None)[[0,2]]
names_df.columns = ['id','Name']
names_df.set_index('id',inplace = True)
id_names_dict = dict(zip(names_df.index.values,names_df['Name']))                      ##

nodes_df = pd.read_csv(nodes_dir,sep = '\t',header = None)
nodes_df.columns = ['id','parent_id','level']
nodes_df.set_index('id',inplace = True)
id_parentid_dict = dict(zip(nodes_df.index.values,nodes_df['parent_id'].values))       ##
id_level_dict = dict(zip(nodes_df.index.values,nodes_df['level'].values))              ##

uniqName_id_dict_eachlevel = {}
for temp_lvl in target_level:
    temp_all_ids = nodes_df[nodes_df['level'] == temp_lvl].index.values
    temp_names_df = names_df.loc[temp_all_ids].copy()
    temp_names_df['id'] = temp_names_df.index.values
    temp_val_counts = temp_names_df['Name'].value_counts()
    temp_val_counts = temp_val_counts[temp_val_counts == 1]
    temp_val_counts = pd.DataFrame({'Name' : temp_val_counts.index.values})
    temp_uniq_df = pd.merge(temp_names_df,temp_val_counts,on='Name')
    uniqName_id_dict_eachlevel[temp_lvl] = dict(zip(temp_uniq_df['Name'],temp_uniq_df['id']))

def find_tax(taxid,tax_dict,id_names_dict = id_names_dict, id_parentid_dict = id_parentid_dict,id_level_dict=id_level_dict):   
    temp_name = id_names_dict[taxid]
    temp_level = id_level_dict[taxid]
    temp_parent_id = id_parentid_dict[taxid]
    tax_dict[temp_level] = temp_name
    if taxid != temp_parent_id:
        tax_dict = find_tax(temp_parent_id,tax_dict)
    return tax_dict                            # this method will loose 'no rank' layers, since there might be multiple of them!

def tax_dict2str(tax_dict,target_level = target_level):
    tax_str = ''
    for lvl in target_level:
        try:
            val = abbrev_dict[lvl] + '__' + tax_dict[lvl]+ ';'
        except:
            val = abbrev_dict[lvl] + '__' + 'norank' + ';'
        tax_str += val
    tax_str = tax_str.strip(';')
    return tax_str

################### Example 1 #####
e1_name = 'Dickeya phage phiDP10.3'
e1_taxid = uniqName_id_dict_eachlevel['species'][e1_name]
e1_taxdict = find_tax(e1_taxid,{})
e1_taxfull = tax_dict2str(e1_taxdict)
```




