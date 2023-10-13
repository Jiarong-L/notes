
在个人PC上运行mysql (Win10)


官网下载最新版本；记住初始密码！登录后修改：``` ALTER USER 'root'@'localhost' IDENTIFIED BY '' ```
```bash
mysqld --initialize --console
mysqld --install mysql

# Add mysql to PATH
net start mysql  #net stop mysql

# remove data/
mysqld --remove mysql


# 忘记密码 (fail)
net stop mysql
mysqld --console --skip-grant-tables --shared-memory
```


new console中输入```mysql```可进入Admin account，下例更新用户root信息
```bash
update user set authentication_string='' where user='root';
flush privileges;
```


创建user、database示例：
```bash
# 查看column:        desc mysql.user;
# 查看current user:     SELECT user();


# Add User
CREATE USER 'ljr'@'localhost' IDENTIFIED BY '123456';
update mysql.user set host='%' where user='ljr';
# Del User
DELETE FROM mysql.user WHERE user='ljr';


# 创建database并赋权限（赋权fail）
CREATE database if NOT EXISTS `jeecg-boot` default character set utf8mb4 collate utf8mb4_general_ci;
CREATE TABLE `ai_control_single`  (..........);
USE jeecg-boot;
GRANT all on * to 'ljr'@'localhost';


## 下载远程数据库  https://zhuanlan.zhihu.com/p/269983875
mysqldump -uroot -p --host=192.163.xxx.xxx --port=43306 --databases DemoDB > DemoDB.v1.sql
      username: root
      password: rootpass


## set Timezone
set global time_zone='+8:00';
```








