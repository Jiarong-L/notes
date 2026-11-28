import pandas as pd
import numpy as np
import sys

lvl_order='dkpcofgs'

def empty_lvl(lvl_order=lvl_order):
    empty_dict = {}
    for ll in lvl_order:
        empty_dict[ll]='other'
    return empty_dict

def lvl_split(x):
    res_dict=empty_lvl()
    if len(x.split('__')) ==1:
        return res_dict
    x_lst = x.strip().split(';')
    for xx in x_lst:
        lvl = xx.strip().split('__')[0]
        val = '__'.join(xx.strip().split('__')[1:])
        res_dict[lvl] = val
    return res_dict

try:
    file_dir = sys.argv[1]
    plot_lvl = sys.argv[2]
except:
    print('Usage: python3 formatting_Krona.py  <otu_taxa_table.xls>   <Taxa_lvls: dkpcofgs>  \n')
    print('Example: python3 formatting_Krona.py  otu_taxa_table.xls   dpcofgs  \n')
    print('Outputs: KronaInput.*   KronaRun.sh  \n')
    exit(0)


df = pd.read_csv(file_dir,sep='\t',index_col=0)
tax_col=df.columns[-1]
samples=df.columns[:-1].values

df['tax_dict'] = df[tax_col].apply(lambda x: lvl_split(x))
plot_order = [item for item in lvl_order if item in plot_lvl]
for lvl in plot_order:
    df[lvl] = df['tax_dict'].apply(lambda x: x[lvl])

with open('KronaRun.sh','w') as f:
    for ss in samples:
        temp_df = df[[ss] + plot_order]
        temp_df[temp_df[ss] > 0].to_csv('KronaInput.{}.{}.xls'.format(ss,''.join(plot_order)),sep='\t',header=False,index=False)
        f.write('ktImportText KronaInput.{}.{}.xls  -n {}  -o {}.html \n'.format(ss,''.join(plot_order),ss,ss))
