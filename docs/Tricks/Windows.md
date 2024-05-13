


一些win系统的使用场景


## Win11 修改DNS

网络和Internet -- 以太网 -- DNS服务器分配 --（默认的“DHCP”改为“手动”）-- 修改IPV4 为：

```
114.114.114.114
8.8.8.8
```



## 硬盘弹出

大容量硬盘弹出时显示占用： 

win + R 后输入eventvwr.msc 打开事件查看器，进入Windows日志-系统，最新显示的警告应该就是来自刚才硬盘弹出失败，其中显示了占用的进程，于是可以去 任务管理器-进程 中关闭


## 蓝牙

升级系统后网卡/蓝牙消失了，可能是因为驱动太新、硬件太旧，卸载后重新按照匹配的网卡驱动即可，可自 设备管理器 中查询硬件型号


## Server
将Win电脑作为web server，（IIS）参考： https://zhuanlan.zhihu.com/p/533305943



## win11右键默认显示更多选项

```
reg.exe add "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /f /ve

## 重新启动，或重启资源管理器
taskkill /f /im explorer.exe
start explorer.exe
```

恢复原状：
```
reg.exe delete "HKCU\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32" /va /f
```


## WSL home
用softlink的方式节约C盘空间，似乎可行
```bash
mkdir /mnt/l/WSL_dir/Ubuntu_Home/
cd /mnt/l/WSL_dir/Ubuntu_Home/
mv ~ .
cd /home
rm <userfolder>
ln -s /mnt/l/WSL_dir/Ubuntu_Home/<userfolder>
```

