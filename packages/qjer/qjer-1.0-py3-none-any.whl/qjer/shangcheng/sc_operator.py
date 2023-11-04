"""
1. 编写代码爬取给定网站的商品ID、名称、价格（销售价）、浏览量、销量、库存，并将数据写入/root/crawl2/goods.txt（自行创建目录）
（0.00 / 20分）
操作环境: Hadoop/Hive/Spark
2. hive中创建shopxo(库).goods表并导入数据，字段包括id,title,price,views,sales,stock。（注意先完成上一模块“开启单节点集群环境“，才能使用hive集群）
（0 / 20分）
create database shopxo;
use shopxo;
create table goods(
id int,
title string,
price float,
views int,
sales int,
stock int) row format delimited fields terminated by ',';
load data local inpath '/root/crawl2/goods.txt' into table goods;

操作环境: Hadoop/Hive/Spark
3. 查找缺失值，将表中价格为空（null）的数据，写入至文件/root/crawl2/01/000000_0（注意为虚拟机本地文件路径，下同）
（0 / 20分）
insert overwrite local directory '/root/crawl2/01/000000_0'
row format delimited fields terminated by '\t'
select * from goods where price is null;
4. 缺失值处理，title中去除“连衣裙”、“女士”及空值null数据，创建中间表goods1，存放过滤后的数据
（0 / 20分）

create table goods1 as select * from goods where not ((title is null) or (title like '%连衣裙%') or (title like '%女士%'))
5. 对中间表数据所有行进行统计，结果写入文件/root/crawl2/02/000000_0
（0 / 20分）
insert overwrite local directory '/root/crawl2/02/000000_0'
row format delimited fields terminated by '\t'
select count(*) from goods1;
6. 查询中间表goods1，按照价格降序查找前三条商品信息（去重，格式为title price），结果写入文件/root/crawl2/03/000000_0
（0 / 20分）
insert overwrite local directory '/root/crawl2/03/000000_0'
row format delimited fields terminated by '\t'
select title,price from goods1 order by price desc limit 3;
7. 分割title字段，要求第一个元素title[0]作为对应商品品牌，其他元素作为商品特征，对各品牌进行计数统计，将TOP10写入文件/root/crawl2/04/000000_0
（0 / 20分）
insert overwrite local directory '/root/crawl2/04/000000_0'
select a.brand,count(*) as num from (select split(title,' ')[0] as brand from goods1) group by a.brand order by num desc limit 10;
8. 对上题排名第一的品牌进行分析，根据其商品特征前6名进行特征统计，结果写入文件/root/crawl2/05/000000_0
（0 / 20分）
操作环境: Hadoop/Hive/Spark

"""