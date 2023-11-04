"""
1.
修改云主机host文件，添加内网IP，对应映射名为hadoop000，实现云主机自身使用root用户ssh访问hadoop000免密登陆
(0/ 10分)
操作环境：
Hadoop/Hive/Spark

hostnamectl set-hostname hadoop000
bash

ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cd .ssh/
ssh-copy-id hadoop000

vi /etc/hosts

ip hadoop000
2.
配置文件中修改zookeeper主机I P为外网地址，启动zookeeper
(0/ 10分)
操作环境：
Hadoop/Hive/Spark、Hadoop/Hive/Spark
vi /root/software/zookeeper-3.4.14/conf/zoo.cfg

zkServer.sh start
3.
格式化HDFS文件系统
(0/ 10分)
操作环境：
Hadoop/Hive/Spark
hadoop namenode -format
4.
启动Hadoop集群
(0/ 10分)
操作环境：
Hadoop/Hive/Spark
start-all.sh
5.
启动Spark集群（环境中Spark配置已经完成，直接开启即可，推荐使用绝对路径）
(0/ 10分)
操作环境：
Hadoop/Hive/Spark
/root/software/spark-2.4.3-bin-hadoop2.7/sbin/start-all.sh
6.
修改kafka配置文件server.properties，使用外网IP进行监听，补充zookeeper外网IP连接地址，启动Kafka服务
(0/ 10分)
操作环境：
Hadoop/Hive/Spark
Vi /root/software/kafka_2.10-0.10.2.2/config/server.properties


启动kafka
bin/kafka-server-start.sh -daemon  config/server.properties
7.
修改Hbase配置文件，使用外网 IP实现zookeeper访问,启动hbase
(0/ 10分)
操作环境：
Hadoop/Hive/Spark
vi conf/hbase-site.xml
追加

bin/start-hbase.sh
创建kafka topic
bin/kafka-topics.sh --create --topic iotTopic --partitions 3 --replication-factor 1 --zookeeper hadoop000:2181

创建hbase表
hbase shell
create ‘default:spark_iot’,’info’


启动kafka consumer
bin/kafka-console-consumer.sh --topic iotTopic --bootstrap-server hadoop000:9092
将Hbase scan数据导出到本地文件并命名为/root/spark_iot.csv
echo "scan 'default:spark_iot’” | hbase shell  > spark_iot.csv

"""