
https://docs.github.com/zh/get-started

### Config
依次有 --system  --global --local，一般来说使用--global；全部都设定的情况下，会执行--local
```
git config --global user.name "your-username"
git config --global user.email "your-email-address"
```


有时需要短暂的切换账户，那么就找个空文件夹生成./git，然后执行--local层面的config；在这个空文件夹中--local层面的注释覆盖--global
```
cd empty_dir/
mkdir .git
git config --global user.name "your-username"
git config --global user.email "your-email-address"
```

设置大小写敏感：
```
git config core.ignorecase false
```



### Clone
```
git clone xxxxxx

git clone -b mybranch xxxxx
```

### Init a local repo & push to remote
建议直接网页生成然后clone
```
cd empty_dir/
git init
....Do something, commit, push to remote

git remote add origin git@xxxxx.git
git pull origin master

git remote -v                     ## Check info
```




### New Branch
push to 远程的origin主机
```
git branch new_branch              ## create local
git checkout new_branch            ## switch to
git push origin new_branch         ## push to remote

git branch -a                      ## See all branch
```



### Pull/Push
```
git pull

git add <path_or_obj>
git commit -m 'commit_notes'
git push
```


### RollBack
https://blog.csdn.net/qing040513/article/details/109150075
```
git log --oneline                 ## see commit logs before HEAD version (all branches)
git reflog                        ## see commit logs ALL (current branch)


git reset --hard HEAD             ## back to current version, all modify DELETED
git reset --soft HEAD             ## back to current version, all modify Saved


git reset --hard HEAD^
git reset --hard HEAD^^
git reset --hard HEAD~3

git push -f
```

找回丢失的数据
```
git fsck --lost-found

git show xxxxVersionCOdexxxx
```

### .gitignore
只需在repo的根目录生成.gitignore文件，列出希望不希望上传的文件即可。若没有生效，是因为它只能忽略那些原来没有被track的文件，此时需要:
```
git rm -r --cached .     ## or: git rm -r --cached xx/yy.md
git add -A .
git commit -m "update .gitignore"
git push
```
删除所有本地缓存后重新commit，**Still Not Working, Why?**

