
hicSPAdes_PATH = '/mnt/d/WSL_dir/workdir/hicSPAdes-binner-0.1/build/bin/'
SPAdes_PATH = '/mnt/d/WSL_dir/workdir/hicSPAdes-binner-0.1/build/SPAdes-3.15.4-Linux/bin/'
collect_PATH = '/mnt/d/WSL_dir/workdir/Collect.py'

import sys
import os
clean_lst_file = sys.argv[1]

def gen_block_sh(output_dir,r1,r2):
    out_sh = 'cd {}  \n'.format(output_dir)
    out_sh += 'export PATH={}:$PATH\n'.format(hicSPAdes_PATH)
    out_sh += 'export PATH={}:$PATH\n'.format(SPAdes_PATH)
    out_sh += 'metaspades.py -1 {} -2 {} -o . \n'.format(r1,r2)
    out_sh += 'hicspades-binner assembly_graph_with_scaffolds.gfa cleandata.yaml Bins \n'
    out_sh += 'cd Bins ; python3 {}; cd ..  \n'.format(collect_PATH)
    return out_sh

def gen_yaml_str(r1,r2):  # not sure about yaml.dump(out_dict)
    out_yaml = '\t{}\n'.format('[')
    out_yaml += '\t\t{}\n'.format('{')
    out_yaml += '\t\t\t{}: "{}",\n'.format('orientation','fr')
    out_yaml += '\t\t\t{}: "{}",\n'.format('type','hic')
    out_yaml += '\t\t\t{}: ["{}"],\n'.format('right reads',r1)
    out_yaml += '\t\t\t{}: ["{}"],\n'.format('left reads',r2)
    out_yaml += '\t\t{}\n'.format('}')
    out_yaml += '\t{}\n'.format(']')
    return out_yaml

with open(clean_lst_file) as fr:
    while True:
        line=fr.readline().strip()
        if not line:
            break
        [output_dir,r1,r2] = line.split('\t')
        try:
            os.mkdir(output_dir)
        except:
            print('{} already exists!'.format(output_dir))
        with open(output_dir+'/cleandata.yaml','w') as fw:
            out_yaml = gen_yaml_str(r1,r2)
            fw.write(out_yaml)
        with open(output_dir+'.pipe.sh','w') as fw:
            out_sh = gen_block_sh(output_dir,r1,r2)
            fw.write(out_sh)



            