
将碳水化合物活性酶归入不同蛋白质家族

从[Cazy官网](http://www.cazy.org/)右上角 ‘DOWNLOAD CAZY’ 得到下载地址: 然后从ncbi/[jgi](https://genome.jgi.doe.gov/portal/)提取对应的**蛋白fasta序列**：此处用[jgi_info.py](Cazy/jgi_info.py)爬取 jgi_info，[jgi_fasta.py](Cazy/jgi_fasta.py)爬取 FASTA
```bash
wget -c http://www.cazy.org/IMG/cazy_data/cazy_data.zip
unzip cazy_data.zip
mv ssd/biblio/cazy_data/cazy_data.txt  cazy_data.txt
cut -f4,5 cazy_data.txt | grep ncbi | cut -f1 | sort |uniq > cazy.ncbi.acc  
cut -f4,5 cazy_data.txt | grep jgi  | cut -f1 | sort |uniq > cazy.jgi

python jgi_info.py > jgi_info.log  &                     ## need internet
wait
python jgi_fasta.py &                                    ## load in jgi_info.log and get fasta from webpage

seqkit grep -f cazy.all.acc  nr.fa -o ncbi.fa            ## also download nr!!

## too much : https://www.ncbi.nlm.nih.gov/sites/batchentrez
## TODO: check if  jgi.fa 's FASTA is correct
## TODO: check if  jgi.fa 's header matches cazy.jgi
## TODO: replace ncbi.fa 's header with jgi
## if not equals, may due to private part of db ???

cat ncbi.fa jgi.fa > cazy.fa
```

之后可以[Dimond](../Blocks/BLAST.md)注释



其它使用参考：
```basj
https://www.jianshu.com/p/57c2974f9376

https://zhuanlan.zhihu.com/p/657191429
```











