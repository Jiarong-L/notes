import pandas as pd
import sys

try:
    pathway_lst_dir = sys.argv[1]     ## pathway (kegg api)
    pathway_folder_dir = sys.argv[2]  ## pathway_folder
    output_dir = sys.argv[3]          ## pathway_info.xls
except:
    print('Usage: python3 Collect_pathway_info.py  pathway_lst  pathway_folder output_dir')
    exit(0)

def read_class_rel(file_dir):
    res_dict = {}
    res_dict['REL'] = []
    if_REL = False
    with open(file_dir) as f:
        while True:
            line = f.readline()
            if not line:
                return res_dict
            if 'CLASS' in line:
                res_dict['CLASS'] = line[5:].strip()
            if 'REL_PATHWAY' in line:
                if_REL = True
                res_dict['REL'].append(line[11:].strip().split(' ')[0])
            if if_REL:
                if line[0] == ' ':
                    res_dict['REL'].append(line.strip().split(' ')[0])


df = pd.read_csv(pathway_lst_dir,sep='\t',header=None)
df.columns = ['pathwayID','L3']
df.set_index('pathwayID', drop=False,inplace=True)
df_dict = {}
for pID in df['pathwayID']:
    file_dir = '{}/{}'.format(pathway_folder_dir,pID)
    temp_dict = read_class_rel(file_dir)
    temp_dict['L3'] = df['L3'][pID]
    df_dict[pID] = temp_dict

df = pd.DataFrame(df_dict).T.fillna('-;-')
df['REL'] = df['REL'].apply(lambda x: ';'.join(x) if x!=[] else '-')
df['L1'] = df['CLASS'].apply(lambda x: x.strip().split(';')[0].strip())
df['L2'] = df['CLASS'].apply(lambda x: x.strip().split(';')[1].strip())
df.index.name = 'pathwayID'
df[['REL','L1','L2','L3']].to_csv(output_dir,index=True,sep='\t')
