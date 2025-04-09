
一款基于内存的分布式NoSQL数据库（Key:Value），Python/JS/Java 都有它的API。

[使用场景](https://www.bilibili.com/video/BV1yPpwetEuq/)：缓存SessionID/热门访问数据（内存加速），Redisson/RedLock/.. [分布式锁](https://www.cnblogs.com/liuqingzheng/p/11080501.html)，计数排序，分布式会话管理、通知推送、实时聊天（发布/订阅/消息队列），附近商家查询（地理空间）



## 简易示例

1. ```sudo apt install redis-server``` 进行安装
2. 服务端维持运行 ```redis-server --bind 127.0.0.1 --port 6333```
3. 另启客户端 ```redis-cli -h 127.0.0.1 -p 6333```
4. 数据库基本操作见 [RedisCheatSheet-ByGeekHour.pdf](Redis/RedisCheatSheet-ByGeekHour.pdf)
    - String/List/Set/SortedSet/Hash （键值对）
    - HyperLogLog（粗略统计）
    - Bitmaps/Bitfields
    - Geospatial （地理空间距离统计）



### 发布/订阅

1. 客户端A/B ```SUBSCRIBE mychannel```
2. 客户端C ```publish mychannel XXX```
3. 客户端A/B收到：(不过收不到订阅前的消息)

```
1) "message"
2) "mychannel"
3) "XXX"
```


### 消息队列

1. 客户端C ```XADD mystream * field value```
2. 客户端A/B/C都可以不限次数的查看/添加/删除/计数stream中信息 ```XRANGE mystream - +```

其中 XGROUP 可用于创建、管理消费者组，不过我的 6.0.16 版本似乎只有 DELCONSUMER 而没有 CREATECONSUMER


### 事务

```
MULTI              ## 所有命令会被放进同一队列进行缓存等待
<Command 1>
<Command 2>
<Command 3>
EXEC/DISCARD       ## EXEC开始执行事务命令后，其它终端的命令不会插队
```

若其中之一的语句执行失败，redis依然会执行其余语句、不会像SQL一样回滚


### Config

本例中，redis默认配置文件是 ```/etc/redis/redis.conf```，也可以启动时候使用自己的文件：```redis-cli my.conf```

```
## 3600秒内只要有一次修改就进行一次快照，也可手动保存：save
## 关于持久化，建议AOF模式：执行命令的同时将文件写入AOF文件中，若断电失去内存信息、下次启动可逐条执行记录的命令
save 3600 1

port 6379
bind 127.0.0.1 ::1
```

查看默认快照地址：```redis-cli config get dir ``` 



## 主从复制

Maser(1) 可读可写，Slave(n)只能从Maser处复制信息，只需 ```redis-server slave.conf``` （conf文件如下），随后客户端可链接 Slave

```
## replicaof <masterip> <masterport>
replicaof 127.0.0.1 6333

## 此处进行单机演示，正常情况下slave是其它服务器
dbfilename dump_1111.rdb
port 1111
bind 127.0.0.1 ::1
pidfile /var/run/redis/redis_1111.pid
```

此外，还可以设置哨兵节点，只需 ```redis-sentinel sentinel.conf``` （conf文件如下），如果现任 Maser 宕机，可将某个 Slave 重新任命为 Master

```
## sentinel monitor master <masterip> <masterport> <需要多少哨兵同意才进行故障转移>
sentinel monitor master 127.0.0.1  6333  1
```



## 参考
[Redis中文教程](https://redis.com.cn/tutorial.html)     
[教程-GeekHour](https://www.bilibili.com/video/BV1Jj411D7oG)    
[教程-讲解](https://www.bilibili.com/video/BV1ZVW6efEbD)      
[使用场景](https://blog.csdn.net/finally_vince/article/details/139499195)   
