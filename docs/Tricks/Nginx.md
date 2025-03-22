
使用场景=网关：将请求均衡负载给多个前/后端服务器（高并发）、反向代理至前/后端服务器（1个ip=多台服务器）；单台服务器上部署多个静态网站

安装：[sudo apt install nginx](https://nginx.org/en/linux_packages.html#Ubuntu) 或 [Windows: download & unpack](https://nginx.org/en/download.html)


## 简单示意

启动Nginx
```bash
sudo nginx -s stop    ## quit/stop/reload/reopen
sudo nginx            ## 成功：命令行无返回，但浏览器中可打开 http://localhost:80/  
                      ##       ps -ef | grep nginx 查看master/worker进程
                      ## 失败的话试试 sudo service nginx restart
```

可以通过 ```nginx -V ``` 查找 nginx.conf 的位置，例如 ```...--conf-path=/etc/nginx/nginx.conf```


可以直接修改 conf 文件中的一部分：
```conf
worker_processes 1;         ## auto    平行进程的数量


events {
	worker_connections 1024;   ## of each worker
}
```


也可以通过include的方式：（注意相对/绝对路径），**注意 http/https**
```conf
http {
    include /etc/nginx/sites-enabled/*;        ## 此处是默认的server设置
    include /mnt/l/WSL_DIR/WORKDIR/my.config;   ## 下文配置
}
```

**修改完成后记得 reload ：** ```sudo nginx -s reload```


## Server

假设一台服务器上可以部署多个静态网站以节约资源，给每一个网站分配一个端口号即可（以及各自的域名）。conf中每一个Server相当于一台虚拟主机。

```conf
server {
        listen  7777;            ## 也可以加上ip；需要注意：是否已在此前的conf中被匹配占用，是则不会生效
        server_name  _;          ## 域名
        root           /mnt/l/WSL_DIR/WORKDIR/testNginx/htmlFolder/;
        index          myindex.html;


        rewrite_log     on;                                        ## 记录日志
        error_log       /mnt/l/WSL_DIR/WORKDIR/tmp/error.log;
        access_log      /mnt/l/WSL_DIR/WORKDIR/tmp/access.log;


        location / {            ##   http://localhost:7777/   即   http://localhost:7777/myindex.html    访问 root/index，即 myindex.html 内容
        }

        location /testA {       ##   http://localhost:7777/testA.html  
            return 301  http://www.baidu.com;        
        }

        location /testB {       ##   curl -I http://localhost:7777/testB.html   第一行中的响应码即701 ，也可以在日志中看到
            return 701  "str of code 701";        
        }
}
## 默认 listen 80(http) or 443(https)，此处修改为7777
```


root/alias也可以挪到location内，下例描述root/alias的区别：

```conf
server {
        listen  7777;            ## 也可以加上ip；需要注意：是否已在此前的conf中被匹配占用，是则不会生效
        server_name  _;          ## 域名

        location /withalias {       ##   http://localhost:7777/withalias/mytext.html    网址 ip/alias/mytext.html      访问本地地址 alias/mytext.html
            alias           /mnt/l/WSL_DIR/WORKDIR/testNginx/htmlFolder/;     
        }

        location /htmlFolder {       ##   http://localhost:7777/htmlFolder/mytext.html  网址 ip/location/mytext.html   访问本地地址 root/location/mytext.html
            root           /mnt/l/WSL_DIR/WORKDIR/testNginx/;    
        }
}
## 访问内容为  /mnt/l/WSL_DIR/WORKDIR/testNginx/htmlFolder/mytext.html
```


## 反向代理

许多大型服务有多台服务器，但客户只需要访问唯一的网址即可，这就用到了反向代理: ``` 网址 --> vm1/vm2/vm3```


首先，用不同的port运行Flask程序：（python port_xxx.py &） 假设它们就是由不同地址服务器提供的
```py
from flask import Flask
app = Flask(__name__)

@app.route("/whichport")
def hello():
    return "port=xxxx"

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=xxxx)
```


随后配置conf

```conf
upstream mybackend {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
        listen 7777;     
        location /whichport {  
            proxy_pass http://mybackend;
        }
}
```

之后每次访问 http://localhost:7777/whichport 可能会返回不同的内容（flask程序打印的端口号）



## https

以上都是http{...}，而https需要SSL证书

```bash
openssl genrsa -out private.key 2048                   ## 私钥 private.key
openssl req -new -key private.key -out cert.csr        ## 证书签名请求文件 cert.csr
--- type in answers ---
openssl x509 -req -in cert.csr -out ssl.pem -signkey private.key  ## SSL证书
```

conf中将http{...}修改为https{...}，添加：
```conf
server {
    listen 443 ssl;
    server_name  xxx.xxx.com

    ssl_certificate     /.../ssl.pem;  
    ssl_certificate_key  /../private.key;

    # ssl验证相关配置
    ssl_session_timeout  5m;    ## 缓存有效期
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;    ## 加密算法
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;    ## 安全链接可选的加密协议
    ssl_prefer_server_ciphers on;   ## 使用服务器端的首选算法
}
```

随后访问 https://xxx.xxx.com/，不过，自签名的证书会标红



## 参考

[nginx 官方doc](https://nginx.org/en/docs/)      
[教程-GeekHour](https://www.bilibili.com/video/BV1mz4y1n7PQ/)      
[多域名配置-GeekHour](https://geekhour.net/2021/01/31/nginx-config/)         
[location 配置1](https://segmentfault.com/a/1190000041217732)     
[location 配置2](https://segmentfault.com/a/1190000022315733)      
[Seajs + Nginx](https://blog.csdn.net/cookcyq__/article/details/129783405)     
[Nginx的工作流程](https://blog.csdn.net/qq_28567955/article/details/129261216)   

