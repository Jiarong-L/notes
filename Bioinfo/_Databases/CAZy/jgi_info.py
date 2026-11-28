import requests
import time
from lxml import etree
import re

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded'
}


def suburl_jgi_hit(suburl):
    time.sleep(1)
    response = requests.get(suburl,headers=headers)
    html_str = response.text
    tree = etree.HTML(html_str)
    for jgiurl in tree.xpath('//td[@class="tdlistprot"]//@href'):
        time.sleep(1)
        jgi_response = requests.get(jgiurl,headers=headers)
        jgi_html_str = jgi_response.text
        jgi_tree = etree.HTML(jgi_html_str)
        # (start,end) = re.search(r'gi\|(.*?)\|', jgi_html_str, flags=0).span()    ## not only gi...
        # gi = html_str[start:end].split('|')[1]
        jgi = jgiurl.split('=')[-1]
        hit_info = '\t'.join(jgi_tree.xpath('//table[1]/tr[7]//text()')[1:])       ## https://www.genome.jp/dbget-bin/www_bget?hir:HETIRDRAFT_127157
        print("loading:{}\tjgi:{}\t{}".format(jgiurl,jgi,hit_info))


dom_lst = ['a','b','e','v']  ## ['a','b','e','v'] or just ['e'] 
idx_lst = ['','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

for d in dom_lst:
    for idx in idx_lst:
        time.sleep(1)
        url = 'http://www.cazy.org/{}{}.html'.format(d,idx)
        response = requests.get(url,headers=headers)
        html_str = response.text
        if 'Erreur [CAZy - 404-ERROR]' in html_str:
            continue
        tree = etree.HTML(html_str)
        for suburl,anno in zip(tree.xpath('//table[3]//a//@href'),tree.xpath('//table[3]//a//text()') ):
            if 'protein released by JGI' in anno:
                suburl_jgi_hit(suburl)