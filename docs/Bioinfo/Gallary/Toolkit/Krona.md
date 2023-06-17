<style>
img{
    width: 30%;
}
</style>

### Install
```
# https://github.com/marbl/Krona/wiki
conda create -n krona -c bioconda krona
source activate
conda activate krona
```

### Usage
Input Example (sep='\t')
```
21	Lvl1_A	Lvl2_A	Lvl3_a
296	Lvl1_A	Lvl2_B	Lvl3_b
213	Lvl1_A	Lvl2_C	Lvl3_c
213	Lvl1_A	Lvl2_C	Lvl3_d
213	Lvl1_A	Lvl2_C	Lvl3_e
```
Run
```
ktImportText KronaInput.xls  -n A1  -o A1.html 
```



### Packed for otu_taxa_table
[otu_taxa_Krona.py](Krona/otu_taxa_Krona.py) generates KronaRun.sh and KronaInput files
```
python3 otu_taxa_Krona.py  otu_taxa_table.xls   dpcofgs
source activate
conda activate krona
sh KronaRun.sh
conda deactivate
```

Example of otu_taxa_table
```
OTU_ID	S1	S2	taxonomy
OTU_1	21	12	d__Bacteria; p__Proteobacteria; c__Deltaproteobacteria; o__Desulfuromonadales; f__Sva1033; g__Sva1033; s__unclassified_Sva1033
OTU_2	26	23	d__Bacteria; p__Proteobacteria; c__Deltaproteobacteria; o__Myxococcales; f__Sandaracinaceae; g__uncultured; s__unclassified_uncultured

```


### 参考
[![Krona wiki](Krona/img/1.png)](https://github.com/marbl/Krona/wiki)







