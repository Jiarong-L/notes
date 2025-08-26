


比较准确，但是内存消耗量大；常用于给MAGs注释物种


## Download & Install
需要留意[**数据库&软件版本对应关系**](https://ecogenomics.github.io/GTDBTk/announcements.html)
```
conda create -n gtdbtk -c bioconda gtdbtk=2.3.0 -y
cd /mnt/d/WSL_dir/home/miniconda3/envs/gtdbtk/share/gtdbtk-1.0.2
wget -c https://data.gtdb.ecogenomic.org/releases/release214/214.0/auxillary_files/gtdbtk_r214_data.tar.gz
tar -xzf gtdbtk_r214_data.tar.gz
rm -r db; mv release214 db

## GTDBTK_DATA_PATH in /mnt/d/WSL_dir/home/miniconda3/envs/gtdbtk/etc/conda/activate.d/gtdbtk.sh
##  is   /mnt/d/WSL_dir/home/miniconda3/envs/gtdbtk/share/gtdbtk-1.0.2/db/
```

ncbi_taxdump(记录版本)
```
wget https://data.gtdb.ecogenomic.org/releases/release214/214.0/auxillary_files/ncbi_taxdump_20220917.tar.gz
```


## Usage

* classify_wf: 通过单拷贝基因，基于GTDB reference tree 注释物种；identify-->align-->classify
* [de_novo_wf](https://ecogenomics.github.io/GTDBTk/commands/de_novo_wf.html): identify-->align-->infer-->root-->decorate，一般不用这个

```
gtdbtk classify_wf -x fa --genome_dir MAGs_genomes/ --out_dir ./ --prefix MAGs --min_perc_aa 30 --cpus 32

## MAGs_genomes/ : genome_1.fa genome_2.fa genome_3.fa
```


## Outputs

* [参考汇总](https://ecogenomics.github.io/GTDBTk/files/index.html)
* [gtdbtk.ar122.summary.tsv/gtdbtk.bac120.summary.tsv](https://ecogenomics.github.io/GTDBTk/files/summary.tsv.html)
```
user_genome classification  fastani_reference       fastani_reference_radius        fastani_taxonomy        fastani_ani     fastani_af      closest_placement_reference     closest_placement_taxonomy      closest_placement_ani   closest_placement_af    pplacer_taxonomy        classification_method   note    other_related_references(genome_id,species_name,radius,ANI,AF)  aa_percent      translation_table       red_value       warnings
genome_2    d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__VadinCA11 sp002498365    GCA_002498365.1 95.0    d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__VadinCA11 sp002498365    99.16   0.94    GCA_002498365.1 d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__VadinCA11 sp002498365    99.16   0.94    d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__ ANI/Placement   topological placement and ANI have congruent species assignments        GCA_002505345.1, s__VadinCA11 sp002505345, 95.0, 89.92, 0.89; GCA_002509405.1, s__VadinCA11 sp002509405, 95.0, 88.13, 0.89      87.1    11      N/A     N/A
genome_3    d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__VadinCA11 sp002498365    GCA_002498365.1 95.0    d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__VadinCA11 sp002498365    95.33   0.87    GCA_002498365.1 d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__VadinCA11 sp002498365    95.33   0.87    d__Archaea;p__Thermoplasmatota;c__Thermoplasmata;o__Methanomassiliicoccales;f__Methanomethylophilaceae;g__VadinCA11;s__ ANI/Placement   topological placement and ANI have congruent species assignments        GCA_002505345.1, s__VadinCA11 sp002505345, 95.0, 94.26, 0.87; GCA_002509405.1, s__VadinCA11 sp002509405, 95.0, 90.74, 0.77      73.07   11      N/A     N/A
genome_1    d__Archaea;p__Euryarchaeota;c__Methanobacteria;o__Methanobacteriales;f__Methanobacteriaceae;g__Methanobrevibacter;s__Methanobrevibacter ruminantium     GCF_000024185.1 95.0    d__Archaea;p__Euryarchaeota;c__Methanobacteria;o__Methanobacteriales;f__Methanobacteriaceae;g__Methanobrevibacter;s__Methanobrevibacter ruminantium     100.0   1.0     GCF_000024185.1 d__Archaea;p__Euryarchaeota;c__Methanobacteria;o__Methanobacteriales;f__Methanobacteriaceae;g__Methanobrevibacter;s__Methanobrevibacter ruminantium     100.0   1.0     d__Archaea;p__Euryarchaeota;c__Methanobacteria;o__Methanobacteriales;f__Methanobacteriaceae;g__Methanobrevibacter;s__   ANI/Placement   topological placement and ANI have congruent species assignments        GCA_900321995.1, s__Methanobrevibacter sp900321995, 95.0, 80.9, 0.7; GCF_900114585.1, s__Methanobrevibacter olleyae, 95.0, 79.96, 0.55; GCA_900314635.1, s__Methanobrevibacter sp900314635, 95.0, 78.45, 0.3    97.09   11      N/A     N/A
```


## 参考
GTDB-Tk官网: https://gtdb.ecogenomic.org/




