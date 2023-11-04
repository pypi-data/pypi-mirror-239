"""
考核条件如下 :
1.
数据/root/college/bike.csv上传至hdfs://college/目录下
hadoop fs -put /root/bike/bike.csv /college/

2.
统计本次数据所有单车数量（以单车车号进行计算，注意去重），结果写入本地/root/bike01/000000_0文件中。
(0/ 10分)
create table bike(
duration  int,
startdate string,
enddate string,
startnum int,
startstation string,
endnum int,
endstation string,
bikenum string,
usertype string
) row format delimited fields terminated by ',';
load data local inpath '/root/bike/bike.csv' into table bike;
insert overwrite local directory  '/root/bike01' row format delimited fields terminated by '\t' 
select count(distinct bikenum) from bike;
3.
计算单车平均用时，结果写入本地/root/bike02/000000_0文件中，以分钟为单位，对数据结果取整数值（四舍五入）。
(0/ 10分)
insert overwrite local directory  '/root/bike02' row format delimited fields terminated by '\t' 
select round(avg(duration / 60000)) from bike;


4.
统计常年用车紧张的地区站点top10，结果写入本地/root/bike03/000000_0文件中。(以stratstation为准)
(0/ 10分)
insert overwrite local directory  '/root/bike03' row format delimited fields terminated by '\t' 
select a.startstation from (select startstation,count(*) as num from bike group by startstation order by num desc limit 10) as a;
5.
给出共享单车单日租赁排行榜，结果写入本地/root/bike04/000000_0文件中。（以startdate为准,结果格式为2021-09-14）
(0/ 10分)
insert overwrite local directory  '/root/bike04' row format delimited fields terminated by '\t' 
select b.s_time from (select a.s_time,count(*) as num from (select from_unixtime( unix_timestamp(startdate,'yyyy-MM-dd HH:mm:ss'),'yyyy-MM-dd')  as s_time from bike) as a group by a.s_time order by num desc, a.s_time asc) as b;
6.
给出建议维修的单车编号（使用次数），结果写入本地/root/bike05/000000_0文件中。
(0/ 10分)
insert overwrite local directory  '/root/bike05' row format delimited fields terminated by '\t' 
select a.bikenum from (select bikenum,count(*) as num from bike group by bikenum order by num desc,bikenum asc limit 10) as a;
7.
给出可进行会员活动推广的地区，结果写入本地/root/bike06/000000_0文件中。（以stratstation为准）
insert overwrite local directory  '/root/bike06' row format delimited fields terminated by '\t' 
select a.startstation from (select startstation,count(*) as num  from bike where usertype<>"Member" group by startstation order by num desc, startstation asc limit 10) as a;

8.
给出可舍弃的单车站点，结果写入本地/root/bike07/000000_0文件中。（以endstation为准）
insert overwrite local directory  '/root/bike07' row format delimited fields terminated by '\t' 
select a.endstation from (select endstation,count(*) as num  from bike where usertype="Member" group by endstation order by num asc, endstation asc limit 10) as a;

"""