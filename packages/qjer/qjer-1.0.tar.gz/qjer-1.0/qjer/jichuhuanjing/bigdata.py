"""
一、基础环境配置
1、修改主机名
master、slave1、slave2分别执行
hostnamectl set-hostname master
2、修改host文件
master、slave1、slave2分别执行
vi /etc/hosts
内网ip master
内网ip slave1
内网ip slave2
3、修改时区
master、slave1、slave2分别执行
tzselect 5 9 1 1
vi /etc/profile
TZ=’Asia/Shanghai’; export TZ
source /etc/profile
4、操作NTP
master节点
vim /etc/ntp.conf
server 127.127.1.0
fudge 127.127.1.0 stratum 10

systemctl restart ntpd

slave1 、 slave2
ntpdate master

6 添加定时任务
分钟值（0-59） 小时（0-23） 几号（1-31） 几月（1-12） 星期几（1-7）

slave1、slave2分别执行
crontab -e
*/30 10-17 * * * /usr/sbin/ntpdate master
7、免密登录
master执行
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

ssh-copy-id master
ssh localhost

ssh-copy-id slave1
ssh-copy-id slave2

8、安装Java
master执行
mkdir /usr/java
tar -zxvf /usr/package277/jdk-8u221-linux-x64.tar.gz -C /usr/java/
vi /etc/profile
export JAVA_HOME=/usr/java/jdk1.8.0_221
export CLASSPATH=$JAVA_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin

source /etc/profile
java -version
scp -r /usr/java slave1:/usr/
scp -r /usr/java slave2:/usr/
scp /etc/profile slave1:/etc/profile
scp /etc/profile slave2:/etc/profile

slave1、slave2分别执行
source /etc/profile

二、安装zookeeper
master 执行

mkdir /usr/zookeeper
tar -zxvf /usr/package277/zookeeper-3.4.14.tar.gz -C /usr/zookeeper/

vi /etc/profile
export ZOOKEEPER_HOME=/usr/zookeeper/zookeeper-3.4.14
export PATH=$PATH:$ZOOKEEPER_HOME/bin
source /etc/profile

vim /usr/zookeeper/zookeeper-3.4.14/conf/zoo.cfg
tickTime=2000
initLimit=10
syncLimit=5
clientPort=2181
dataDir=/usr/zookeeper/zookeeper-3.4.14/zkdata
dataLogDir=/usr/zookeeper/zookeeper-3.4.14/zkdatalog
server.1=master:2888:3888
server.2=slave1:2888:3888
server.3=slave2:2888:3888

cd /usr/zookeeper/zookeeper-3.4.14
mkdir zkdata zkdatalog

cd /usr/zookeeper/zookeeper-3.4.14/zkdata
echo 1 > myid

scp -r /usr/zookeeper slave1:/usr/
scp -r /usr/zookeeper slave2:/usr/

scp /etc/profile slave1:/etc/profile
scp /etc/profile slave2:/etc/profile

slave1、slave2分别执行

source /etc/profile

slave1中操作
cd /usr/zookeeper/zookeeper-3.4.14/zkdata
echo 2 > myid

slave2中操作
cd /usr/zookeeper/zookeeper-3.4.14/zkdata
echo 3 > myid

master、slave1、slave2分别执行

zkServer.sh start
zkServer.sh status

三、安装hadoop

master执行
mkdir /usr/hadoop
tar -zxvf /usr/package277/hadoop-2.7.7.tar.gz -C /usr/hadoop/

vim /etc/profile
#hadoop
export HADOOP_HOME=/usr/hadoop/hadoop-2.7.7
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
source /etc/profile


cd /usr/hadoop/hadoop-2.7.7/etc/hadoop/
vim hadoop-env.sh
粘贴一下内容
export JAVA_HOME=/usr/java/jdk1.8.0_221

vim yarn-env.sh
粘贴一下内容
export JAVA_HOME=/usr/java/jdk1.8.0_221

vim core-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>fs.default.name</name>
<value>hdfs://master:9000</value>
</property>
<property>
<name>hadoop.tmp.dir</name>
<value>/root/hadoopData/tmp</value>
</property>


vim hdfs-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>dfs.replication</name>
<value>2</value>
</property>
<property>
<name>dfs.namenode.name.dir</name>
<value>/root/hadoopData/name</value>
</property>
<property>
<name>dfs.datanode.data.dir</name>
<value>/root/hadoopData/data</value>
</property>
<property>
<name>dfs.permissions</name>
<value>false</value>
</property>
<property>
<name>dfs.datanode.use.datanode.hostname</name>
<value>true</value>
</property>


vim yarn-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>yarn.resourcemanager.admin.address</name>
<value>master:18141</value>
</property>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
<value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>


cp mapred-site.xml.template mapred-site.xml
vim mapred-site.xml
按a进入编辑模式，粘贴一下内容

<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>


echo master > master
cat master
echo slave1 > slaves
echo slave2 >> slaves
cat slaves


scp -r /usr/hadoop slave1:/usr/
scp -r /usr/hadoop slave2:/usr/

scp /etc/profile slave1:/etc/profile
scp /etc/profile slave2:/etc/profile

slave1、slave2分别执行
source /etc/profile

master执行
hadoop namenode -format
start-all.sh

四、安装hive

1、配置mysql
slave2中操作

systemctl start mysqld
grep "temporary password" /var/log/mysqld.log
mysql -uroot -p  回车后粘贴密码，然后回车，显示mysql>表示mysql连接成功
mysql中操作一下语句
set global validate_password_policy=0;
set global validate_password_length=4;
alter user 'root'@'localhost' identified by '123456';
create user 'root'@'%' identified by '123456';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;
flush privileges;


2、安装hive

mkdir /usr/hive
tar -zxvf /usr/package277/apache-hive-2.3.4-bin.tar.gz -C /usr/hive/


vim /etc/profile
按a进入编辑模式，粘贴一下内容
#hive
export HIVE_HOME=/usr/hive/apache-hive-2.3.4-bin
export PATH=$PATH:$HIVE_HOME/bin
source /etc/profile

cd conf
vim hive-env.sh
按a进入编辑模式，粘贴一下内容
export HADOOP_HOME=/usr/hadoop/hadoop-2.7.7
export HIVE_CONF_DIR=/usr/hive/apache-hive-2.3.4-bin/conf
export HIVE_AUX_JARS_PATH=/usr/hive/apache-hive-2.3.4-bin/lib


cp $HIVE_HOME/lib/jline-2.12.jar $HADOOP_HOME/share/hadoop/yarn/lib/

scp -r /usr/hive slave1:/usr/


scp -r /etc/profile slave1:/etc/profile


slave1中操作
source /etc/profile
cp $HIVE_HOME/lib/jline-2.12.jar $HADOOP_HOME/share/hadoop/yarn/lib/
cp /usr/package277/mysql-connector-java-5.1.47-bin.jar /usr/hive/apache-hive-2.3.4-bin/lib/
cd /usr/hive/apache-hive-2.3.4-bin/conf/
vim hive-site.xml
按a进入编辑模式，粘贴一下内容
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
<property>
<name>hive.metastore.warehouse.dir</name>
<value>/user/hive_remote/warehouse</value>
</property>
<property>
<name>javax.jdo.option.ConnectionDriverName</name>
<value>com.mysql.jdbc.Driver</value>
</property>
<property>
<name>javax.jdo.option.ConnectionURL</name>
<value>jdbc:mysql://slave2:3306/hive?createDatabaseIfNotExist=true&amp;useSSL=false</value>
</property>
<property>
<name>javax.jdo.option.ConnectionUserName</name>
<value>root</value>
</property>
<property>
<name>javax.jdo.option.ConnectionPassword</name>
<value>123456</value>
</property>
</configuration>


master节点操作：
cd /usr/hive/apache-hive-2.3.4-bin/conf/
vim hive-site.xml
按a进入编辑模式，粘贴一下内容
<configuration>
<property>
<name>hive.metastore.warehouse.dir</name>
<value>/user/hive_remote/warehouse</value>
</property>
<property>
<name>hive.metastore.local</name>
<value>false</value>
</property>
<property>
<name>hive.metastore.uris</name>
<value>thrift://slave1:9083</value>
</property>
</configuration>


slave1节点：
schematool -dbType mysql -initSchema
hive --service metastore
master节点：
hive
出现hive>说明连接成功
show databases;
create database hive;

五、安装spark

master执行：
mkdir /usr/spark
tar -zxvf /usr/package277/spark-2.4.3-bin-hadoop2.7.tgz -C /usr/spark/


vim /etc/profile
按a进入编辑模式，粘贴一下内容
#spark
export SPARK_HOME=/usr/spark/spark-2.4.3-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin

source /etc/profile

cd /usr/spark/spark-2.4.3-bin-hadoop2.7/conf/
vim spark-env.sh
按a进入编辑模式，粘贴一下内容
export JAVA_HOME=/usr/java/jdk1.8.0_221
export HADOOP_HOME=/usr/hadoop/hadoop-2.7.7
export HADOOP_CONF_DIR=/usr/hadoop/hadoop-2.7.7/etc/hadoop
export SPARK_MASTER_IP=master
export SPARK_WORKER_MEMORY=8g

echo slave1 > slaves
echo slave2 >> slaves

scp -r /usr/spark slave1:/usr/
scp -r /usr/spark slave2:/usr/

slave1和slave2编辑环境变量文件
vim /etc/profile
按a进入编辑模式，粘贴一下内容
#spark
export SPARK_HOME=/usr/spark/spark-2.4.3-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin

所有节点执行source /etc/profile

master节点执行
cd /usr/spark/spark-2.4.3-bin-hadoop2.7/sbin
./start-all.sh


六、平台运维
1、动态添加节点
slave3执行：
hostnamectl set-hostname slave3
bash

master执行：
vim /etc/hosts
在此文件中添加slave3的内网IP和主机名
添加完成保存推出

ssh-copy-id slave3回车后输入yes，输入密码，完成免密
scp /etc/profile slave3:/etc/profile

slave3执行：
source /etc/profile
date查看时区是否为CST时区

master执行：
scp /etc/hosts slave1:/etc/hosts
scp /etc/hosts slave2:/etc/hosts
scp /etc/hosts slave3:/etc/hosts

slave3执行：
crontab -e
按a进入编辑模式，粘贴一下内容
*/10 * * * * /usr/sbin/ntpdate master

master执行：
cd /usr/hadoop/hadoop-2.7.7/etc/hadoop/
echo slave3 >> slaves

scp -r /usr/java slave3:/usr/
scp -r /usr/hadoop slave3:/usr/

slave1和slave2执行
echo slave3 >> /usr/hadoop/hadoop-2.7.7/etc/hadoop/slaves

slave3执行：
hadoop-daemon.sh start datanode
yarn-daemon.sh start nodemanager

2、集群动态删除节点
master执行
echo slave3 > /usr/hadoop/hadoop-2.7.7/etc/hadoop/excludes
vim /usr/hadoop/hadoop-2.7.7/etc/hadoop/hdfs-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>dfs.hosts.exclude</name>
<value>/usr/hadoop/hadoop-2.7.7/etc/hadoop/excludes</value>
</property>

hdfs dfsadmin -refreshNodes
hdfs dfsadmin -report


slave3执行：
hadoop-daemon.sh stop datanode
yarn-daemon.sh stop nodemanager


master执行
start-balancer.sh
hdfs dfsadmin -refreshNodes
时间较长，7分钟左右，从live 到dead

七、集群调优与运维

操作环境: Hadoop/Hive/Spark
hostnamectl set-hostname hadoop000
vim /etc/hosts
按a进入编辑模式，粘贴一下内容
内网ip hadoop000

ssh hadoop000 然后输入yes，显示成功后，输入exit退出连接

echo $HADOOP_HOME
cd /root/software/hadoop-2.7.7/etc/hadoop/
vim hdfs-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>dfs.namenode.heartbeat.recheck-interval</name>
<value>275000</value>
</property>
<property>
<name>dfs.heartbeat.interval</name>
<value>5</value>
</property>

vim core-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>fs.trash.interval</name>
<value>10080</value>
</property>
<property>
<name>fs.trash.checkpoint.interval</name>
<value>0</value>
</property>

vim yarn-site.xml
按a进入编辑模式，粘贴一下内容
<property>
<name>yarn.nodemanager.pmem-check-enabled</name>
<value>false</value>
</property>
<property>
<name>yarn.nodemanager.vmem-check-enabled</name>
<value>false</value>
</property>
<property>
<name>yarn.nodemanager.vmem-pmem-ratio</name>
<value>5</value>
</property>


hadoop namenode -format
start-all.sh

检查文件是否存在
ll /root/software/hadoop-2.7.7/README.txt
hdfs dfs -put /root/software/hadoop-2.7.7/README.txt /
hdfs dfs -ls /    检查是否上传成功

查看spark-env.sh文件
cd /root/software/spark-2.4.3-bin-hadoop2.7/conf/
vim spark-env.sh  检查没问题就可以保存推出

启动spark
cd /root/software/spark-2.4.3-bin-hadoop2.7/sbin
./start-all.sh


八、数据分析

1、大数据处理与应用（Hive技术）

hive启动
systemctl start mysqld
schematool -dbType mysql -initSchema
初始化完成后
执行hive，进入hive>这个状态，输入show databases;看是否能够正常输出

create database hive;

use hive;

use hive;
create table traffic(
    peopletype string,
               roadnum string,
                       carid int,
                             time timestamp,
                                  province string,
                                           gender string,
                                                  age int,
                                                      drivertype string,
                                                                 belt string,
                                                                      airbags string,
                                                                              popup string,
                                                                                    injury string,
                                                                                           operation string,
                                                                                                     sight string,
                                                                                                           check string) row format delimited fields terminated by ',';



load data local inpath '/root/traffic/traffic.csv' into table traffic;

create table driver as select * from traffic where peopletype='司机' and age is not null;

第三题
insert overwrite local directory '/root/traffic1'
row format delimited fields terminated by '\t'
select count(*) from traffic;

第四题
insert overwrite local directory '/root/traffic2'
row format delimited fields terminated by '\t'
select count(*) from driver;

第五题
insert overwrite local directory '/root/traffic3'
row format delimited fields terminated by '\t'
select drivertype,count(*) from driver where drivertype='C1'
group by drivertype;

第六题
insert overwrite local directory '/root/traffic4'
row format delimited fields terminated by '\t'
select ceiling(avg(age)) from driver;

第七题
insert overwrite local directory '/root/traffic5'
row format delimited fields terminated by '\t'
select age,count(*) c from driver
group by age
order by c
limit 3;

第八题
insert overwrite local directory '/root/traffic6'
row format delimited fields terminated by '\t'
select operation,count(*) from driver where operation like '变道不当' and gender='女';

第九题
insert overwrite local directory '/root/traffic7'
row format delimited fields terminated by '\t'
select t2.c,count(*)
(select t1.check as c, t1.province,t1.gender from driver t1
where t1.province like '江苏' and t1.gender like '男') t2
where t2.c='拒绝检测'
group by t2.c;

第十题
insert overwrite local directory '/root/traffic8'
row format delimited fields terminated by '\t'
select province,count(*) from driver
where year(time)=2019
group by province
order by c asc
limit 4;


2、论坛数据分析
第一题
mkdir discuz
粘贴Py代码
IP修改为内网IP
python *.py

第二题

create table data(
    tid int,
        author string,
               score int,
                     grate string,
                           title string,
                                 content string
) row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' with SERDEPROPERTIES("separatorChar"=",") STORED AS TEXTFILE;

导入数据

load data local inpath "/root/discuz/data.txt" into table data;

insert overwrite local directory '/root/discuz01'
row format delimited fields terminated by '\t'
select count(*) from data;


insert overwrite local directory '/root/discuz02'
row format delimited fields terminated by '\t'
select count(distinct author) from data;


insert overwrite local directory '/root/discuz03'
row format delimited fields terminated by '\t'
select author,count(*) as sum from data group by author order by sum desc,author asc limit 10;


insert overwrite local directory '/root/discuz04'
row format delimited fields terminated by '\t'
select a.author,a.grate from (select author,grate,count(*) as sum from data group by author,grate order by sum desc limit 1) as a;


insert overwrite local directory '/root/discuz05'
row format delimited fields terminated by '\t'
select author,score from data group by author,score order by score desc limit 5


3、网站访问量分析
hostnamectl set-hostname hadoop000
vim /etc/hosts
按a进入编辑模式，粘贴一下内容
内网ip hadoop000

ssh hadoop000 然后输入yes，显示成功后，输入exit退出连接
hadoop namenode -format
start-all.sh

hdfs dfs -mkdir /input
hdfs dfs -put .../ /input
systemctl start mysqld

"""