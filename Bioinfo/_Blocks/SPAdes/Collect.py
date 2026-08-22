import os
try:
    os.system('rm bin_*.fa')
except:
    pass

## Input File #####
fasta_dir = '../scaffolds.fasta'
cluster_dir = 'clustering.tsv'
###################

def write_res(header,seq,file_path):
    with open(file_path,'a') as fw:
        fw.write('>{}\n{}\n'.format(header,seq))


cluster_dict = {}
with open(cluster_dir,'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        [contig,group] = line.strip().split('\t')
        cluster_dict[contig] = group

with open(fasta_dir,'r') as f:
    header = ''
    while True:
        line = f.readline()
        if not line:
            write_res(header,seq,file_path)
            break
        line = line.strip()
        if '>' == line[0]:
            if header:
                write_res(header,seq,file_path)
            header = line[1:]
            try:
                file_path = 'bin_{}.fa'.format(cluster_dict[header])
            except:
                file_path = 'non_clustered.fa'
            seq = ''
        else:
            seq += line