import sys
import time
import os

try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    new_header = sys.argv[3]
except:
    print('Usage: Fasta_Header_Rename.py  <input_file.fa>  <output_file.fa>  <new_header>')
    print('Change old header to new header, auto count')
    exit(0)


if input_file == output_file:
    output_file = input_file + '.tmp.{}'.format(time.time())
    replace_file = True
else:
    replace_file = False

i = 1
with open(input_file,'r') as fr, open(output_file,'w') as fw:
    while True:
        line = fr.readline()
        if not line:
            break
        if '>' == line.strip()[0]:
            print()
            line = '>{}_{}\n'.format(new_header,i)
            i = i+1
        fw.write(line)


if replace_file:
    os.remove(input_file)
    os.rename(output_file,input_file)

