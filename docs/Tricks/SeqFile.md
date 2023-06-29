


### [Fasta_Header_Rename.py](Scripts/Fasta_Header_Rename.py)
Turn header line to: >new_header_1, >new_header_2,...
```
Fasta_Header_Rename.py  <input_file.fa>  <output_file.fa>  <new_header>
```



### re提取字符串括号内的内容
参考: https://www.jianshu.com/p/e556fa43e4e1
```python
import re

pattern = re.compile(r'[(](.*?)[)]', re.S)  #最小匹配() -- 第一对()
pattern = re.compile(r'[(](.*)[)]', re.S)   #贪婪匹配() -- 最外围一对()
pattern = re.compile(r'\[(.*?)\]', re.S)    #最小匹配[]
pattern = re.compile(r'\[(.*)\]', re.S)     #贪婪匹配[]

re.findall(pattern, mystr)
```

