import requests
import time
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded'
}



def parse_fasta(db_str,jgi):
    time.sleep(1)
    url = 'https://mycocosm.jgi.doe.gov/cgi-bin/dispTranscript?db={}&id={}&useCoords=1&withTranslation=1&dispRuler=1'.format(db_str,jgi)
    response = requests.get(url,headers=headers)
    assert len(response.text.split('begin<br>')) == 3
    html_str = response.text.split('begin<br>')[2]
    frames = [line for line in html_str.split('\n') if 'eg -0'==line[:5]]    ## get 'eg -0' lines
    tree = etree.HTML(''.join(frames)) 
    AA_fasta = ''.join(tree.xpath('//font//text()')).replace(' ','')
    return AA_fasta



with open('jgi_info.log','r') as fr, open('jgi.fa','w') as fw:
    while True:
        line = fr.readline()
        if not line:
            break
        db_str,jgi = line.split('\t')[0].split('?')[1].replace('db=','').replace('id=','').split('&')
        AA_fasta = parse_fasta(db_str,jgi)
        fw.write('>{}\n{}\n'.format(jgi,AA_fasta))



