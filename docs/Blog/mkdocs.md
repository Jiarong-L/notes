# MkDocs

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
.github/workflows/notes.yml中：
```
name: notes 
on:
  push:
    branches:
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - uses: actions/cache@v2
        with:
          key: ${{ github.ref }}
          path: .cache
      - run: pip install mkdocs-material 
      - run: mkdocs gh-deploy --force
```
随后参考：<https://docs.github.com/en/actions/quickstart>

