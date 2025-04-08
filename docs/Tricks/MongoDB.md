


NoSQL数据库：可以类似关系型数据库，但不需要预先创建Table，也不需要预设字段类型长度，数据也不需要有相同的结构

图形化管理工具可用 compass/**navicat** 

可通过 [Mongoose](https://mongoose.nodejs.cn/docs/index.html) 与 NodeJS 交互，也有与 R 交互的 mongolite 包 [(GIS示例)](https://www.mongodb.com/resources/languages/mongodb-and-r-example)，与 [SpringBoot 的交互示例](https://blog.csdn.net/qq_46112274/article/details/117425532)


应用：[GeoJson -- GIS/游戏地图 数据](https://www.cnblogs.com/oloroso/p/9777141.html)，在线chatbot会话储存...


| SQL | MongoDB |
| -- | -- |
| Table | Collection |
| Row | Document (a Record in Binary JSON) 每一条数据以文档的形式存储!  |
| Column | Field |
| Index | Index |
| Primary Key | _id |
| ```join``` | ```$lookup``` |
| ```groupby``` | ```$group``` |



## 简易示例


建议遵照 [v5.0教程 apt安装](https://www.mongodb.com/zh-cn/docs/v5.0/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition) --- 也可以下载对应操作系统的 [MongoDB Community Server/Tools](https://www.mongodb.com/try/download/community) 后 ```sudo dpkg -i xx.deb```(```-l list / -r remove```)


随后，启动 mongod 进程 

```bash
sudo systemctl daemon-reload     ## 更新所有服务的配置文件，port占用见 ss -tlnp

sudo systemctl start mongod      ## start  /  stop  /  restart  /   enable设置开机启动
sudo systemctl status mongod     ## 查看运行状态
```


注意，WSL中或许需要安装 [Systemd 套件](https://learn.microsoft.com/zh-cn/windows/wsl/systemd)，而如果出现 status=14 错误则需要修改以下权限

```bash
sudo chown -R mongodb:mongodb /var/lib/mongodb        ## /etc/mongod.conf 中配置的 dbPath
sudo chown mongodb:mongodb /tmp/mongodb-*.sock

sudo touch /etc/init.d/mongod
sudo chmod +x /etc/init.d/mongod
```

成功后，可以使用 ```mongosh``` Shell 进行交互，默认为 test 数据库，可用 ```show dbs``` 查看其它，然后 ```use anotherDB``` 新建/切换至其它数据库


### mongosh

增/删/改/查见 [教程](https://www.mongodb.com/zh-cn/docs/v5.0/crud/)，此处增加两个 User

```
db.userCollection.insertMany([
    {name : "Ann", age : 10} ,
    {name : "Bee", age : 20} ,           // 自动生成  _id: ObjectId('67f382376609a69b4a6b140b')
])


db.userCollection.find().sort({age: 1})     // Find all Users & 排列: 升序(1)降序(-1)
db.userCollection.find({age: {$gt: 10} })   // Find age>10 Users
db.userCollection.find({name: {$regex: /a*n/ , $options: 'i' } }) 

db.userCollection.countDocuments()
```


### Mongoose

```npm install mongoose --save``` 本地安装后，进入 node



```js
//import { createRequire } from 'module';
//const require = createRequire(import.meta.url);


const dbURL = 'mongodb://127.0.0.1:27017/test';
const options = {};


const mongoose = require('mongoose');
mongoose.connect(dbURL,options).then( ()=>{console.log("Connected")} ).catch( (err)=>{console.log(err)} )

// Schema and Model !!
const UserSchema = new mongoose.Schema({name: String, age: Number});
const User = mongoose.model("user",UserSchema,"userCollection")   // Default collection will be user+s !!!

// Save to DB
let Cee = new User({name: 'Cee', age: 30})
Cee.save().then( (obj)=>{console.log(obj.name)} )

// Load from DB
await User.findOne({age: {$gt: 10}})

for await (const item of User.find()) {
  console.log(item.name,item.age); 
}
```

关于 [Mongoose 获取数据库列表 ](https://geek-docs.com/mongodb/mongodb-questions/35_mongodb_getting_list_of_all_databases_with_mongoose.html)






