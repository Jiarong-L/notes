# MkDocs 静态网站构建
MkDocs: <https://www.mkdocs.org/>    
Setup MkDocs: <https://squidfunk.github.io/mkdocs-material/> 


## 简单使用
1.安装
```
pip install mkdocs
pip install mkdocs-material
```
2.基本命令
```
mkdocs new ./      #Create a new project in ./ Dir
mkdocs serve       #Start the live-reloading docs server.
mkdocs build       #Build the documentation site.
mkdocs -h          #Print help message and exit.
```
3.美化页面  
参照“mkdocs-material/setup”更改mkdocs.yml即可。


## Git Pages部署
1. 参考：<https://docs.github.com/en/actions/quickstart>，生成 [.github/workflows/notes.yml](https://github.com/Jiarong-L/notes/blob/main/.github/workflows/notes.yml)
2. git action 运行完成后，生成内容位于gh-pages分支，去Settings-Pages设置一下Build and deployment的分支即可。


## 其它平台
Gitee: https://help.gitee.com/services/gitee-pages/  
