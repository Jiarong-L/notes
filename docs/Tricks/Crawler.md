使用Python爬虫爬取网页数据；  
其它：Scrapy 框架

## Robots协议
* 域名/robots.txt
* 例如：https://zhuanlan.zhihu.com/robots.txt
```
User-agent: *         *表示所有搜索引擎准守
Disallow: /?s*        ?s*表示不能爬取带有“/?s”的路径
Disallow: /           表示所有内容都不能爬取
```

## 网络请求
* 如果批量发送请求，可以 ```time.sleep(t)``` 设置间隔t秒
* 可以使用 [multiprocessing](https://zhuanlan.zhihu.com/p/103135242) 线程池异步发送请求；或 [asyncio 协程异步](https://zhuanlan.zhihu.com/p/59621713)
* User-Agent、返回信息等 可以打开浏览器-审查元素-网络-XHR 发送一次请求后查看响应内容
* 有些可能也需要记录cookie，下次请求时在header里带上 ；此时需要使用 session 进行POST操作；(不同服务器的设置下，cookie也许会过期、也许每次都会变化)
* 建议使用 ```response.status_code``` 判断请求状态
* ```requests.get(proxies={},..)``` 设置代理  


session: 
```py
sessionA = requests.session()
sessionA.get(...)             
sessionA.post(...)       
```

multiprocessing: 
```py
import multiprocessing
def funcA(url):
    pass

pool = multiprocessing.Pool(processes = 3)
map(funcA, ['urlA','urlB','urlC'])
```

### POST
```py
import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded'
}
response = requests.post(url = url,data = {'kw' : 'aaa'},headers = headers)

response.json()              # JSON parse；
```


### GET
```py
import requests

response = requests.get(url)
response.text                # HTML string
response.content             # HTML binary (e.g. 图片以二进制字符串而非src表示)
```



## HTML文本处理
1. 进行标签定位  
2. 标签数据提取
3. 可能需要注意中文乱码问题：```text.encode('iso-8859-1').decode('gbk')``` 或 ```text.encoding = 'utf-8'```

### [正则](https://www.w3schools.cn/python/python_regex.asp)
示例：
```py
import re
## example_html = response.text

ex_h = '<h.>.*?</h.>'                ## ex_h = '<h.>(.*?)</h.>' 只返回括号内字段
re.findall(ex_h,example_html,re.S)  ## S: 单行 M:多行
```
写法参考[w3cschool]('https://www.w3schools.cn/python/python_regex.asp#元字符')

### [bs4](https://beautifulsoup.cn/)
Install: lxml是第三方的解析器，bs4默认支持Python标准库中的HTML解析器
```
pip install beautifulsoup4
pip install lxml   
```

示例：
```py
from bs4 import BeautifulSoup

## 'myattr'正常情况下可以是class，id 等
example_html = '<mytag>OOO<button>BBB</button><p myattr="pClass1" myattr_sub="pClass1_sub">PPP1</p><t>TTT</t><p myattr="pClass2">PPP2</p></mytag>'
soup = BeautifulSoup(example_html, 'lxml')  ## 若是文件：BeautifulSoup(open("index.html"))

soup.find('mytag').find('p')  ## 第一个mytag标签的第一个p标签：<p myattr="pClass1" myattr_sub="pClass1_sub">PPP1</p>
soup.mytag.p                  ## 同上
soup.find(myattr="pClass1")   ## 返回第一个myattr="pClass1"的框

soup.find_all('mytag')[0].find_all('p')[0]   ## find_all返回所有符合条件的框，以list的形式
soup.find_all(myattr="pClass1")[0]


soup.mytag.p.name               ## 'p'
soup.mytag.p.attrs              ## {'myattr': 'pClass1', 'myattr_sub': 'pClass1_sub'}

soup.mytag.p['myattr']          ## 'pClass1'

soup.mytag.p.next_sibling       ## soup.mytag.p的下一个标签,不一定是p：<t>TTT</t>


## 也可以修改soup对象
soup.t.name = 'w'
soup                            ## <html><body><mytag>...<w>TTT</w>...</body></html>


## 获取文本数据
soup.mytag.text                 ## 所有文本 'OOOBBBPPP1TTTPPP2' 
soup.mytag.get_text()

soup.mytag.p.string              ## 只能是直系文本，并且似乎当内含子元素时会失效 
```
1. 实例化一个bs4对象，加载html数据至该对象
2. 调用bs4对象的属性与方法进行定位  

### etree
Install: 
```
pip install lxml  
```

示例：
```py
from lxml import etree

example_html = '<mytag>OOO<button>BBB</button><p myattr="pClass1" myattr_sub="pClass1_sub">PPP1</p><t>TTT</t><p myattr="pClass2">PPP2</p></mytag>'
## etree.HTML自动加上了/html/body
tree = etree.HTML(example_html) ## 若是文件：etree.parse("index.html")

tree.xpath('/html/body/mytag/p')   ##  /表示单个层级、从根节点开始;[<Element p at 0x1238ec7b940>, <Element p at 0x1238ec40c00>]
tree.xpath('/html//p')             ##  //表示任意层级

tree.xpath('/html//p[@myattr="pClass1"]')
tree.xpath('/html//p[2]')          ## 第二个p; [<Element p at 0x1238ecc0580>]

tree.xpath('/html//p/text()')      ## 取文本；/text()取直系文本、//text()取所有文本  ['PPP1', 'PPP2']
tree.xpath('/html//p/@myattr')     ## 取某属性值  ['pClass1', 'pClass2']
```
1. 实例化一个etree对象，加载html数据至该对象
2. 调用etree对象的xpath方法进行定位 

## 验证码
使用验证码识别工具，比如使用OpenCV或Tensorflow训练一个？ 暂无资源
```py
## 1. 请求页面；获取返回的验证码
## 2. 识别验证码
## 3. 将识别结果与其余数据 POST回去 （e.g.模仿上传button激发的的POST操作）
```

## [Selenium](https://www.selenium.dev/zh-cn/documentation/webdriver/getting_started/)
操纵浏览器; 需要下载浏览器驱动，见：[Firefox](https://github.com/mozilla/geckodriver/releases/), [Chrome](http://chromedriver.storage.googleapis.com/index.html), [IE](http://selenium-release.storage.googleapis.com/index.html),[Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) （另：Safari无需下载驱动）


```py
driver = webdriver.Chrome(r'chromeDriver_dir') ## FireFox, Chrome, Ie, Edge, Safari

driver.get(url)

driver.find_elements_by_xpath('...')[0].click()
driver.accept()

driver.quit()
```
详细操作见 [Selenium Doc](https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/)

