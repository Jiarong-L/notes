
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
git clone xxxxxx                       ## 默认的branch

git clone -b mybranch xxxxx            ## 指定branch
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


### Switch Branch

```
git checkout new_branch            ## switch to new_branch (连带着内容显示也一起)
```


### New Branch

```
git branch new_branch              ## create local

git push origin new_branch         ## push *new_branch to remote/origin （push to 远程的origin主机）
```
另外，本地位于 branchA 时， 运行  ```git merge branchB``` 可以将 B 合并入 A


### Delete Branch
！！请谨慎使用，不可恢复    

**注意，push 才会对远程仓库造成修改，否则只是修改本地的仓库**&记录
```
git branch -d localBranchName               ##  del localBranch
git branch -r -d origin/remoteBranchName    ##  del remoteBranch's LOCAL RECORD, will not showup when 'git branch -r'
                                            ##  still available on Github webpage (the real remote repo:origin)

git push origin --delete remoteBranchName   ##  del remoteBranch
                                            ##  not available anymore on Github webpage
```

当网页上删除/创建了branch，需要 pull 后才能更新到本地的remoteBranch记录（git branch -r 查看），不过不会自动创建对应的localBranch

特别的，当网页上删除了远程仓库，可以运行 ```git remote prune origin```对 remote/origin 在本地的显示记录进行同步删除


### Pull/Push
```
git pull

git add <path_or_obj>
git commit -m 'commit_notes'
git push
```

拉取远程分支到本地：手动创建localBranch后再关联远程，或者

```
## 含映射关系：切换至localBranch（若不存在则新建一个），且拉取remoteBranch的代码
git checkout -b localBranchName origin/remoteBranchName

## 不含映射关系：创建localBranch且拉取remoteBranch的代码
git fetch origin remoteBranchName:localBranchName
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


### 查看/修改仓库文件
有时本地删除某文件后，需要同步从仓库中删除：假设需要删除‘./aax.md’
```
git ls-files | grep aax
git rm ‘./aax.md’
```
然后 commit & push    ！！ 需慎重

若有如下警告，说明‘./aax.md’于本地依旧存在（不确定）
```
error: the following file has changes staged in the index:
    aaa.txt
(use --cached to keep the file, or -f to force removal)
```


### Track Branch

本地分支与远程分支之间的 tracking: ```git branch -a``` 查看本地（关于local与remote分支的）branches记录，而 ```git remote show origin``` 查看远程origin主机的branches记录

* 设置pull关联
```
##                                remote       local
git branch --set-upstream-to=origin/gh-pages  gh-pages
```

* 查看关联状态
```
$ git remote show origin           ####### 检查跟踪 origin 中分支的状态
* remote origin
  Fetch URL: git@github.com:Jiarong-L/notes.git
  Push  URL: git@github.com:Jiarong-L/notes.git
  HEAD branch: main
  Remote branches:
    CC       new (next fetch will store in remotes/origin)  ## 网页上新创建，还没有来得及pull记录
    gh-pages tracked
    main     tracked
    newTest  tracked
  Local branches configured for 'git pull':           ## pull 时
    gh-pages merges with remote gh-pages              ## newTest 没有设置 upstream，故不在此
    main     merges with remote main
  Local refs configured for 'git push':
    gh-pages pushes to gh-pages (local out of date)   ## push 时
    main     pushes to main     (up to date)          ## 自动设置
    newTest  pushes to newTest  (up to date)


$ git branch -a                     ####### 查看所有分支，其中 CC 的记录还没有更新至本地
  gh-pages
* main             ## 目前所处分支
  newTest
  remotes/origin/HEAD -> origin/main
  remotes/origin/gh-pages
  remotes/origin/main
  remotes/origin/newTest
```

* 取消pull关联（或者直接-d删除本地branch） 
```
##                            local
git branch --unset-upstream  newTest
```

Q: [停止跟踪Git中的一个远程分支?](https://cloud.tencent.com/developer/ask/sof/108969602/answer/133469378)









