
一款基于内存的分布式NoSQL数据库（Key:Value），Python/JS/Java([Spring Data Redis](https://docs.springframework.org.cn/spring-data/redis/reference/index.html)) 都有它的API。

[使用场景](https://www.bilibili.com/video/BV1yPpwetEuq/)：
    
1. 分布式会话管理：[缓存SessionID](https://blog.csdn.net/qq_34207422/article/details/144747200)（[Spring Session](https://docs.springframework.org.cn/spring-session/reference/guides/java-redis.html)）& Redisson/RedLock/.. [分布式锁](https://www.cnblogs.com/liuqingzheng/p/11080501.html)

2. 热门访问数据：内存加速 [@Cacheable](https://blog.csdn.net/CompiShoal/article/details/154135010)、计数排序（[ZSetOperations](https://blog.csdn.net/zhangbeizhen18/article/details/130119763)）、附近商家查询（地理空间 @GeoIndexed）


3. 通知推送、实时聊天（发布/订阅/消息队列）


## 简易示例

1. ```sudo apt install redis-server``` 进行安装
2. 服务端维持运行 ```redis-server --bind 127.0.0.1 --port 6333```
3. 另启客户端 ```redis-cli -h 127.0.0.1 -p 6333```
4. 数据库基本操作见 [RedisCheatSheet-ByGeekHour.pdf](Redis/RedisCheatSheet-ByGeekHour.pdf)
    - String/List/Set/SortedSet(zSet)/Hash(键值对) 
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

1. XADD 创建 Stream 并写入消息：客户端C ```XADD mystream * field value```，其中 ```*``` 表示自动生成StreamID

2. XREAD 读取 Stream 中消息
    - 客户端A/B/C都可以XADD/XDEL/不限次数的查看 Stream 中信息：```XREAD COUNT 2 BLOCK 1000 STREAMS mystream 0``` 返回 2 条 ```StreamID > 0``` 的消息（改成 ```$``` 则表示此XREAD命令之后新写入的StreamID）


3. XGROUP 协调对 Stream 的读取，避免被不同 customer（可以指定映射给一个固定IP/pid）重复读取
    - ```XGROUP CREATE mystream mygroup $``` 在指定的 Stream 上创建一个消费者组、**指定从**```$```开始消费
    - ```XREADGROUP GROUP mygroup customerA COUNT 2 STREAMS mystream >``` 投递2条**未被这个组投递过的消息**(```>```)给```customerA```（自动创建）
    - ```XACK mystream mygroup 1792384461852-0``` 业务确认处理完成后，按照 StreamID **移除某条 Pending** 消息

请参考 [Redis Streams](https://docs.springframework.org.cn/spring-data/redis/reference/redis/redis-streams.html) 查看 Spring 中 Redis 功能的写法，例如上述命令对应的 Java 代码：

```java
List<MapRecord<String, Object, Object>> records = template.opsForStream().read(
        Consumer.from("mygroup", "customerA"),                      // GROUP mygroup customerA
        StreamReadOptions.empty().count(2),                         // COUNT 2
        StreamOffset.create("mystream", ReadOffset.lastConsumed())  // STREAMS mystream >
);

// ------------------
for (MapRecord<String, Object, Object> record : records) {
    // 业务处理：略
    // record.getId() ，record.getValue() 
    template.opsForStream().acknowledge("mygroup", record); // 对应 XACK mystream mygroup <id>
}
```

投递后但未确认的消息显示 Pending ，会一直留在 mygroup 的 PEL 里，不会再被 ```>``` 读到，除非 ```XCLAIM mystream mygroup customerB 3600000 1792384461852-0``` 在阻塞 3600000ms 后将这条消息转移给另一个消费者B
    
```XPENDING mystream mygroup``` 查看各消费者的 Pending 分布，```XPENDING mystream mygroup - + 1000000``` 列出 Pending 消息 

---------------------------

版本事项：6.2.0版本前只有 DELCONSUMER 而没有 CREATECONSUMER，CheatSheet里手动```XGROUP CREATECONSUMER mystream mygroup customerA```的用法是新版本，但不常用、可忽略

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
其它消息中间件：[RabbitMQ](https://rabbitmq.cn/), [Kafka](https://kafka.apache.org/), 利用 Lists 的基本操作制作最简单的先进先出队列（LPUSH/RPOP）


