

DNA to Protein 时， 不同的生物可能会使用不同的 [Coden Table](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi)， 可至 NCBI 相关 assembly（？） 的页面搜索关键词 'Coden' 


此外，数据库的序列中会出现除了ATCG之外的字符，其对应如下：
```py
    degenerate_dict = {
        'A':'A',
        'T':'T',
        'C':'C',
        'G':'G',
        'R':'AG',
        'Y':'CT',
        'M':'AC',
        'K':'GT',
        'S':'GC',
        'W':'AT',
        'H':'ATC',
        'B':'GTC',
        'V':'GAC',
        'D':'GAT',
        'N':'ATCG'
    }
```


