
* NR: Non-Redundant **Protein** Sequence Database
* NT: **Nucleotide** Sequence Database (of NR)

关联：NR SWissport GO KEGG 已实现相互注释

## Setup DB

可以从 [ncbi ftp blastdb](https://ftp.ncbi.nlm.nih.gov/blast/db) 处下载 FASTA 或者 BLAST DB，然后从 [accession2taxid](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/) 处下载 accession 与 taxid，gi 的关系。
```bash
wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/db/nr-prot-metadata.json
wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/db/nt-nucl-metadata.json
grep tar.gz nr-nucl-metadata.json | sed 's/"//g' | sed 's/,//g' | while read dd ; do wget -c $dd ; done
grep tar.gz nt-nucl-metadata.json | sed 's/"//g' | sed 's/,//g' | while read dd ; do wget -c $dd ; done


wget -c ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz
wget -c ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz


tar -xzf nr*.gz
tar -xzf nt*.gz
tar -xzf prot.accession2taxid.gz
tar -xzf nucl_gb.accession2taxid.gz

## 或者可以用BLAST包 update_blastdb.pl --showall
## nohup update_blastdb.pl --decompress nr >out.log 2>&1 &
##  GI number/ ACCESSION:  https://www.jianshu.com/p/84500d6c7aea
##  gb/WGS/TSA/... :  https://zhuanlan.zhihu.com/p/106664362
```


随后：[BLAST(NT)/Dimond(NR)](../_Blocks/BLAST.md) --> accession2taxid --> [NCBI Taxonomy](Taxonony.md)进行注释


